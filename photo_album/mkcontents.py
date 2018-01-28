#import argparse
import configparser
from jinja2 import (Environment, FileSystemLoader, PackageLoader,
        select_autoescape)
import logging
import os
import re
import sqlite3
import stat
import sys
from photo_album import (Album, Package, CustomArgumentParser)


logger = logging.getLogger(__name__)


def mk_archive_contents(config):
    album = Album(config, False)
    build_dir = config.get('album', 'build_directory')
    album_dir = config.get('album', 'album_directory')
    template_dir = "{}/templates".format(build_dir)
    env = Environment(
        loader=PackageLoader("photo_album", package_path="templates"),
        autoescape=select_autoescape(['html'])
    )

    template_vars = {
        "title": album.title,
        "description": album.description,
        "packages": album
    }

    contents_template = env.get_template('contents.html')
    faq_template = env.get_template('faq.html')

    logger.info("Writing {}/contents.html".format(album_dir))
    with open(os.path.join(album_dir, 'contents.html'), 'w') as f:
        f.write(contents_template.render(template_vars))

    logger.info("Writing {}/faq.html".format(album_dir))
    with open(os.path.join(album_dir, 'faq.html'), 'w') as f:
        f.write(faq_template.render(template_vars))


def mk_package_contents(config):
    packages = Album(config, False)
    build_dir = config.get('album', 'build_directory')
    album_dir = config.get('album', 'album_directory')
    template_dir = "{}/templates".format(build_dir)

    for pkgid in packages.keys():
        package = Package(config, pkgid, build=False)

        env = Environment(
            loader=PackageLoader("photo_album", package_path="templates"),
            autoescape=select_autoescape(['html'])
        )

        template_vars = {
            "pkgid": pkgid,
            "photographs": package,
            "package": packages[pkgid],
        }

        detail_template = env.get_template('detail.html')
        gallery_template = env.get_template('gallery.html')

        logger.info("Writing package {}/detail.html".format(pkgid))
        with open(os.path.join(album_dir, pkgid, 'detail.html'), 'w') as f:
            f.write(detail_template.render(template_vars))

        logger.info("Writing package {}/gallery.html".format(pkgid))
        with open(os.path.join(album_dir, pkgid, 'gallery.html'), 'w') as f:
            f.write(gallery_template.render(template_vars))


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
        mk_package_contents(config)
        mk_archive_contents(config)

    if error:
        logger.warn("Not yet implemented.")
        parser.usage_message()
        sys.exit(1)

if __name__ == '__main__': # pragma no cover
    main()
