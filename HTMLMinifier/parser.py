# -*- coding: utf-8 -*-



import re
import sys
if sys.version_info[0] < 3:
    from html.parser import HTMLParser
else:
    from html.parser import HTMLParser

_EMPTY_SET = frozenset()

_PRE_WS_ELEMENTS = frozenset(('pre', 'script', 'style', 'textarea'))

_RM_WS_ELEMENTS = frozenset(('colgroup', 'datalist', 'head', 'select'))

_VOID_ELEMENTS = frozenset(('area', 'base', 'br', 'col', 'command', 'embed',
                            'hr', 'img', 'input', 'keygen', 'link', 'meta',
                            'param', 'source', 'track', 'wbr'))

_HIDDEN_ELEMENTS = frozenset(('datalist', 'script', 'style'))

_BLOCK_ELEMENTS = frozenset(('address', 'article', 'aside', 'blockquote',
                             'body', 'dd', 'details', 'div', 'dl', 'dt',
                             'fieldset', 'figcaption', 'figure', 'footer',
                             'form', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
                             'header', 'hgroup', 'hr', 'html', 'legend',
                             'menu', 'nav', 'ol', 'p', 'pre', 'section',
                             'summary', 'table', 'tbody', 'td', 'tfoot', 'th',
                             'thead', 'tr', 'ul'))

_COND_COMMENT_PATTERN = re.compile(r'^\[if([^\]]+)\]>(.*)<!\[endif\]$', flags=re.DOTALL)
_WS_PATTERN = re.compile(r'\s+')


def _make_omission_rules(rules):
    return dict((tag, followed_tags)
                for tags, followed_tags in rules for tag in tags)


# See: http://www.w3.org/TR/html5/syntax.html#optional-tags
_OMISSION_RULES = _make_omission_rules((
    (('colgroup',), frozenset(('colgroup', 'thead', 'tbody', 'tfoot', 'tr'))),
    (('dd', 'dt'), frozenset(('dt', 'dd'))),
    (('li',), frozenset(('li',))),
    (('optgroup',), frozenset(('optgroup',))),
    (('option',), frozenset(('optgroup', 'option'))),
    (('p',), _BLOCK_ELEMENTS),
    (('rp', 'rt'), frozenset(('rp', 'rt'))),
    (('thead', 'tbody'), frozenset(('tbody', 'tfoot'))),
    (('th', 'td'), frozenset(('th', 'td'))),
    (('tfoot',), frozenset(('tbody',))),
    (('tr',), frozenset(('tr',)))
))

_DECL_FORMAT = '<!%s>'
_UNKNOWN_DECL_FORMAT = '<![%s]>'
_PI_FORMAT = '<?%s>'
_COND_COMMENT_START_FORMAT = '<!--[if%s]>'
_COND_COMMENT_END_FORMAT = '<![endif]-->'
_COMMENT_FORMAT = '<!--%s-->'
_ELEM_START_FORMAT = '<%s%s>'
_ELEM_END_FORMAT = '</%s>'
_ATTR_VAL_FORMAT = '"%s"'
_ATTR_FORMAT = '%s=%s'
_ENTITY_REF_FORMAT = '&%s;'
_CHAR_REF_FORMAT = '&#%s;'


class Parser(HTMLParser):

    def __init__(self, remove_comments=True, remove_quotes=False):
        self.remove_comments = remove_comments
        self.remove_quotes = remove_quotes

        HTMLParser.__init__(self)

    def reset(self):
        HTMLParser.reset(self)

        self._buffer = []
        self._tag_stack = []
        self._remove_begining_ws = True
        self._preserve = 0
        self._last_text_idx = -1

        self._backup = []

    def _push_status(self):
        self._backup.append((self.rawdata, self.lasttag, self.getpos()))
        HTMLParser.reset(self)

    def _pop_status(self):
        self.rawdata, self.lasttag, pos = self._backup.pop()
        self.updatepos(*pos)

    def _reset_newline_status(self):
        self._remove_begining_ws = False
        self._last_text_idx = -1

    def _enter_newline(self):
        """
        Remove the trailing spaces in the current line, and then mark that the
        leading spaces of the next line need to be removed.

        .. seealso::
           `CSS Text Module Level 3 - The White Space Processing Rules
            <http://www.w3.org/TR/css3-text/#white-space-phase-2>`_
        """

        last_text_idx = self._last_text_idx
        if last_text_idx >= 0:
            buf = self._buffer
            buf[last_text_idx] = buf[last_text_idx].rstrip()

        self._remove_begining_ws = True

    def _append_tag(self, tag, attrs, closing=False):
        tokens = [tag]
        append_token = tokens.append
        for name, val in attrs:
            if val is None:
                append_token(name)
            else:
                if not self.remove_quotes or ' ' in val:
                    val = _ATTR_VAL_FORMAT % val
                append_token(_ATTR_FORMAT % (name, val))

        self._buffer.append(_ELEM_START_FORMAT % (' '.join(tokens),
                                                  '/' if closing else ''))

    def handle_decl(self, decl):
        self._buffer.append(_DECL_FORMAT % decl)

    def handle_comment(self, comment):
        """
        Remove comment except IE conditional comment.

        .. seealso::
           `About conditional comments
            <http://msdn.microsoft.com/en-us/library/ms537512.ASPX>`_
        """

        match = _COND_COMMENT_PATTERN.match(comment)
        if match is not None:
            cond = match.group(1)
            content = match.group(2)

            self._buffer.append(_COND_COMMENT_START_FORMAT % cond)
            self._push_status()
            self.feed(content)
            self._pop_status()
            self._buffer.append(_COND_COMMENT_END_FORMAT)
        elif not self.remove_comments:
            self._buffer.append(_COMMENT_FORMAT % comment)

    def handle_starttag(self, tag, attrs):
        tag_stack = self._tag_stack
        if tag_stack and \
           tag in _OMISSION_RULES.get(tag_stack[-1], _EMPTY_SET):
            tag_stack.pop()

        if tag not in _VOID_ELEMENTS:
            tag_stack.append(tag)

        if tag in _BLOCK_ELEMENTS:
            self._enter_newline()
        elif tag in _VOID_ELEMENTS and tag not in _HIDDEN_ELEMENTS:
            self._reset_newline_status()

        if tag in _PRE_WS_ELEMENTS:
            self._preserve += 1

        self._append_tag(tag, attrs)

    def handle_endtag(self, tag):
        tag_stack_pop = self._tag_stack.pop
        while tag != tag_stack_pop():
            pass

        self._buffer.append(_ELEM_END_FORMAT % tag)
        if tag in _BLOCK_ELEMENTS:
            self._enter_newline()

        if tag in _PRE_WS_ELEMENTS:
            self._preserve -= 1

    def handle_startendtag(self, tag, attrs):
        """
        Normalize the tag with trailing '/' character (such as `<img ... />`).

        The trailing '/' character has no effect on void elements, but on
        foreign elements it marks the start tag as self-closing.

        .. seealso::
           `HTML5 - Start tags
            <http://www.w3.org/TR/html5-author/syntax.html#syntax-start-tag>`_
        """
        is_foreign = tag not in _VOID_ELEMENTS
        self._append_tag(tag, attrs, closing=is_foreign)
        if tag in _BLOCK_ELEMENTS:
            self._enter_newline()
        elif tag not in _HIDDEN_ELEMENTS:
            self._reset_newline_status()

    def handle_data(self, data):
        """
        Any space immediately following another collapsible space will be
        collapsed.

        .. seealso::
           `CSS Text Module Level 3 - The White Space Processing Rules
            <http://www.w3.org/TR/css3-text/#egbidiwscollapse>`_
        """

        tag_stack = self._tag_stack
        if tag_stack and tag_stack[-1] in _RM_WS_ELEMENTS:
            # just ignore the content of this element
            assert data.strip() == ''
            return

        if self._preserve == 0:
            if self._remove_begining_ws:
                data = data.lstrip()
                if not data:
                    return

                self._remove_begining_ws = False

            self._last_text_idx = len(self._buffer)

            data = _WS_PATTERN.sub(' ', data)
            if data and data[-1] == ' ':
                # immediately followed spaces will be collapsed
                self._remove_begining_ws = True
        else:
            # the content cannot be stripped
            self._reset_newline_status()

        self._buffer.append(data)

    def handle_entityref(self, entity):
        self._buffer.append(_ENTITY_REF_FORMAT % entity)
        self._reset_newline_status()

    def handle_charref(self, char):
        self._buffer.append(_CHAR_REF_FORMAT % char)
        self._reset_newline_status()

    def handle_pi(self, pi):
        self._buffer.append(_PI_FORMAT % pi)

    def unknown_decl(self, decl):
        self._buffer.append(_UNKNOWN_DECL_FORMAT % decl)

    def get_minified_html(self):
        return ''.join(self._buffer).rstrip()
