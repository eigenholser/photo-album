Modify and Build Jinja2 Templates
=================================

The `Jinja2`_ templates used by ``photo_album`` are built using the shell
scripts in this directory. Building is easy::

    ./mktemplates.sh
    Creating templates...
    index.css
    gallery.css
    base.html
    contents.html
    gallery.html
    detail.htm

The CSS is rebuilt, the templates are built and output into the
``photo_album/templates`` directory where they belong.


Background Pattern and Logo
---------------------------

The background pattern and logo are base64-encoded images. They are generated
using the base64 command::

    base64 -w 0 image.png > logo-base64.txt

Use the ``-w 0`` flag so the base64 is one long line.

The background pattern must be present. A future TODO might be a conditional
to replace it with a background color if the ``background-base64.txt`` file
is empty.

The logo must also be present. The logo height is restricted in the template
image tag to 92 pixels. Size it accordingly when you prepare the logo image.


Editing the Templates and CSS
-----------------------------

The templates must be edited inside the shell scripts. Once the changes are
complete, rebuild the templates as described in the first paragraph above.


.. _Jinja2: http://jinja.pocoo.org/
