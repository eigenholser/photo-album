#!/bin/sh

templates_dir="../photo_album/templates"
echo "Creating templates..."
echo "contents.html"
./mkcontentstemplate.sh > "${templates_dir}/contents.html"
echo "gallery.html"
./mkgallerytemplate.sh > "${templates_dir}/gallery.html"
echo "detail.html"
./mkdetailtemplate.sh > "${templates_dir}/detail.html"
