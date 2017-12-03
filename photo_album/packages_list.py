import os


class PackagesList(object):
    """
    Build a list of packages from the distribution directory.
    """

    def __init__(self, config):
        dist_dir = config.get('album', 'dist_directory')

        self.packages_list = sorted([file for file in os.listdir(dist_dir)
                if os.path.isdir(os.path.join(dist_dir, file))])

    def __iter__(self):
        for pkg in self.packages_list:
            yield pkg
