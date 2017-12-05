#!/bin/sh
#
# Create content view template.

wipdir=${0%%mkcontentstemplate.sh}

cat <<HEAD
<html>
  <head>
    <title>{{ title }}</title>
    <style type="text/css">
HEAD

# CSS inline
cat "$wipdir/index.css" | sed -e 's/^/      /'

cat <<BODY1
    </style>
  </head>

  <body>

    <table class="heading">
      <tbody>
        <tr>
          <td class="title">
            <h1>{{ title }}</h1>
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
      </tbody>
    </table>

    <h2>Table of Contents</h2>

    <table class="contents">

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
BODY2
