#   Copyright (C) 2016-2018  Povilas Kanapickas <povilas@radix.lt>
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

import unittest

from asmtest.compiler import detect_compiler_from_version_output


class TestDetectCompilerFromVersionOutput(unittest.TestCase):

    def test_gcc(self):
        output = 'g++ (Ubuntu 7.2.0-8ubuntu3.2) 7.2.0'
        self.assertEqual(('gcc', '7.2.0'),
                         detect_compiler_from_version_output(output))

    def test_gcc_with_date(self):
        output = 'arm-linux-gnueabihf-g++-5 (Ubuntu/Linaro 5.4.1-8ubuntu1) 5.4.1 20170304'  # noqa: E501
        self.assertEqual(('gcc', '5.4.1'),
                         detect_compiler_from_version_output(output))

    def test_clang(self):
        output = 'clang version 4.0.1-6 (tags/RELEASE_401/final)'
        self.assertEqual(('clang', '4.0.1-6'),
                         detect_compiler_from_version_output(output))
