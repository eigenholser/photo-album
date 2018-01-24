#!/bin/sh
#
# Create detail view template.

wipdir=${0%%mkdetailtemplate.sh}

cat <<BODY
{% extends "base.html" %}
{% block title %}
            <h1>{{ pkgid }}</h1>
{% endblock title %}
{% block content %}
    <p><a href="../contents.html">Table of Contents</a> -
    <a href="gallery.html" title="{{ pkgid }}">Thumbnail Gallery</a></p>

    <h2>Description</h2>
    <div class="description">
      {% for paragraph in package["description"] %}
      <p>{{ paragraph|safe }}</p>
      {% endfor %}
    </div>

    <h2>Contents</h2>
    <table class="contents">

      <thead>
        <tr>
          <th class="photoid" >Photograph ID</th>
          <th class="detail-poi">*</th>
          <th class="notes">Description</th>
        </tr>
      </thead>

      <tbody>

      {% for photoid in photographs.keys() %}
        <tr>
          <td><a href="jpeg/{{ photographs[photoid]["filename"] }}" title="{{ photographs[photoid]["description"] }}">{{ photoid }}</a></td>
          <td>{% if photographs[photoid]["poi"] == 1 %}*{% else %}&nbsp;{% endif %}</td>
          <td>{{ photographs[photoid]["description"] }}</td>
        </tr>
      {% endfor %}

      </tbody>
    </table>

    <p>&nbsp;</p>

    <h2>Metadata</h2>

    <table border="1" class="metadata">
      <tr>
        <td class="metakey">Date</td>
        <td class="metaval">{{ package["pkg_date"] }}</td>
      </tr>
      <tr>
        <td class="metakey">Location</td>
        <td>{{ package["location"] }}</td>
      </tr>
      <tr>
        <td class="metakey">Subjects</td>
        <td>{{ package["subjects"] }}</td>
      </tr>
      <tr>
        <td class="metakey">Media Type</td>
        <td>{{ package["media_type"] }}</td>
      </tr>
      <tr>
        <td class="metakey">Media Format</td>
        <td>{{ package["media_fmt"] }}</td>
      </tr>
      <tr>
        <td class="metakey">Media Status</td>
        <td>{{ package["media_status"] }}</td>
      </tr>
      <tr>
        <td class="metakey">Film</td>
        <td>{{ package["film"] }}</td>
      </tr>
      <tr>
        <td class="metakey">Sequence</td>
        <td>{{ package["sequence"] }}</td>
      </tr>
      <tr>
        <td class="metakey">Frames</td>
        <td>{{ package["frames"] }}</td>
      </tr>
      <tr>
        <td class="metakey">Pieces</td>
        <td>{{ package["pieces"] }}</td>
      </tr>
      <tr>
        <td class="metakey">Sheets</td>
        <td>{{ package["sheets"] }}</td>
      </tr>
      <tr>
        <td class="metakey">Set Datetime</td>
        <td>{{ package["set_datetime"] }}</td>
      </tr>
      <tr>
        <td class="metakey">Interval Datetime</td>
        <td>{{ package["interval"] }}</td>
      </tr>
    </table>
    <p>&nbsp;<p>
{% endblock content %}
BODY
