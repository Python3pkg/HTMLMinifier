# HTMLMinifier

[![Build Status](https://travis-ci.org/jason2506/HTMLMinifier.png)](http://travis-ci.org/jason2506/HTMLMinifier)

A simple HTML5 minifier inspired by [jinja2-htmlcompress](https://github.com/mitsuhiko/jinja2-htmlcompress).

## Quickstart

```python
>>> from HTMLMinifier import minify
>>> html = u'''
    <!DOCTYPE html>
    <html>
      <head>
        <title>Hello</title>
      </head>
      <body>
        <p>hello, world</p>
      </body>
    </html>'''
>>> minify(html)
u'<!DOCTYPE html><html><head><title>Hello</title></head><body><p>hello, world</p></body></html>'
```

## How it Works

* Spaces in **space-preserved elements** (i.e., `<pre>`, `<script>`, `<style>` and `<textarea>`) will be preserved.
* Spaces directly contained in **spaceless elements** (i.e., `<colgroup>`, `<datalist>`, `<head>` and `<select>`) will be removed.
* Multiple spaces in element content (except **space-preserved elements**) will be collapsed. See [The White Space Processing Rules](http://www.w3.org/TR/css-text-3/#egbidiwscollapse) for more details.
* Spaces around start and end tag of [block elements](http://www.w3.org/TR/CSS2/visuren.html#block-boxes) will be removed.
* Redundant spaces within element tag (e.g. multiple spaces between attributes or spaces around '=') will be removed.
* Slash character ('/') in self-closing tag (e.g., `<br/>` or `<img src="..."/>`) of [void elements](http://www.w3.org/TR/html5/syntax.html#void-elements) will be removed.
* Unnecessary quotes around element attributes could be removed (off by default).
* Comments (except [IE conditional comments](http://msdn.microsoft.com/en-us/library/ms537512.ASPX)) will be removed (could be disabled). The content in the IE conditional comments will be further minified.

## License

Copyright (c) 2014, Chi-En Wu.

Distributed under [The BSD 3-Clause License](http://opensource.org/licenses/BSD-3-Clause).
