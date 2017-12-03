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
from photo_album import (ArchiveContents, PackageContents, CustomArgumentParser)


logger = logging.getLogger(__name__)


def mk_archive_contents(config):
    contents = ArchiveContents(config)
    build_dir = config.get('album', 'build_directory')
    dist_dir = config.get('album', 'dist_directory')
    template_dir = "{}/templates".format(build_dir)
    contents_title = config.get('album', 'title')
    env = Environment(
        loader=PackageLoader("photo_album", package_path="templates"),
        autoescape=select_autoescape(['html'])
    )
    template_vars = {
        "title": contents_title,
        "packages": contents,
    }

    template = env.get_template('contents.html')

    logger.info("Writing /contents.html")
    with open(os.path.join(dist_dir, 'contents.html'), 'w') as f:
        f.write(template.render(template_vars))


def mk_package_contents(config):
    packages = ArchiveContents(config)
    build_dir = config.get('album', 'build_directory')
    dist_dir = config.get('album', 'dist_directory')
    template_dir = "{}/templates".format(build_dir)

    for package in packages.keys():
        contents = PackageContents(config, package)

        env = Environment(
            loader=PackageLoader("photo_album", package_path="templates"),
            autoescape=select_autoescape(['html'])
        )

        template_vars = {
            "pkgid": package,
            "photographs": contents,
            "package": packages[package],
        }

        detail_template = env.get_template('detail.html')
        gallery_template = env.get_template('gallery.html')

        logger.info("Writing package {}/detail.html".format(package))
        with open(os.path.join(dist_dir, package, 'detail.html'), 'w') as f:
            f.write(detail_template.render(template_vars))

        logger.info("Writing package {}/gallery.html".format(package))
        with open(os.path.join(dist_dir, package, 'gallery.html'), 'w') as f:
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
