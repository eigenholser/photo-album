from __future__ import print_function
import argparse
import configparser
import logging
import os
import pathlib
from PIL import (Image, ImageDraw, ImageFont, ImageEnhance)
import sys
from photo_album import (Album, Package, Caption, CustomArgumentParser)


logger = logging.getLogger(__name__)


def mk_caption_album(config, build=True):
    """
    Process all packages in album from work or album directory.
    """
    work_dir = get_work_dir(config, build)
    packages = Album(config, build)

    for pkgid in packages.keys():
        mk_caption(config, pkgid, build)


def mk_caption(config, pkgid, build=True):
    """
    Create JPEG from gallery TIFF with photoid added as caption.
    """
    work_dir = get_work_dir(config, build)

    package = Package(config, pkgid, build)
    pkg_dir = os.path.join(work_dir, pkgid)
    gallery_tiff_directory = config.get('album', 'gallery_tiff_directory')
    gallery_caption_directory = config.get(
            'album', 'gallery_caption_directory')
    source_dir = os.path.join(pkg_dir, gallery_tiff_directory)
    target_dir = os.path.join(pkg_dir, gallery_caption_directory)

    if not os.path.exists(pkg_dir):
        logger.error("Invalid package directory: {}".format(pkg_dir))
        sys.exit(1)

    pathlib.Path(target_dir).mkdir(parents=True, exist_ok=True)

    for photoid in package.keys():
        source = os.path.join(source_dir, '{}.tif'.format(photoid))
        target = os.path.join(target_dir, '{}.jpg'.format(photoid))
        logger.info("Processing {}".format(source))
        logger.debug("Target is {}".format(target))
        caption = Caption(config, source, target, photoid)


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
    Parse command-line arguments. Process form.
    """
    parser = CustomArgumentParser()
    parser.add_argument("-a", "--album",
            help="Work in album directory. Danger!", action="store_true")
    parser.add_argument("-c", "--config", help="Configuration file.")
    parser.add_argument("-p", "--pkgid", help="Package to work on.")
    parser.add_argument("-v", "--verbose", help="Log level to DEBUG.",
            action="store_true")
    args = parser.parse_args()

    if args.verbose:
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
            mk_caption(config, pkgid, not args.album)
        else:
            mk_caption_album(config, not args.album)

    if error:
        logger.error("Exiting due to errors.")
        parser.usage_message()
        sys.exit(1)


if __name__ == "__main__": # pragma: no cover
    main()

