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
$wipdir/mkindexcss.sh | sed -e 's/^/      /'

cat <<BODY1
    </style>
  </head>

{% block body %}
  <body>
{% endblock %}

  <div id="container">
    <div id="content">
      <table class="heading">
        <tbody>
          <tr>
            {% block title_td %}
            <td class="title">
              <h1>{{ title }}</h1>
            </td>
            {% endblock %}
            <td class="logo">
BODY1

# This mess does a nice job at creating the logo img tag from external base64.
echo -n "<img alt=\"Logo Image\" height=\"92\" src=\"data:image/png;base64,"
cat logo-base64.txt | tr '\n' '\"'
echo " />"

cat <<BODY2
            </td>
          </tr>
        </tbody>
      </table>

      {% block content %}{% endblock %}

    </div> {# <!-- /#content --> #}

    <div id="footer">
        <p style="text-align: center;">Crafted with Love by eigenholser</p>
    </div>

    </div> {# <!-- /#container --> #}
  </body>
</html>
BODY2
