#!/bin/sh
#
# Create detail view template.

wipdir=${0%%mkindexcss.sh}

cat <<CSS1
html,
body {
    margin:0;
    padding:0;
    height:100%;
    font-family: sans-serif;
CSS1

# This mess does a nice job at creating the logo img tag from external base64.
echo -n "    background-image: url(data:image/png;base64,"
cat ${wipdir}/background-base64.txt
echo ");"
echo "}"
echo

cat <<CSS2

#container {
    min-height:100%;
    position:relative;
}

#header {
    background:#ff0;
    padding:10px;
}

#content {
    padding:10px;
    padding-bottom:60px;   /* Height of the footer */
}

#footer {
    color: #fff;
    border-top: 1px solid black;
    position:absolute;
    bottom:0;
    width:100%;
    height:64px;   /* Height of the footer */
    background: rgba(0, 0, 0, 0.5);
}

h1 h2 h3 h4 h5 h6 p {
    font-family: sans-serif;
}

code {
    background-color: #EEEEEE;
}

li {
    line-height: 1.5em;
}

pre {
    margin-left: 1em;
    margin-right: 1em;
    background-color: #EEEEEE;
    padding: 0.5em;
    white-space: pre-wrap;       /* CSS 3 */
    white-space: -moz-pre-wrap;  /* Mozilla, since 1999 */
    white-space: -pre-wrap;      /* Opera 4-6 */
    white-space: -o-pre-wrap;    /* Opera 7 */
    word-wrap: break-word;       /* Internet Explorer 5.5+ */
}

/* from encycolorpedia.com/008000 (Green) Sonya */

 /* Unvisited link Revell 37161*/
a:link {
    color: #127826;
}

/* Visited link Revell 37161 (Green) Sonya */
a:visited {
    color: #127826;
}

/* Mouse over link Revell 37130 (Red) Ry */
a:hover {
    color: #f23b1c;
}

/* Selected link  Revell 37112 (Yellow) Anna */
a:active {
    color: #ffd64d;
}

table.heading {
    width: 100%;
    table-layout: fixed;
}

table.heading td.title {
    width: 80%;
    vertical-align: top;
}

table.heading td.logo {
    width: 20%;
    text-align: right;
}

table.contents {
    width: 100%;
    table-layout: fixed;
    white-space: nowrap;
    border: 1px solid #ccc;
    border-collapse: collapse;
    border-spacing: 0;
    box-shadow: 0 0 1em #eee; /* from pre.contents */
}

table.contents td {
    border: 1px solid #ccc;
    padding: .1em .25em;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    text-align: left;
    padding-left: 0.5em;
}

table.contents td.metakey {
    width: 10%;
    background: #fff;
    font-weight: bold;
}

table.contents td.metaval {
    width: 90%;
}

table.contents th {
    border: 1px solid #bbb;
    padding: .1em .25em;
    background-color: #f7f7f7;
    text-align: left;
    padding-left: 0.5em;
}

/* DETAIL page */
table.contents th.photoid {
    width: 10%;
}

table.contents th.notes {
    width: 90%;
}

/* CONTENTS page */
table.contents th.packageid {
    width: 10%;
}

table.contents th.description {
    width: 90%;
}

table.contents tbody tr.even { background-color: #fcfcfc }
table.contents tbody tr.odd { background-color: #f7f7f7 }
CSS2
