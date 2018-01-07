import configparser
from jinja2 import (Environment, FileSystemLoader, PackageLoader,
        select_autoescape)
import logging
import os
import pathlib
from PIL import Image
import re
import sqlite3
import stat
import subprocess
import sys
from photo_album import (Album, Package, CustomArgumentParser)


logger = logging.getLogger(__name__)


def mk_gallery_tiff_album(config, build=True):
    """
    Process all packages in album from work or album directory.
    """
    work_dir = get_work_dir(config, build)
    packages = Album(config, build)

    for pkgid in packages.keys():
        mk_gallery_tiff(config, pkgid, build)


def mk_gallery_tiff(config, pkgid, build=True):
    """
    Convert TIFF images to gallery size.
    """
    build_dir = config.get('album', 'build_directory')

    package = Package(config, pkgid, build)
    pkg_dir = os.path.join(build_dir, pkgid)
    source_dir = os.path.join(pkg_dir, "tiff")
    gallery_dir = os.path.join(pkg_dir, "gallery-tiff")

    if not os.path.exists(pkg_dir):
        logger.error("Invalid package directory: {}".format(pkg_dir))
        sys.exit(1)

    pathlib.Path(gallery_dir).mkdir(parents=True, exist_ok=True)

    for photoid in package.keys():
        source_photo = os.path.join(source_dir, '{}.tif'.format(photoid))
        target_photo = os.path.join(gallery_dir, '{}.tif'.format(photoid))
        im = Image.open(source_photo)
        scale_factor = compute_scale_factor(config, im.size)
        logger.debug("({}x{}) [{}] {}".format(
            im.size[0], im.size[1], scale_factor, photoid))
        resize_cmd = "convert -resize {scale}% {source} {target}".format(
                scale=scale_factor, source=source_photo, target=target_photo)
        logger.info(
            "Creating gallery TIFF {}.tif with scaling {:3.2f}%".format(
            photoid, scale_factor))
        run = subprocess.run(resize_cmd.split(), stdout=subprocess.PIPE)
        # TODO: Check exec status

        # TODO: Refactor this to be functional'ish.
        crop = get_crop(package, photoid)
        if crop:
            logger.debug(
                "Crop marks already recorded. Checking for proper scaling.")
            gallery_height = int(config.get('album', 'gallery_height'))
            if crop[0] != gallery_height:
                logger.warn("Scaling not correct. Rescaling.")
                scale_factor = compute_scale_factor(
                        config, (int(crop[0]), int(crop[1],)))
                logger.debug("Computed new scale factor {:3.2f}".format(
                    scale_factor))
                new_crop = (int((crop[0] * scale_factor)/100),
                    int((crop[1] * scale_factor)/100),
                    int((crop[2] * scale_factor)/100),
                    int((crop[3] * scale_factor)/100),)
                logger.warn("New crop marks: {}x{}+{}+{}".format(*new_crop))
                crop_cmd = \
                    "convert -crop {}x{}+{}+{} {source} {target}".format(
                    *new_crop, source=target_photo, target=target_photo)
                logger.warn(crop_cmd)
                run = subprocess.run(crop_cmd.split(), stdout=subprocess.PIPE)
                # TODO: Check exec status


def compute_scale_factor(config, size):
    """
    Compute gallery conversion scale factor as a percentage.
    """
    landscape = True
    gallery_height = int(config.get('album', 'gallery_height'))
    source_width = size[0]
    source_height = size[1]
    if source_width < source_height:
        landscape = False
    if landscape:
        return gallery_height/source_height * 100
    return gallery_height/source_width * 100


def get_crop(package, photoid):
    """
    Return existing convert crop marks from DB as tuple or None if not yet
    recorded.
    """
    query = "SELECT crop FROM photographs WHERE photoid=?"
    cur = package.conn.cursor()
    cur.execute(query, (photoid,))
    row = cur.fetchone()
    if row:
        logger.debug("{}: {}".format(photoid, row['crop']))
        match = re.search(r'(\d+)x(\d+)\+(\d+)\+(\d+)', row['crop'])
        if match:
            crop = (int(match.group(1)), int(match.group(2)),
                    int(match.group(3)), int(match.group(4)))
            return crop
    return None


def get_work_dir(config, build):
    """
    Get work directory.
    """
    if build:
        return config.get('album', 'build_directory')
    else:
        return config.get('album', 'album_directory')


def main():
    """
    Parse command-line arguments. Initiate file processing.
    """
    parser = CustomArgumentParser()
    parser.add_argument("-a", "--album",
            help="Work in album directory. Danger!", action="store_true")
    parser.add_argument("-c", "--config", help="Configuration file.")
    parser.add_argument("-p", "--pkgid", help="Package to work on.")
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
            mk_gallery_tiff(config, pkgid, not args.album)
        else:
            mk_gallery_tiff_album(config, not args.album)

    if error:
        logger.warn("Not yet implemented.")
        parser.usage_message()
        sys.exit(1)

if __name__ == '__main__': # pragma no cover
    main()
