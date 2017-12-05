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

cat <<BODY1
    </style>
  </head>

  <body class="no-touch">

    <table class="heading">
      <tr>
        <td class="title">
          <h1>{{ pkgid }}</h1>
          <p><a href="../contents.html">Table of Contents</a> -
          <a href="detail.html" title="{{ pkgid }}">Package Details</a></p>
        </td>
        <td class="logo">
BODY1

# This mess does a nice job at creating the logo img tag from external base64.
echo -n "<img alt=\"Logo Image\" height=\"92\" src=\"data:image/png;base64,"
cat logo-base64.txt | tr '\n' '\"'
echo " />"

cat <<BODY2
        </td>
      </tr>
    </table>

    <div class="description">
      <p>{{ package["description"] }}</p>
    </div>

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
BODY2
