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
    work_dir = get_work_dir(config, build)

    package = Package(config, pkgid, build)
    pkg_dir = os.path.join(work_dir, pkgid)
    tiff_source_dir = config.get('album', 'tiff_source_directory')
    gallery_tiff_dir = config.get('album', 'gallery_tiff_directory')
    source_dir = os.path.join(pkg_dir, tiff_source_dir)
    gallery_dir = os.path.join(pkg_dir, gallery_tiff_dir)

    if not os.path.exists(pkg_dir):
        logger.error("Invalid package directory: {}".format(pkg_dir))
        sys.exit(1)

    pathlib.Path(gallery_dir).mkdir(parents=True, exist_ok=True)

    for photoid in package.keys():
        source_photo = os.path.join(source_dir, '{}.tif'.format(photoid))
        target_photo = os.path.join(gallery_dir, '{}.tif'.format(photoid))

        # Necessary for large format photographs.
        Image.MAX_IMAGE_PIXELS = int(1024 * 1024 * 1024)

        im = Image.open(source_photo)

        crop = get_crop(package, photoid)
        scale_factor = None
        if crop:
            # Crop marks recorded from previous processing.
            logger.debug(
                "Crop marks already recorded. Checking for proper scaling.")
            gallery_height = int(config.get('album', 'gallery_height'))
            gallery_width = gallery_height # Yes, we are committing to square.
            if crop[0] != gallery_height:
                logger.warn("Scaling not correct. Rescaling and cropping...")
                scale_factor = compute_scale_factor(
                        config, (int(crop[0]), int(crop[1],)))
                logger.debug("Computed new scale factor {:3.2f}".format(
                    scale_factor))
                new_crop = (gallery_width, gallery_height,
                    int((crop[2] * scale_factor)/100),
                    int((crop[3] * scale_factor)/100),)
                new_crop_str = "{}x{}+{}+{}".format(*new_crop)
                set_crop(package, photoid, new_crop_str)

        if scale_factor is None:
            # Crop marks not previously recorded.
            scale_factor = compute_scale_factor(config, im.size)

        logger.debug("({}x{}) [{}] {}".format(
            im.size[0], im.size[1], scale_factor, photoid))
        resize_cmd = ['convert', '-resize',
                '{scale}%'.format(scale=scale_factor),
                '{source}'.format(source=source_photo),
                '{target}'.format(target=target_photo)]
        if os.path.exists(target_photo):
            logger.info("Target photograph exists. Skipping: {}".format(
                target_photo))
        else:
            logger.info(
                "Creating gallery TIFF {}.tif with scaling {:3.2f}%".format(
                photoid, scale_factor))
            run = subprocess.run(
                    resize_cmd, stdout=subprocess.PIPE, check=True)

        # Resize complete. Crop if previously recorded.
        if crop:
            logger.warn("Scaling as expected. Cropping...")
            crop_str = "{}x{}+{}+{}".format(*crop)
            crop_cmd = ['convert', '-crop', '{}'.format(crop_str),
                    '{source}'.format(source=target_photo),
                    '{target}'.format(target=target_photo)]
            logger.debug(crop_cmd)
            # XXX: Intentionally not handling exception if subprocess
            #      fails.
            run = subprocess.run(
                    crop_cmd, stdout=subprocess.PIPE, check=True)


def compute_scale_factor(config, size):
    """
    Compute gallery conversion scale factor as a percentage.
    """
    landscape = True
    gallery_height = int(config.get('album', 'gallery_height'))
    source_width = size[0]
    source_height = size[1]
    source_ratio = source_width/source_height

    logger.info("Source ratio: {}".format(source_ratio))

    if source_width < source_height:
        landscape = False

    # XXX: Magic number alert.
    # If we have a narrow landscape image, reverse the orientation. Fall
    # through to the landscape == False orientation. Landscape and portrait
    # limits are the inverse of one another - i.e. 3 ~ 0.33

    portrait_scale_factor = gallery_height/source_width * 100
    landscape_scale_factor = gallery_height/source_height * 100

    if landscape:
        if source_ratio < 3:
            return landscape_scale_factor
        else:
            logger.warn(
                "Source ratio == {}. Overriding landscape orientation ".format(
                    source_ratio))
            return portrait_scale_factor

    # portrait == True
    if source_ratio > 0.33:
        return portrait_scale_factor
    else:
        logger.warn(
            "Source ratio == {}. Overriding portrait orientation ".format(
                source_ratio))
        return landscape_scale_factor


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


def set_crop(package, photoid, crop):
    """
    Set new calculated crop value in database on photoid.
    """
    query = "UPDATE photographs SET crop=? WHERE photoid=?"
    cur = package.conn.cursor()
    cur.execute(query, (crop, photoid,))
    package.conn.commit()


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

    error = False

    config_file = args.config
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
            # Worried about accidental operation on entire Album directory.
            # mk_gallery_tiff_album(config, not args.album)
            mk_gallery_tiff_album(config)

    if error:
        logger.error("Exiting due to errors.")
        parser.usage_message()
        sys.exit(1)


if __name__ == '__main__': # pragma no cover
    main()
