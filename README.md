# HTMLMinifier

[![Build Status](https://travis-ci.org/jason2506/HTMLMinifier.png)](http://travis-ci.org/jason2506/HTMLMinifier)

A simple HTML5 minifier inspired by [jinja2-htmlcompress](https://github.com/mitsuhiko/jinja2-htmlcompress).

## How it Works

* Spaces in **space-preserved elements** (i.e., `<pre>`, `<script>`, `<style>` and `<textarea>`) will be preserved.
* Multiple spaces in element content (except **space-preserved elements**) will be collapsed.
* Spaces around start and end tag of [block elements](http://www.w3.org/TR/CSS2/visuren.html#block-boxes) will be removed.
* Redundant spaces within element tag will be removed.
* Slash character ('/') in self-closing tag (e.g., `<br/>` or `<img src="..."/>`) of [void elements](http://www.w3.org/TR/html5/syntax.html#void-elements) will be removed.
* Unnecessary quotes around element attributes could be removed (off by default).
* Comments (except [IE conditional comments](http://msdn.microsoft.com/en-us/library/ms537512.ASPX)) will be removed (could be disabled). The content in the IE conditional comments will be further minified.

## License

Copyright (c) 2014, Chi-En Wu.

Distributed under [The BSD 3-Clause License](http://opensource.org/licenses/BSD-3-Clause).
