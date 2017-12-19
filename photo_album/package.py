import os
import sqlite3
from photo_album.common import AlbumBase

class Package(AlbumBase):
    """
    Contents of the package with metadata.
    """

    def __init__(self, config, pkgid):
        self.pkgid = pkgid
        dist_dir = config.get('album', 'dist_directory')
        self.photographs_on_disk(dist_dir, pkgid)
        self.contents = {
            os.path.splitext(k)[0]: {
                "filename": k,
                "description": '',
            } for k in self.photographs
        }

        super().__init__(config)
        self.photograph_description()

    def photograph_description(self):
        """
        Get description for each photograph.
        """
        query = "SELECT * FROM photographs WHERE pkgid=?"
        self.conn.row_factory = sqlite3.Row
        cur = self.conn.cursor()
        cur.execute(query, (self.pkgid,))
        rows = cur.fetchall()
        for photo in rows:
            self.contents[photo["photoid"]]["description"] = \
                    photo["description"]

    def keys(self):
        return sorted([photoid for photoid in self.contents.keys()])

    def __getitem__(self, key):
        # TODO: validate and raise IndexError, TypeError, KeyError as needed.
        return self.contents[key]

    def photographs_on_disk(self, dist_dir, pkgid):
        """
        Read list of photographs from package on disk.
        """
        file_list = self.photographs_list = sorted(
            [file for file in os.listdir(
                    os.path.join(dist_dir, pkgid, 'jpeg'))
                if not os.path.isdir(os.path.join(dist_dir, pkgid, file))])

        self.photographs = [
            file for file in file_list if os.path.splitext(file)[1] == ".jpg"]
