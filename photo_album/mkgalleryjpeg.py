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
from photo_album import (Album, Package, CustomArgumentParser, GalleryImage)


logger = logging.getLogger(__name__)


def mk_gallery_jpeg_album(config, build=True):
    """
    Process all packages in album from work or album directory.
    """
    work_dir = get_work_dir(config, build)
    packages = Album(config, build)

    for pkgid in packages.keys():
        mk_gallery_jpeg(config, pkgid, build)


def mk_gallery_jpeg(config, pkgid, build=True):
    """
    Convert cropped TIFF images to JPEG with gallery size.
    """
    work_dir = get_work_dir(config, build)

    package = Package(config, pkgid, build)
    pkg_dir = os.path.join(work_dir, pkgid)
    gallery_tiff_dir = config.get('album', 'gallery_tiff_directory')
    gallery_jpeg_dir = config.get('album', 'gallery_jpeg_directory')
    gallery_thumb_dir = config.get('album', 'gallery_thumb_directory')
    gallery_tiff_path = os.path.join(pkg_dir, gallery_tiff_dir)
    gallery_jpeg_path = os.path.join(pkg_dir, gallery_jpeg_dir)
    gallery_thumb_path = os.path.join(pkg_dir, gallery_thumb_dir)

    if not os.path.exists(pkg_dir):
        logger.error("Invalid package directory: {}".format(pkg_dir))
        sys.exit(1)

    # Create both directories as needed.
    pathlib.Path(gallery_jpeg_path).mkdir(parents=True, exist_ok=True)
    pathlib.Path(gallery_thumb_path).mkdir(parents=True, exist_ok=True)

    for photoid in package.keys():
        source_photo = os.path.join(
                gallery_tiff_path, '{}.tif'.format(photoid))
        gallery_jpeg_photo = os.path.join(
                gallery_jpeg_path, '{}.jpg'.format(photoid))
        gallery_thumb_photo = os.path.join(
                gallery_thumb_path, '{}.jpg'.format(photoid))
        im = Image.open(source_photo)
        gallery_thumb_height = int(
                config.get('album', 'gallery_thumb_height'))
        thumb_scale_factor = compute_scale_factor(
                gallery_thumb_height, im.size)

        # Normalize the TIFF image if necessary.
        norm_img = GalleryImage(config, source_photo, source_photo)
        norm_img.normalize_tiff()

        jpeg_cmd = ['convert', '{source}'.format(source=source_photo),
                '{target}'.format(target=gallery_jpeg_photo)]
        thumb_cmd = ['convert', '-resize',
                '{scale}%'.format(scale=thumb_scale_factor),
                '{source}'.format(source=source_photo),
                '{target}'.format(target=gallery_thumb_photo)]
        logger.debug("{}".format(jpeg_cmd))
        logger.info("Creating gallery JPEG {}.jpg".format(photoid))
        # XXX: Intentionally not handling exception if subprocess fails.
        if os.path.exists(gallery_jpeg_photo):
            logger.info("File exists. Skipping {}".format(gallery_jpeg_photo))
        else:
            run = subprocess.run(jpeg_cmd, stdout=subprocess.PIPE, check=True)

        logger.debug("{}".format(thumb_cmd))
        logger.info(
            "Creating gallery thumbnail JPEG {}.jpg with scaling {:3.2f}%".format(
            photoid, thumb_scale_factor))
        # XXX: Intentionally not handling exception if subprocess fails.
        if os.path.exists(gallery_thumb_photo):
            logger.info("File exists. Skipping {}".format(gallery_jpeg_photo))
        else:
            run = subprocess.run(
                thumb_cmd, stdout=subprocess.PIPE, check=True)


def compute_scale_factor(height, size):
    """
    Compute gallery conversion scale factor as a percentage.
    """
    landscape = True
    source_width = size[0]
    source_height = size[1]
    if source_width < source_height:
        landscape = False
    if landscape:
        return height/source_height * 100
    return height/source_width * 100


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
            mk_gallery_jpeg(config, pkgid, not args.album)
        else:
            # Worried about accidental operation on entire Album directory.
            # mk_gallery_jpeg_album(config, not args.album)
            mk_gallery_jpeg_album(config)

    if error:
        logger.error("Exiting due to errors.")
        parser.usage_message()
        sys.exit(1)


if __name__ == '__main__': # pragma no cover
    main()
