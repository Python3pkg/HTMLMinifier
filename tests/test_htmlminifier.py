# -*- coding: utf-8 -*-

from nose.tools import assert_equal

from HTMLMinifier import HTMLMinifier


class TestMinifier(object):
    def setUp(self):
        self.minifier = HTMLMinifier()

    def minify(self, html):
        self.minifier.feed(html)
        return self.minifier.get_minified_html()

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
        assert_equal(minified_html, self.minify(html))

    def test_remove_comments(self):
        html = u"""
        <!--
        this comment will be removed.
        -->
        """
        assert_equal('', self.minify(html))

    def test_preserve_comments(self):
        html = u"""
        <!--
        this comment will be removed.
        -->
        """
        self.minifier.remove_comments = False
        assert_equal(html.strip(), self.minify(html))

    def test_ie_cond_comment(self):
        html = u"""
        <!--[if lt IE 9]>
        some comments here
        <![endif]-->
        """
        assert_equal(html.strip(), self.minify(html))

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
        assert_equal(minified_html, self.minify(html))

    def test_remove_quotes(self):
        html = u"""
        <div class="field required">
          <label for=username>User Name: </label>
          <input type  =  "text"    id="username">
        </div>
        """
        minified_html = u'<div class="field required">' \
                        u'<label for=username>User Name: </label>' \
                        u'<input type=text id=username>' \
                        u'</div>'
        self.minifier.remove_quotes = True
        assert_equal(minified_html, self.minify(html))

    def test_self_closing_tags(self):
        html = u"""
        <div class="clearfix" />
        <img src="test.jpg" />
        """
        minified_html = u'<div class="clearfix"/>' \
                        u'<img src="test.jpg">'
        assert_equal(minified_html, self.minify(html))

    def test_pre_ws_elements(self):
        html = u"""
        <script>
          var sum = 0;
          for (var i = 0; i < 10; i++) {
              sum += i;
          }
          console.log(i)
        </script>
        """
        assert_equal(html.strip(), self.minify(html))

    def test_entity(self):
        html = u"""
        <p> &lt; html &gt; </p>
        """
        minified_html = u'<p>&lt; html &gt;</p>'
        assert_equal(minified_html, self.minify(html))
