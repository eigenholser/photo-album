import os
import re
import sqlite3
from photo_album.common import AlbumBase


class Album(AlbumBase):
    """
    All packages in the album.
    """
    def __init__(self, config, build=True):
        if build:
            work_dir = config.get('album', 'build_directory')
        else:
            work_dir = config.get('album', 'album_directory')

        package_list = self.get_packages_on_disk(work_dir)
        self.packages = {k: {} for k in package_list}

        super().__init__(config)
        self.album_description()
        self.package_description(package_list)

        # If packages do not exist in database, we must use dummy key/val so
        # next step does not break. You'll need to manually edit the DB files
        # later to set the sequence like you want.
        for key, val in self.packages.items():
            if not "pkgid" in val:
                val["pkgid"] = key
            if not "sequence" in val:
                val["sequence"] = 1

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

    def package_description(self, package_list):
        """
        Fetch package metadata for each package. Stash the data so it is
        available as a dict on the object.
        """
        query = "SELECT * FROM packages WHERE pkgid IN ({})".format(
                ','.join('?'*len(self.packages)))
        self.conn.row_factory = sqlite3.Row
        cur = self.conn.cursor()
        cur.execute(query, package_list)
        rows = cur.fetchall()
        row_list = [
            'pkgid', 'sequence', 'pkg_date', 'location', 'subjects',
            'media_type', 'media_fmt', 'media_status', 'film', 'nonce',
            'frames', 'pieces', 'sheets', 'set_datetime', 'interval',
            'description'
        ]

        for pkg in rows:
            for row_name in row_list:
                if row_name == "description":
                    self.packages[pkg["pkgid"]][row_name] = \
                            self.split_description(pkg[row_name])
                else:
                    self.packages[pkg["pkgid"]][row_name] = pkg[row_name]

    def keys(self):
        # Sort pkgid's on pkgid then sequence of packages table. This is a two
        # step sort. Sort on sequence numbers. If the sequence numbers are the
        # same, then sort on pkgid.
        secondary_sort = sorted(
                self.packages.values(), key=lambda pkg: pkg["pkgid"])
        primary_sort = [package["pkgid"] for package in
                sorted(secondary_sort, key=lambda pkg: int(pkg["sequence"]))]
        return primary_sort

    def __getitem__(self, key):
        # TODO: validate and raise IndexError, TypeError, KeyError as needed.
        return self.packages[key]

    def get_packages_on_disk(self, work_dir):
        """
        Read packages present in album directory on disk.
        """
        package_list = sorted([file for file in os.listdir(work_dir)
                if os.path.isdir(os.path.join(work_dir, file))])

        for pkgid in [x for x in package_list]:
            if not self.is_package_dir(work_dir, pkgid):
                package_list.remove(pkgid)

        return package_list

    def is_package_dir(self, work_dir, pkgid):
        """
        Inspect package directory to see if it looks like a package directory.
        That means it will have a `jpeg' and a `tiff' directory inside.

        TODO: Is there a better way?
        """
        ls_pkg_dir = os.listdir(os.path.join(work_dir, pkgid))
        # TODO: Maybe these could be in the configuration file?
        if 'tiff' in ls_pkg_dir and 'jpeg' in ls_pkg_dir:
            return True
        return False


