#import argparse
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


logger = logging.getLogger(__name__)


def mk_db_template(config):
    packages = Album(config)
    build_dir = config.get('album', 'build_directory')
    album_dir = config.get('album', 'album_directory')
    db_dir = config.get('album', 'database_directory')
    template_dir = "{}/templates".format(build_dir)

    for pkgid in packages.keys():
        package = Package(config, pkgid, build=False)

        for photoid in package.keys():
            photo = os.path.join(
                    album_dir, pkgid, 'index/{}.tif'.format(photoid))
            logger.debug("Identifying photograph {}".format(photo))
            run = subprocess.run(['identify', photo], stdout=subprocess.PIPE)
            match = re.search(r'\d+x\d+\+\d+\+\d+', run.stdout.decode("utf-8"))
            if match:
                crop = match.group()
                logger.debug("Found crop marks: {}".format(crop))
                package[photoid]['crop'] = crop

        env = Environment(
            loader=PackageLoader("photo_album", package_path="templates"),
            autoescape=select_autoescape(['sql'])
        )

        template_vars = {
            "pkgid": pkgid,
            "photographs": package,
            "package": packages[pkgid],
        }

        sql_template = env.get_template('PKG-template.sql')

        dbfile = os.path.join(db_dir, 'PKG-{}.sql'.format(pkgid))
        if os.path.isfile(dbfile):
            logger.error(
                    "PKG-{}.sql exists. Performing update.".format(pkgid))
            update(pkgid, package, dbfile)
        else:
            logger.info("Writing package {}.sql".format(pkgid))
            with open(dbfile, 'w') as f:
                f.write(sql_template.render(template_vars))


def update(pkgid, package, dbfile):
    """
    This is a migration and will not be useful once the one-time migration is
    complete.
    """
    with open(dbfile, 'r') as f:
        content = f.readlines()

    pinserts = {}
    cropfmt = """    /* crop */          '{}',\n"""
    for photoid in package.keys():
        for line in [x for x in content]:
            m = re.match(r'INSERT INTO photograph', line)
            if m:
                idx = content.index(line)
                pattern = re.sub(r'\+', '\\+', photoid)
                if (re.search(r'{}'.format(pattern), content[idx + 2])
                        and not re.search(r'crop', content[idx + 3])):
                    pinserts[photoid] = [
                        content[idx + 0],
                        content[idx + 1],
                        content[idx + 2],
                        cropfmt.format(package[photoid]['crop']),
                        content[idx + 3],
                        content[idx + 4],
                        content[idx + 5],
                        content[idx + 6],
                    ]
                    for i in range(7):
                        del content[idx]
                    break

    for photoid in package.keys():
        if photoid in pinserts:
            for line in pinserts[photoid]:
                content.append(line)
        elif pinserts.keys():
            content.append("INSERT INTO photographs VALUES (\n")
            content.append("    /* pkgid */         '{}',\n".format(pkgid))
            content.append("    /* photoid */       '{}',\n".format(photoid))
            content.append("    /* crop */          '{}',\n".format(package[photoid]['crop']))
            content.append("    /* poi */           '0',\n")
            content.append("    /* description */   ''\n")
            content.append(");\n")
            content.append("\n")

    logger.debug("Content line count: {}".format(len(content)))
#   for line in content:
#       print(line.rstrip())

    with open(dbfile, 'w') as f:
        for line in content:
            f.write(line)


def main():
    """
    Parse command-line arguments. Initiate file processing.
    """
    parser = CustomArgumentParser()
    parser.add_argument("-c", "--config",
            help="Configuration file.")
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
        log.error("Configuration file is required.")
        error = True
    else:
        config = configparser.ConfigParser()
        config.read(config_file)

    if not error:
        mk_db_template(config)

    if error:
        logger.warn("Not yet implemented.")
        parser.usage_message()
        sys.exit(1)

if __name__ == '__main__': # pragma no cover
    main()
