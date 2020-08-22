#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : mocobk
# @Email  : mailmzb@qq.com
# @Time   : 2020/8/18 19:12
import codecs
import os
import re
import typing
from json.encoder import encode_basestring_ascii, encode_basestring, INFINITY, c_make_encoder, _make_iterencode, \
    JSONEncoder as _JSONEncoder

from py_mini_racer.py_mini_racer import MiniRacer

__JS_REGEX_PATTERN = re.compile(r'^/.*/$')
__JS_REGEX_ESCAPE_PATTERN = re.compile(r'^\\/.*\\/$')


def encode_regex_basestring_wrap(func):
    def wrap(string: str):
        if __JS_REGEX_PATTERN.match(string):
            return string
        else:
            if __JS_REGEX_ESCAPE_PATTERN.match(string):
                string = f'/{string[2:-2]}/'
        return func(string)

    return wrap


class JSONEncoder(_JSONEncoder):
    """For support js regex str"""

    def iterencode(self, o, _one_shot=False):
        """Encode the given object and yield each string
        representation as available.

        For example::

            for chunk in JSONEncoder().iterencode(bigobject):
                mysocket.write(chunk)

        """
        if self.check_circular:
            markers = {}
        else:
            markers = None
        if self.ensure_ascii:
            # For support js regex str
            _encoder = encode_regex_basestring_wrap(encode_basestring_ascii)
        else:
            _encoder = encode_regex_basestring_wrap(encode_basestring)

        def floatstr(o, allow_nan=self.allow_nan,
                     _repr=float.__repr__, _inf=INFINITY, _neginf=-INFINITY):
            # Check for specials.  Note that this type of test is processor
            # and/or platform-specific, so do tests which don't depend on the
            # internals.

            if o != o:
                text = 'NaN'
            elif o == _inf:
                text = 'Infinity'
            elif o == _neginf:
                text = '-Infinity'
            else:
                return _repr(o)

            if not allow_nan:
                raise ValueError(
                    "Out of range float values are not JSON compliant: " +
                    repr(o))

            return text

        if (_one_shot and c_make_encoder is not None
                and self.indent is None):
            _iterencode = c_make_encoder(
                markers, self.default, _encoder, self.indent,
                self.key_separator, self.item_separator, self.sort_keys,
                self.skipkeys, self.allow_nan)
        else:
            _iterencode = _make_iterencode(
                markers, self.default, _encoder, self.indent, floatstr,
                self.key_separator, self.item_separator, self.sort_keys,
                self.skipkeys, _one_shot)
        return _iterencode(o, 0)


class Mock:
    def __init__(self):
        self.__code = codecs.open(os.path.join(os.path.dirname(__file__), 'js/mock.mini_racer.min.js'),
                                  encoding='utf-8').read()
        self.__ctx = MiniRacer()
        self.__ctx.eval(self.__code)

    def mock(self,
             template: typing.Union[dict, list, str],
             encoder=JSONEncoder,
             timeout=0,
             max_memory=0) -> typing.Union[dict, list, str]:
        """
        Mock from python object
        :param template: Mock template
        :param encoder: You can pass a custom JSON encoder by passing it in the encoder
        :param timeout: Limit run timeout, default no limit: timeout = 0(millisecond)
        :param max_memory: Limit max memory, default no limit: max_memory = 0
        :return: dict, list, str
        """
        return self.__ctx.call('Mock.mock', template, encoder=encoder, timeout=timeout, max_memory=max_memory)

    def mock_js(self,
                js_str: str,
                timeout=0,
                max_memory=0) -> typing.Union[dict, list, str]:
        """
        Mock form JSON string or JavaScript Object like-string
        :param js_str: Mock template
        :param timeout: Limit run timeout, default no limit: timeout = 0(millisecond)
        :param max_memory: Limit max memory, default no limit: max_memory = 0
        :return: dict, list, str
        """
        js = "Mock.mock({template})".format(template=js_str)
        return self.__ctx.eval(js, timeout, max_memory)
