import os


class PhotographsList(object):
    """
    Build a list of photographs from the package  directory.
    """

    def __init__(self, config, package):
        dist_dir = config.get('album', 'dist_directory')
        self.photographs_list(dist_dir, package)

    def __iter__(self):
        for photo in self.photographs:
            yield photo

    def photographs_list(self, dist_dir, package):

        file_list = self.photographs_list = sorted(
            [file for file in os.listdir(
                    os.path.join(dist_dir, package, 'jpeg'))
                if not os.path.isdir(os.path.join(dist_dir, package, file))])

        self.photographs = [
            file for file in file_list if os.path.splitext(file)[1] == ".jpg"]
