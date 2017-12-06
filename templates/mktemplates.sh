#!/bin/sh

wipdir=${0%%mktemplates.sh}
templates_dir="$wipdir/../photo_album/templates"

echo "Creating templates..."

echo "index.css"
$wipdir/mkindexcss.sh > index.css

echo "gallery.css"
$wipdir/mkgallerycss.sh > gallery.css

echo "base.html"
$wipdir/mkbasetemplate.sh > "${templates_dir}/base.html"

echo "contents.html"
$wipdir/mkcontentstemplate.sh > "${templates_dir}/contents.html"

echo "gallery.html"
$wipdir/mkgallerytemplate.sh > "${templates_dir}/gallery.html"

echo "detail.html"
$wipdir/mkdetailtemplate.sh > "${templates_dir}/detail.html"

rm index.css
rm gallery.css
