# -*- coding: utf-8 -*-

from nose.tools import assert_equal

from HTMLMinifier import minify


class TestParser(object):

    def test_simplest_html(self):
        html = u"""
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
        minified_html = u'<!DOCTYPE html>' \
                        u'<html><head><title>Hello</title></head>' \
                        u'<body><p>hello, world</p></body></html>'
        assert_equal(minified_html, minify(html))

    def test_remove_comments(self):
        html = u"""
        <!--
        this comment will be removed.
        -->
        """
        assert_equal('', minify(html))

    def test_preserve_comments(self):
        html = u"""
        <!--
        this comment will be removed.
        -->
        """
        assert_equal(html.strip(), minify(html, remove_comments=False))

    def test_ie_cond_comment(self):
        html = u"""
        <!--[if lt IE 9]>
          <p>  This is a paragraph  </p>
          <p>  This is another paragraph  </p>
        <![endif]-->
        """
        minified_html = u'<!--[if lt IE 9]>' \
                        u'<p>This is a paragraph</p>' \
                        u'<p>This is another paragraph</p>' \
                        u'<![endif]-->'
        assert_equal(minified_html, minify(html))

    def test_tag_with_attrs(self):
        html = u"""
        <div class="field required">
          <label for=username>User Name: </label>
          <input type  =  "text"    id="username">
        </div>
        """
        minified_html = u'<div class="field required">' \
                        u'<label for="username">User Name: </label>' \
                        u'<input type="text" id="username">' \
                        u'</div>'
        assert_equal(minified_html, minify(html))

        minified_html = u'<div class="field required">' \
                        u'<label for=username>User Name: </label>' \
                        u'<input type=text id=username>' \
                        u'</div>'
        assert_equal(minified_html, minify(html, remove_quotes=True))

    def test_self_closing_tags(self):
        html = u"""
        <div class="clearfix" />
        <img src="test.jpg" />
        """
        minified_html = u'<div class="clearfix"/>' \
                        u'<img src="test.jpg">'
        assert_equal(minified_html, minify(html))

    def test_pre_ws_elements(self):
        html = u"""
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
        html = u"""
        <p>  This is a [ <a href="index.html"> link </a> ]  </p>
        <p>  Some <b> highlighted </b> <i> text </i>  </p>
        <p>  More <b> complex <i> example </i> </b> ! </p>
        """
        minified_html = u'<p>This is a [ <a href="index.html">link </a>]</p>' \
                        u'<p>Some <b>highlighted </b><i>text</i></p>' \
                        u'<p>More <b>complex <i>example </i></b>!</p>'
        assert_equal(minified_html, minify(html))

    def test_entity(self):
        html = u"""
        <p> &lt; html &gt; </p>
        """
        minified_html = u'<p>&lt; html &gt;</p>'
        assert_equal(minified_html, minify(html))
