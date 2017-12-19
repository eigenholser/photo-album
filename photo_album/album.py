import os
import re
import sqlite3
from photo_album.common import AlbumBase


class Album(AlbumBase):
    """
    All packages in the album.
    """
    def __init__(self, config):
        self.get_packages_on_disk(config)
        self.packages = {k: {} for k in self.package_list}

        super().__init__(config)
        self.album_description()
        self.package_description()

    def album_description(self):
        """
        Retrieve album description from database.
        """
        query = "SELECT * FROM albums"
        self.conn.row_factory = sqlite3.Row
        cur = self.conn.cursor()
        cur.execute(query)
        row = cur.fetchone()
        self.title = row["albumid"]
        self.description = self.split_description(row["description"])

    def package_description(self):
        """
        """
        query = "SELECT * FROM packages WHERE pkgid IN ({})".format(
                ','.join('?'*len(self.packages)))
        self.conn.row_factory = sqlite3.Row
        cur = self.conn.cursor()
        cur.execute(query, self.package_list)
        rows = cur.fetchall()
        row_list = [
            'pkgid', 'pkg_date', 'location', 'subjects', 'media_type',
            'media_fmt', 'media_status', 'film', 'sequence', 'frames',
            'pieces', 'sheets', 'set_datetime', 'interval', 'description'
        ]

        for pkg in rows:
            for row_name in row_list:
                if row_name == "description":
                    self.packages[pkg["pkgid"]][row_name] = \
                            self.split_description(pkg[row_name])
                else:
                    self.packages[pkg["pkgid"]][row_name] = pkg[row_name]

    def keys(self):
        return sorted([pkgid for pkgid in self.packages.keys()])

    def __getitem__(self, key):
        # TODO: validate and raise IndexError, TypeError, KeyError as needed.
        return self.packages[key]

    def get_packages_on_disk(self, config):
        """
        Read packages present in album directory on disk.
        """
        dist_dir = config.get('album', 'dist_directory')

        self.package_list = sorted([file for file in os.listdir(dist_dir)
                if os.path.isdir(os.path.join(dist_dir, file))])
