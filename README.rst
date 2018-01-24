Photo Album
===========

The photo album paradigm is *album* and *package*. A package is a collection
of related photos. This could be a roll of film, an event, or just a trunk
full of old photos you've scanned. The definition is arbitrary; but broadly
is just a bunch of photographs you've decided to group for whatever reason.
An album is a collection of *packages*.

The purpose of the ``photo_album`` application is to generate an HTML
*table of contents* for the entire album as well as a *thumbnail gallery* and
*detail view* for each package. The information needed to generate the HTML
files is gathered from an SQLite database by reading the album and package
directory contents

The `database schema`_ is in the ``database`` directory. It is a simple two-table
structure that defines a one-to-many relationship between packages and
photographs. Taken together, this database constitutes the album.

The configuration file ``album.cfg`` must be configured properly. The database
must be created. Currently there no import functionality so you'll be enjoying
some quality time with SQLite SQL92 syntax.


Installation
------------

This is a work in progress. Install::

    mkvirtualenv --python=python3 photo_album
    pip install -r requirements.txt
    python setup.py develop


Invoking
--------

The application consists of several console scripts that perform distinct
operations on packages in the album.::

    mkcontents
    mkdbtemplate
    mkgallerytiff
    mkgalleryjpeg
    mkgallerycaption

`mkdbtemplate` produces database schema for each package to be used for
populating the database for that package. It also has some facility for
doing DB migrations as schema changes occur. It serves as a replacement for a
front-end and will do nicely for now.

`mkgallerytiff` copies original TIFF images from the `tiff` directory into the
`gallery-tiff` directory. If there is a `crop` value present in the database,
the image will be cropped as described. Note that if cropping occurs,
`mkdbtemplate` must be run again to capture the new crop marks. The SQL must
also be invoked again to populate the database.

Manual cropping must be performed after this console script has been run. This
is not true if `mkgallerytiff` is being run after a previous crop and the new
cropping is done automatically.

`mkgalleryjpeg` converts the cropped TIFF images to JPEG with no scaling. These
are suitable for producing prints. This command will also produce the
thumbnails needed for the thumbnail gallery.

`mkgallerycaption` processes the cropped gallery TIFF images to JPEG and places
the photo ID as a caption on the image. The resolution is the same as the
gallery TIFF images. These images are suitable for a printed index.

`mkcontents` combines packages it finds on the filesystem with data from the
database and produces an album table of contents and for each package produces
a thumbnail gallery and detail view. This command must be run last once all
the previous processing steps have been performed.

Run the application like this::

    mkcontents --config album.cfg


Editing and Building the Templates
----------------------------------

See the `README in the templates directory`_ for details.

.. _database schema: database/
.. _README in the templates directory: templates/
.. _Make <h1> Vertically Center with CSS: https://stackoverflow.com/a/29504662
.. _How to align an image side by side with a heading element?: https://stackoverflow.com/a/29504662
.. _How to make this Header/Content/Footer layout using CSS?: https://codepen.io/enjikaka/pen/zxdYjX
.. _Anser to question #7123138 on Stack Overflow: https://codepen.io/enjikaka/pen/zxdYjX
.. _Creating Responsive Tiled Layout with Pure CSS: http://www.dwuser.com/education/content/creating-responsive-tiled-layout-with-pure-css/
.. _Thumbnail Gallery Example: http://output.jsbin.com/aseram/1
.. _Thumbnail Gallery JSbin: http://jsbin.com/dewuhewari/edit?html,output

