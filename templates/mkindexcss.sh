#!/bin/sh
#
# Create detail view template.

wipdir=${0%%mkindexcss.sh}

cat <<CSS1
html, body {
    margin:0;
    padding:0;
    height:100%;
    font-family: sans-serif;
    font-size: 16px;
}
CSS1

# TODO: Removed this in favor of plain background. Leaving for now in case I
# change my mind.
#
# This mess does a nice job at creating the logo img tag from external base64.
#echo -n "    background-image: url(data:image/png;base64,"
#cat ${wipdir}/background-base64.txt
#echo ");"
#echo "}"
#echo

cat <<CSS2

#container {
    height: 100vh;
    display: flex;
    flex-direction: column;
}

main {
    flex: 1;
    padding-left: 10px;
    padding-right: 10px;
}

header {
    color: #fff;
    border-bottom: 2px solid black;
    height: 100px;
    background: rgba(0, 0, 0, 0.4);
}

header img {
    position: relative;
    vertical-align: middle;
    float: right;
    padding-right: 10px;
}

header h1 {
    margin-left: 0.5em;
    line-height: 100px; /* same as header height */
    display: inline;
}

footer {
    color: #fff;
    border-top: 2px solid black;
    height:64px;   /* Height of the footer */
    background: rgba(0, 0, 0, 0.4);
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

/* Contents tables on main contents page and detail page. */
table.contents {
    width: 100%;
    table-layout: fixed;
    white-space: nowrap;
    border: 1px solid #ccc;
    border-collapse: collapse;
    border-spacing: 0;
    box-shadow: 0 0 1em #888;
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

table.contents th {
    border: 1px solid #bbb;
    padding: .1em .25em;
    background-color: #606060;
    text-align: left;
    padding-left: 0.5em;
    color: #f0f0f0;
}

/* DETAIL page */
table.contents th.photoid {
    width: 10%;
}

table.contents th.detail-poi {
    width: 1%;
}

table.contents th.notes {
    width: 89%;
}

/* Metadata table on detail page */
table.metadata {
    width: 100%;
    table-layout: fixed;
    white-space: nowrap;
    border: 1px solid #ccc;
    border-collapse: collapse;
    border-spacing: 0;
    box-shadow: 0 0 1em #888;
}

table.metadata td {
    border: 1px solid #ccc;
    padding: .1em .25em;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    text-align: left;
    padding-left: 0.5em;
}

table.metadata td.metakey {
    width: 10%;
    background: #606060;
    color: #f0f0f0;
    font-weight: bold;
}

table.metadata td.metaval {
    width: 90%;
}

/* CONTENTS page */
table.contents th.packageid {
    width: 10%;
}

table.contents th.description {
    width: 90%;
}

/* Alternate row highlights for clarity */
table.contents tr:nth-child(even) {
    /* background-color: #000000; */
    background: rgba(0, 0, 0, 0.05);
}

/*
table.contents tbody tr.even { background-color: #fcfcfc }
table.contents tbody tr.odd { background-color: #f7f7f7 }
*/

/* Fading behavior */
@-webkit-keyframes reset {
    0% {
        opacity: 0;
    }
    100% {
        opacity: 0;
    }
}

@-webkit-keyframes fade-in {
    0% {
        opacity: 0;
    }
    40% {
        opacity: 0;
    }
    100% {
        opacity: 1;
    }
}

@-moz-keyframes reset {
    0% {
        opacity: 0;
    }
    100% {
        opacity: 0;
    }
}

@-moz-keyframes fade-in {
    0% {
        opacity: 0;
    }
    40% {
        opacity: 0;
    }
    100% {
        opacity: 1;
    }
}

@keyframes reset {
    0% {
        opacity: 0;
    }
    100% {
        opacity: 0;
    }
}

@keyframes fade-in {
    0% {
        opacity: 0;
    }
    40% {
        opacity: 0;
    }
    100% {
        opacity: 1;
    }
}

.instaFade {
    -webkit-animation-name: reset, fade-in;
    -webkit-animation-duration: 1.5s;
    -webkit-animation-timing-function: ease-in;

    -moz-animation-name: reset, fade-in;
    -moz-animation-duration: 1.5s;
    -moz-animation-timing-function: ease-in;

    animation-name: reset, fade-in;
    animation-duration: 1.5s;
    animation-timing-function: ease-in;
}

.quickFade {
    -webkit-animation-name: reset, fade-in;
    -webkit-animation-duration: 2.5s;
    -webkit-animation-timing-function: ease-in;

    -moz-animation-name: reset, fade-in;
    -moz-animation-duration: 2.5s;
    -moz-animation-timing-function: ease-in;

    animation-name: reset, fade-in;
    animation-duration: 2.5s;
    animation-timing-function: ease-in;
}

.delayOne {
    -webkit-animation-delay: 0, .5s;
    -moz-animation-delay: 0, .5s;
    animation-delay: 0, .5s;
}

.delayTwo {
    -webkit-animation-delay: 0, 1s;
    -moz-animation-delay: 0, 1s;
    animation-delay: 0, 1s;
}

.delayThree {
    -webkit-animation-delay: 0, 1.5s;
    -moz-animation-delay: 0, 1.5s;
    animation-delay: 0, 1.5s;
}

.delayFour {
    -webkit-animation-delay: 0, 2s;
    -moz-animation-delay: 0, 2s;
    animation-delay: 0, 2s;
}

.delayFive {
    -webkit-animation-delay: 0, 2.5s;
    -moz-animation-delay: 0, 2.5s;
    animation-delay: 0, 2.5s;
}
CSS2
