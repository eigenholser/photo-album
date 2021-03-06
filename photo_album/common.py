import os
import re
import sqlite3


class AlbumBase(object):
    """
    Common code.
    """

    def __init__(self, config):
        build_dir = config.get('album', 'build_directory')
        db_file = config.get('album', 'album_database')
        self.conn = sqlite3.connect(db_file)

    def split_description(self, description):
        """
        Split description on linefeeds into list so we can have paragraphs.
        """
        # Replace two newlines with possible whitespace with single newline.
        # TODO: What about 3 or more newlines?
        paragraphs = re.sub(r'\s*\n\s*\n\s*', '\n', description)
        return paragraphs.splitlines()

