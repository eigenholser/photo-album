#!/bin/sh
#
# Create content view template.

wipdir=${0%%mkbasetemplate.sh}

cat <<HEAD
<html>
  <head>
    <title>{{ title }}</title>
    {% block style_gallery %}{% endblock %}
    <style type="text/css">
HEAD

# CSS inline
cat $wipdir/index.css | sed -e 's/^/      /'

cat <<BODY1
    </style>
BODY1

# This mess does a nice job at creating the logo img tag from external base64.
echo -n "<link rel=\"icon\" type=\"image/x-icon\" href=\"data:image/x-icon;base64,"
cat favicon-base64.txt
echo "\" />"

cat <<BODY2
  </head>

{% block body %}
  <body>
{% endblock %}

  <div id="container">
    <header>
      {% block title %}
        <h1>{{ title }}</h1>
      {% endblock title %}
BODY2

# This mess does a nice job at creating the logo img tag from external base64.
echo -n "<img alt=\"Logo Image\" height=\"92\" src=\"data:image/png;base64,"
cat logo-base64.txt
echo "\" />"

cat <<BODY3
    </header>

    <article class="instaFade">

      {% block content %}{% endblock %}

    </article>

    <footer>
      <div class="footer-container">
        <div class="footer-child">
          <ul>
            <li><a class="footer" href="{% if pkgid %}../{% endif %}faq.html">Frequently Asked Questions</a></li>
          </ul>
        </div>
        <div class="footer-child">
        </div>
        <div class="footer-child">
        </div>
      </div>
      <div class="footer-credit">
      <p class="footer-credit">Crafted with Care by eigenholser.</p>
      </div>
    </footer>

    </div> {# <!-- /#container --> #}
  </body>
</html>
BODY3
