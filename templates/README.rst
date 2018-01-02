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

TODO: Currently the background image is not used. Stay tuned.


Editing the Templates
---------------------

The templates must be edited inside the shell scripts. Once the changes are
complete, rebuild the templates as described in the first paragraph above.


Stylesheets
-----------

Stylesheets are implemented using Stylus. Install Stylus locally not
globally::

    npm install stylus

That is all. The CSS files will be built as needed during template creation
and deleted when complete.

Some rudimentary support for theme is contained in ``values.styl``. Change
those values as needed.


Footer
------

Just so I don't forget, the footer was implemented using  excellent pattern
from `Stackoverflow`_


.. _Jinja2: http://jinja.pocoo.org/
.. _Matthew James Taylor: http://matthewjamestaylor.com/blog/keeping-footers-at-the-bottom-of-the-page
.. _Stackoverflow: https://stackoverflow.com/questions/7123138/how-to-make-this-header-content-footer-layout-using-css
