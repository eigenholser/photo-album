import os
import sqlite3
from photo_album.packages_list import PackagesList

class ArchiveContents(object):
    """
    Complete contents of the distribution archcive.

    TODO: Naming issue here: Archive or Distribution? Both okey?
    """

    def __init__(self, config):
        self.packages = [pkg for pkg in PackagesList(config)]
        self.contents = {k: '' for k in self.packages}
        self.contents = {k: {} for k in self.packages}

        build_dir = config.get('album', 'build_directory')
        db_file = config.get('album', 'packages_database')
        db_dir = "{}/database".format(build_dir)
        self.conn = sqlite3.connect(os.path.join(db_dir, db_file))
        self.package_description()

    def package_description(self):
        """
        """
        query = "SELECT * FROM packages WHERE pkgid IN ({})".format(
                ','.join('?'*len(self.packages)))
        self.conn.row_factory = sqlite3.Row
        cur = self.conn.cursor()
        cur.execute(query, self.packages)
        rows = cur.fetchall()
        row_list = [
            'pkgid', 'pkg_date', 'location', 'subjects', 'media_type',
            'media_fmt', 'media_status', 'film', 'sequence', 'frames',
            'pieces', 'sheets', 'set_datetime', 'interval', 'description'
        ]

        for pkg in rows:
            for row_name in row_list:
                self.contents[pkg["pkgid"]][row_name] = pkg[row_name]

    def keys(self):
        return sorted([pkgid for pkgid in self.contents.keys()])

    def __getitem__(self, key):
        # TODO: validate and raise IndexError, TypeError, KeyError as needed.
        return self.contents[key]
