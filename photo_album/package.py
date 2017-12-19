import os
import sqlite3
from photo_album.photographs_list import PhotographsList
from photo_album.common import AlbumBase

class Package(object):
    """
    Contents of the package with metadata.
    """

    def __init__(self, config, package):
        self.package = package
        self.photos = [photo for photo in PhotographsList(config, package)]
        self.contents = {
            os.path.splitext(k)[0]: {
                "filename": k,
                "description": '',
            } for k in self.photos
        }

        build_dir = config.get('album', 'build_directory')
        db_file = config.get('album', 'packages_database')
        db_dir = "{}/database".format(build_dir)
        self.conn = sqlite3.connect(os.path.join(db_dir, db_file))
        self.photograph_description()

    def photograph_description(self):
        """
        Get description for each photograph.
        """
        query = "SELECT * FROM photographs WHERE pkgid=?"
        self.conn.row_factory = sqlite3.Row
        cur = self.conn.cursor()
        cur.execute(query, (self.package,))
        rows = cur.fetchall()
        for photo in rows:
            self.contents[photo["photoid"]]["description"] = \
                    photo["description"]

    def keys(self):
        return sorted([photoid for photoid in self.contents.keys()])

    def __getitem__(self, key):
        # TODO: validate and raise IndexError, TypeError, KeyError as needed.
        return self.contents[key]

    def photographs_on_disk(self, dist_dir, package):
        """
        Read list of photographs from package on disk.
        """
        file_list = self.photographs_list = sorted(
            [file for file in os.listdir(
                    os.path.join(dist_dir, package, 'jpeg'))
                if not os.path.isdir(os.path.join(dist_dir, package, file))])

        self.photographs = [
            file for file in file_list if os.path.splitext(file)[1] == ".jpg"]
