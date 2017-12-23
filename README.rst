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
