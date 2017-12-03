#/bin/sh
#
# Create GALLERY.html file in it's entirety.

wipdir=${0%%mkgallerytemplate.sh}

cat <<HEAD
<html>
  <head>
    <meta http-equiv="content-type" content="text/html; charset=UTF-8">

    <!-- Enable responsive view on mobile devices -->
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />

    <title>{{ pkgid }}</title>

    <style type="text/css">
HEAD

cat "$wipdir/gallery.css" | sed -e 's/^/        /'
cat "$wipdir/index.css" | sed -e 's/^/        /'

cat <<BODY
    </style>
  </head>

  <body class="no-touch">

    <h1>{{ pkgid }}</h1>

    <p><a href="../contents.html">Table of Contents</a> -
    <a href="detail.html">Package Details</a></p>

    <div class="wrap">

      <!-- Define all of the tiles: -->
      {% for photoid in photographs.keys() %}
      <div class="box">
        <div class="boxInner">
          <a href="jpeg/{{ photographs[photoid]["filename"] }}"><img src="thumbs/{{ photographs[photoid]["filename"] }}" /></a>
          <div class="titleBox">thumbs/{{ photographs[photoid]["filename"] }}</div>
        </div>
      </div>
      {% endfor %}

    </div>
    <!-- /#wrap -->

  </body>
</html>
BODY
