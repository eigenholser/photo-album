#!/bin/sh
#
# Create content view template.

wipdir=${0%%mkcontentstemplate.sh}

cat <<CONTENT
{% extends "base.html" %}
{% block title_td %}
          <td class="title">
            <h1>{{ title }}</h1>
          </td>
{% endblock title_td %}
{% block content %}
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
          {# Don't implement paragraphs here. Just join the text. #}
          <td>{% for paragraph in packages[package]["description"] %}{{ paragraph }}&nbsp;{% endfor %}</td>
        </tr>
      {% endfor %}

      </tbody>
    </table>
{% endblock content %}
CONTENT
