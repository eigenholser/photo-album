#!/bin/sh
#
# Create faq template.

wipdir=${0%%mkfaqtemplate.sh}

cat <<BODY
{% extends "base.html" %}
{% block title %}
            <h1>{{ title }}</h1>
{% endblock title %}
{% block content %}
    <p><a href="contents.html">Table of Contents</a>

    <h1>Frequently Asked Questions</h1>

    <h3>How do I print the photographs?</h3>

    <p>The full-size photographs are displayed in the browser when the gallery
    thumbnail or detail view photograph ID link is clicked. Those images may
    be copied to external media or uploaded to a printing service.</p>

    <p>The full-size photographs are located in the album directory in the
    package folder. The JPEG files may be copied directly from that location
    or saved directly from the web browser.</p>

    <h3>Can I enhance or edit the photographs?</h3>

    <p>Yes but with some <i>caveats</i>.
    Never ever edit the original scanned images cross my heart, hope to die!.
    Those are the master copies. Make a copy first and edit that.</p>

    <p>
    Also <i>important</i>.
    Edit the TIFF files because they do not lose fidelity when editing like
    JPEG files. Once the photograph has been enhanced, cropped, then convert
    it to JPEG for printing.</p>

{% endblock content %}
BODY
