Creating the Database
=====================

The SQLite database must be created in the database subdirectory of the
``build_directory`` specified in the ``album.cfg`` file. The ``sqlite3``
utility must be installed::

    sqlite3 myalbum.sqlite < packagedb.sql

Now you can roll up your sleeves and write beautiful SQL to specicfy the
information needed to populate your HTML navigation files for all of the
packages and photographs.

Happily, I've dropped in a template SQL file to get you started. Use one per
package.


Errata
------

You will need to give your packages a name. The package directories must use
the same name as the packages in your database. The directory names will be
used to look up package data from the database.
