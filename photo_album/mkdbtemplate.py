import collections
import configparser
from jinja2 import (Environment, FileSystemLoader, PackageLoader,
        select_autoescape)
import logging
import os
import re
import sqlite3
import stat
import subprocess
import sys
from photo_album import (Album, Package, CustomArgumentParser)
from photo_album.mkgallerytiff import get_crop


logger = logging.getLogger(__name__)


def mk_db_template_album(config, build=True):
    """
    Make DB templates for all packages in scope.
    """
    work_dir = get_work_dir(config, build)
    packages = Album(config, build)

    for pkgid in packages.keys():
        mk_db_template(config, packages[pkgid], build)


def get_package(config, pkgid, build=True):
    """
    Get a single package.
    """
    work_dir = get_work_dir(config, build)
    packages = Album(config, build)
    return packages[pkgid]


def mk_db_template(config, package, build=True):
    """
    Build a package database template. Update existing if it already exists.

    Warning: The update mechanism is a one-shot update. It will do nothing if
    the SQL is already current.
    """
    pkgid = package["pkgid"]
    work_dir = get_work_dir(config, build)
    db_dir = config.get('album', 'database_directory')
    tiff_src_dir = config.get('album', 'tiff_source_directory')
    gallery_tiff_dir = config.get('album', 'gallery_tiff_directory')

    package_contents = Package(config, pkgid, build)
    mapfile = os.path.join(work_dir, pkgid, tiff_src_dir, 'rename_map.txt')
    map = read_alt_file_map(mapfile)

    newpkg = collections.OrderedDict()
    for photoid in sorted(package_contents.keys()):
        newpkg[map.get(photoid, photoid)] = {}

    for photoid in sorted(newpkg.keys()):
        photo = os.path.join(
                work_dir, pkgid, gallery_tiff_dir, '{}.tif'.format(photoid))
        logger.debug("Identifying photograph {}".format(photo))
        if os.path.isfile(photo):
            run = subprocess.run(
                ['identify', photo], stdout=subprocess.PIPE, check=True)
            match = re.search(
                r'\d+x\d+\+\d+\+\d+', run.stdout.decode("utf-8"))
            if match:
                crop = match.group()
                logger.debug("Found crop marks: {}".format(crop))
                newpkg[photoid]['crop'] = crop

    env = Environment(
        loader=PackageLoader("photo_album", package_path="templates"),
        autoescape=select_autoescape(['sql'])
    )

    template_vars = {
        "package": package,
        "photographs": newpkg,
    }

    sql_template = env.get_template('PKG-template.sql')

    dbfile = os.path.join(db_dir, 'PKG-{}.sql'.format(pkgid))
    if os.path.isfile(dbfile):
        logger.warn("PKG-{}.sql exists. Performing update.".format(pkgid))
        update(package_contents, pkgid, newpkg, dbfile)
    else:
        logger.info("Writing package {}.sql".format(pkgid))
        with open(dbfile, 'w') as f:
            f.write(sql_template.render(template_vars))


def update(package_contents, pkgid, package, dbfile):
    """
    This is a migration and will not be useful once the one-time migration is
    complete.
    """
    pkg = package_contents
    with open(dbfile, 'r') as f:
        content = f.readlines()

    pinserts = {}
    cropfmt = """    /* crop */          '{}',\n"""
    for photoid in package.keys():
        for line in [x for x in content]:
            m = re.match(r'INSERT INTO photographs VALUES', line)
            if m:
                idx = content.index(line)
                pattern = re.sub(r'\+', '\\+', photoid)
                if (re.search(r'{}'.format(pattern), content[idx + 2])):
                    cropval = "{}x{}+{}+{}".format(*get_crop(pkg, photoid))
                    pinserts[photoid] = [
                        content[idx + 0],
                        content[idx + 1],
                        content[idx + 2],
                        cropfmt.format(cropval),
                        content[idx + 4],
                        content[idx + 5],
                        content[idx + 6],
                        content[idx + 7],
                    ]
                    for i in range(8):
                        del content[idx]
                    break

    for photoid in package.keys():
        if photoid in pinserts:
            for line in pinserts[photoid]:
                content.append(line)
        elif pinserts.keys():
            cropval = "{}x{}+{}+{}".format(*get_crop(pkg, photoid))
            content.append("INSERT INTO photographs VALUES (\n")
            content.append("    /* pkgid */         '{}',\n".format(pkgid))
            content.append("    /* photoid */       '{}',\n".format(photoid))
            content.append("    /* crop */          '{}',\n".format(cropval))
            content.append("    /* poi */           '0',\n")
            content.append("    /* description */   ''\n")
            content.append(");\n")
            content.append("\n")

    logger.debug("Content line count: {}".format(len(content)))
    for line in content:
        logger.debug(line.rstrip())

    with open(dbfile, 'w') as f:
        for line in content:
            f.write(line)


def get_work_dir(config, build):
    """
    Get the work directory.
    """
    if build:
        return config.get('album', 'build_directory')
    else:
        return config.get('album', 'album_directory')


# This was copied/pasted from photo_rename because I want intstant
# gratification.
def read_alt_file_map(mapfile, lineterm=None, delimiter='\t'):
    """
    Read a filename map for the purpose of transforming the filenames as
    an alternative to using EXIF/XMP metadata DateTime information. Only
    require map file as an absolute path.
    """
    with open(mapfile, 'r') as f:
        lines = [
            line for line in f.readlines() if not line.startswith('#')]

    if lineterm is None:
        lineterm = get_line_term(lines)

    # Get a list of destination filenames from map so we can check for
    # dupes. This may seem pedantic but it will avoid a lot of trouble if
    # there is a duplicate new filename because of human error.
    files = [
        str.split(line.rstrip(lineterm), delimiter)[1] for line in lines]
    dupe_file = scan_for_dupe_files(files)
    if dupe_file:
        raise Exception(
            "Duplicate destination filename detected: {}".format(dupe_file))

    # XXX: This is soooo cool! List of lists flattened all on one nested
    # comprehension.
    # [[k1, v1], [k2, v2], ..., [kn, vn]]
    #                               --> {k1: v1, k2: v2, ..., kn: vn}
    return dict(zip(*[iter([x for sublist in [
        str.split(line.rstrip(lineterm), delimiter) for line in lines]
        for x in sublist])] * 2))


# This was copied/pasted from photo_rename because I want intstant
# gratification.
def get_line_term(lines):
    """
    Find line termination style. Require every line to have the same
    termination.
    """
    lineterm = None
    for line in lines:
        if line.endswith('\r\n'):
            term = '\r\n'
        elif line.endswith('\n'):
            term = '\n'
        if lineterm is not None and lineterm != term:
            raise Exception("Inconsistent line termination.")
        else:
            lineterm = term
    return lineterm


# This was copied/pasted from photo_rename because I want intstant
# gratification.
def scan_for_dupe_files(files):
    """
    O(n^2) scan of desination list for duplicates. Used when processing a
    map file. Returns True if duplicate files.
    """
    for ofile in files:
        count = 0
        for ifile in files:
            if ofile == ifile:
                count += 1
            if count > 1:
                return ifile
    return False


def main():
    """
    Parse command-line arguments. Initiate file processing.
    """
    parser = CustomArgumentParser()
    parser.add_argument("-a", "--album",
            help="Work in album directory. Danger!", action="store_true")
    parser.add_argument("-c", "--config", help="Configuration file.")
    parser.add_argument("-p", "--pkgid", help="Package ID.")
    parser.add_argument("-v", "--verbose", help="Log level to DEBUG.",
            action="store_true")
    args = parser.parse_args()

    if (args.verbose):
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    config_file = args.config
    error = False
    if not config_file:
        logger.error("Configuration file is required.")
        error = True
    else:
        config = configparser.ConfigParser()
        config.read(config_file)

    pkgid = args.pkgid

    if not error:
        # XXX: Note logic negation of --album. Command-line semantics are more
        # clearly expressed this way.
        logger.warn("Working in album directory: {}".format(args.album))
        if pkgid:
            package = get_package(config, pkgid, not args.album)
            mk_db_template(config, package, not args.album)
        else:
            # Worried about accidental operation on entire Album directory.
            # mk_db_template_album(config, not args.album)
            mk_db_template_album(config)

    if error:
        parser.usage_message()
        sys.exit(1)


if __name__ == '__main__': # pragma no cover
    main()
