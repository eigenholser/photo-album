#/bin/sh
#
# Create gallery view template.

wipdir=${0%%mkgallerytemplate.sh}

#<html>
#  <head>
#    <meta http-equiv="content-type" content="text/html; charset=UTF-8">
#
#    <!-- Enable responsive view on mobile devices -->
#    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
#
#    <title>{{ pkgid }}</title>
#
#    <style type="text/css">

cat <<CSS1
{% extends "base.html" %}
{% block style_gallery %}
    <style type="text/css">
CSS1

$wipdir/mkgallerycss.sh | sed -e 's/^/        /'

cat <<BODY1
    </style>
{% endblock style_gallery %}
{% block body %}
  <body class="no-touch">
{% endblock body %}
{% block title_td %}
          <td class="title">
            <h1>{{ pkgid }}</h1>
            <p><a href="../contents.html">Table of Contents</a> -
            <a href="detail.html" title="{{ pkgid }}">Package Details</a></p>
          </td>
{% endblock title_td %}
{% block content %}

    <h2>Description</h2>
    <div class="description">
      {% for paragraph in package["description"] %}
      <p>{{ paragraph }}</p>
      {% endfor %}
    </div>

    <div class="wrap">

      <!-- Define all of the tiles: -->
      {% for photoid in photographs.keys() %}
      <div class="box">
        <div class="boxInner">
          <a href="jpeg/{{ photographs[photoid]["filename"] }}"><img src="thumbs/{{ photographs[photoid]["filename"] }}" /></a>
          <div class="titleBox">{{ photoid }}</div>
        </div>
      </div>
      {% endfor %}

    </div> {# <!-- /#wrap --> #}

    <p>&nbsp;</p>
{% endblock content %}
BODY1
