#!/bin/sh
#
# Create faq template.

wipdir=${0%%mkfaqtemplate.sh}

cat <<BODY
{% extends "base.html" %}
{% block title %}<title>{{ title }}</title>{% endblock title %}
{% block header_label %}<h1>{{ title }}</h1>{% endblock header_label %}
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
    Also <i>important</i>:
    Edit the TIFF files because they do not lose fidelity when editing like
    JPEG files. Once the photograph has been enhanced, cropped, then convert
    it to JPEG for printing.</p>

    <h3>What are all those directories?</h3>

    <p>
    <ul>
        <li><i>tiff</i>: These images are the source of all JPEG images and used for the <i>gallery-tiff</i> directory. The thumbnails used for the gallery thumbnail view were generated from these files. Any edits or enhancements should begin from these TIFF images or the ones in <i>tiff-raw</i> if present.</li>
        <li><i>tiff-raw</i>: Some packages contain this directory. These will be accompanied by a PNM directory as well. These were converted from the PNM files and have not been auto adjusted for white balance. They have an antique look about them that may be desired.</li>
        <li><i>jpeg</i>: Full resoolution JPEG images suitable for printing converted directly from the TIFF images in the <i>tiff</i> directory. Do not edit these. Instead, edit the TIFF images, convert to JPEG for printing.</li>
        <li><i>gallery-tiff</i>: These high resolution images have been reformatted to be square. Some have been cropped. Generally negatives have been cropped while snapshots (prints) have not been cropped. These square formatted TIFF images have been used as the source to generate <i>gallery-jpeg</i>, <i>gallery-thumb</i>, and <i>gallery-caption</i> images.</li>
        <li><i>gallery-jpeg</i>: High resolution JPEG images generated from the <i>gallery-tiff</i> directory.</li>
        <li><i>gallery-thumb</i>: Low resolution images generated from the <i>gallery-tiff</i> directory. These are used in the gallery view.</li>
        <li><i>gallery-caption</i>:High resolution JPEG images generated from the <i>gallery-tiff</i> directory but with the photograph ID overlaid at the bottom in a semi-transparent caption. Intended to be used for a printed index.</li>
        <li><i>pnm</i>: Some photographs were first scanned to PNM format files. These are large. They have been cropped and slightly edited. They are generally useless except for rebuilding TIFF images should the need arise. So much effort went into the scanning that these are kept just in case the TIFF images need to be regenerated.</li>
    </ul>
    </p>

{% endblock content %}
BODY
