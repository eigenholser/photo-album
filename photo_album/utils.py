import argparse
import logging
import sys

def logged_class(cls):
    """
    Class Decorator to add a class level logger to the class with module and
    name.
    """
    cls.logger = logging.getLogger(
            "{0}.{1}".format(cls.__module__, cls.__name__))
    return cls


class CustomArgumentParser(argparse.ArgumentParser): # pragma: no cover
    """
    Custom argparser.
    """
    def error(self, message):
        sys.stderr.write('error: {}\n'.format(message))
        self.print_help()
        sys.exit(2)

    def usage_message(self):
        """
        Print a message and exit.
        """
        sys.stderr.write("error: Missing required arguments.\n")
        self.print_help()
        sys.exit(3)
