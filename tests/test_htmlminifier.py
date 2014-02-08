# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from nose.tools import assert_equal

from HTMLMinifier import minify


class TestMinifier(object):

    def test_simplest_html(self):
        html = """
        <!DOCTYPE html>
        <html>
          <head>
            <title>Hello</title>
          </head>
          <body>
            <p>hello, world</p>
          </body>
        </html>
        """
        minified_html = '<!DOCTYPE html>' \
                        '<html><head><title>Hello</title></head>' \
                        '<body><p>hello, world</p></body></html>'
        assert_equal(minified_html, minify(html))

    def test_comment(self):
        html = """
        <!--
        this comment will be removed.
        -->
        """
        assert_equal('', minify(html))
        assert_equal(html.strip(), minify(html, remove_comments=False))

    def test_cond_comment(self):
        html = """
        <!--[if lt IE 9]>
          <p>  This is a paragraph  </p>
          <p>  This is another paragraph  </p>
        <![endif]-->
        """
        minified_html = '<!--[if lt IE 9]>' \
                        '<p>This is a paragraph</p>' \
                        '<p>This is another paragraph</p>' \
                        '<![endif]-->'
        assert_equal(minified_html, minify(html))

    def test_tag_with_attr(self):
        html = """
        <div class="field required">
          <label for=username>User Name: </label>
          <input type  =  "text"    id="username">
        </div>
        """
        minified_html = '<div class="field required">' \
                        '<label for="username">User Name: </label>' \
                        '<input type="text" id="username">' \
                        '</div>'
        assert_equal(minified_html, minify(html))

        minified_html = '<div class="field required">' \
                        '<label for=username>User Name: </label>' \
                        '<input type=text id=username>' \
                        '</div>'
        assert_equal(minified_html, minify(html, remove_quotes=True))

    def test_self_closing_tag(self):
        html = """
        <div class="clearfix" />
        <img src="test.jpg" />
        """
        minified_html = '<div class="clearfix"/>' \
                        '<img src="test.jpg">'
        assert_equal(minified_html, minify(html))

    def test_space_preserved_element(self):
        html = """
        <script>
          var sum = 0;
          for (var i = 0; i < 10; i++) {
              sum += i;
          }
          console.log(i);
        </script>
        """
        assert_equal(html.strip(), minify(html))

    def test_collapseing_spaces(self):
        html = """
        <p>  This is a [ <a href="index.html"> link </a> ]  </p>
        <p>  Some <b> highlighted </b> <i> text </i>  </p>
        <p>  More <b> complex <i> example </i> </b> ! </p>
        """
        minified_html = '<p>This is a [ <a href="index.html">link </a>]</p>' \
                        '<p>Some <b>highlighted </b><i>text</i></p>' \
                        '<p>More <b>complex <i>example </i></b>!</p>'
        assert_equal(minified_html, minify(html))

    def test_entity(self):
        html = """
        <p> &lt; html &#x3E; </p>
        """
        minified_html = '<p>&lt; html &#x3E;</p>'
        assert_equal(minified_html, minify(html))
