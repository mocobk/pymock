#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : mocobk
# @Email  : mailmzb@qq.com
# @Time   : 2020/8/18 19:12
import codecs
import json
import json.encoder
import os
import re
import typing

from py_mini_racer import py_mini_racer

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


json.encoder.encode_basestring = encode_regex_basestring_wrap(json.encoder.encode_basestring)
json.encoder.encode_basestring_ascii = encode_regex_basestring_wrap(json.encoder.encode_basestring_ascii)


class MiniRacer(py_mini_racer.MiniRacer):
    def call(self, identifier, *args, **kwargs):
        """ Call the named function with provided arguments
        You can pass a custom JSON encoder by passing it in the encoder
        keyword only argument.
        """

        encoder = kwargs.get('encoder', None)
        timeout = kwargs.get('timeout', 0)
        max_memory = kwargs.get('max_memory', 0)

        if isinstance(args[0], (dict, list)):
            json_args = json.dumps(args, separators=(',', ':'), cls=encoder)
        else:
            json_args = f'[{args[0]}]'
        js = "{identifier}.apply(this, {json_args})"
        return self.eval(js.format(identifier=identifier, json_args=json_args), timeout, max_memory)


class Mock:
    def __init__(self):
        self.__code = codecs.open(os.path.join(os.path.dirname(__file__), 'js/mock.mini_racer.min.js'),
                                  encoding='utf-8').read()
        self.__ctx = MiniRacer()
        self.__ctx.eval(self.__code)

    def mock(self, template: typing.Union[dict, list, str]) -> typing.Union[dict, list]:
        """
        :param template: mock template
        :return: dict, list
        """
        return self.__ctx.call('Mock.mock', template)
