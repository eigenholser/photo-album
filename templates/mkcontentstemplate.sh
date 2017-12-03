#!/bin/sh
#
# Process CONTENTS.md to HTML.

wipdir=${0%%mkcontentstemplate.sh}

cat <<HEAD
<html>
  <head>
    <title>{{ title }}</title>

    <style>
HEAD

# CSS inline
cat "$wipdir/index.css" | sed -e 's/^/      /'

cat <<FOOT
    </style>
  </head>

  <body>

    <h1>Table of Contents</h1>

    <p>{{ title }}</p>

    <table border="1" class="contents">

      <thead>
        <tr>
          <th class="packageid">Package ID</th>
          <th class="description">Description</th>
        </tr>
      </thead>

      <tbody>

      {% for package in packages.keys() %}
        <tr>
          <td><a href="{{ package }}/gallery.html" title="{{ package }}">{{ package }}</a></td>
          <td>{{ packages[package]["description"] }}</td>
        </tr>
      {% endfor %}
      </tbody>
    </table>

  </body>
</html>
FOOT
