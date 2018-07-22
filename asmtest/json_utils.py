#!/usr/bin/env python3

#   Copyright (C) 2018  Povilas Kanapickas <povilas@radix.lt>
#
#   This file is part of libsimdpp asm tests
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see http://www.gnu.org/licenses/.

from __future__ import print_function

import json
import re


class NoIndent(object):

    def __init__(self, value):
        self.value = value


class NoIndentJsonEncoder(json.JSONEncoder):

    def __init__(self, *args, **kwargs):
        super(NoIndentJsonEncoder, self).__init__(*args, **kwargs)
        self._kwargs = dict(kwargs)
        self._kwargs.pop('indent')
        self._replacement_list = []

    def _unique_json_id(self):
        return 'noindent-584cf21a545b11e8843b-d37cfd205cef'

    def _add_replacement(self, value):
        self._replacement_list.append(value)
        return len(self._replacement_list) - 1

    def _handle_noindent_value(self, match):
        try:
            key = int(match.group(1))
            return self._replacement_list[key]
        except Exception:
            raise Exception('Could not parse {0}'.format(match.group(0)))

    def default(self, o):
        if isinstance(o, NoIndent):
            key = self._add_replacement(json.dumps(o.value, **self._kwargs))
            return self._unique_json_id() + str(key)
        return super(NoIndentJsonEncoder, self).default(o)

    def iterencode(self, o, **kwargs):
        id_pattern = r'"{0}(\d+)"'.format(self._unique_json_id())
        for chunk in super(NoIndentJsonEncoder, self).iterencode(o, **kwargs):
            chunk = re.sub(id_pattern,
                           lambda m: self._handle_noindent_value(m), chunk)
            yield chunk
