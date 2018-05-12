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

from asmtest import *
import unittest

class TestParserCompilerAsmOutput(unittest.TestCase):

    def test_empty(self):
        self.assertEqual([], parse_compiler_asm_output(''))
        self.assertEqual([], parse_compiler_asm_output('\n\n'))

    def test_no_function(self):
        output = '''
    .directive
    .directive
'''
        self.assertEqual([], parse_compiler_asm_output(output))

        output = '''
    .directive
    insn
    .directive
    insn
'''
        self.assertEqual([], parse_compiler_asm_output(output))

        output = '''
    .directive
    insn
directive_at_line_begin
    .directive
    insn
'''
        self.assertEqual([], parse_compiler_asm_output(output))

    def test_empty_function_at_file_end(self):
        output = '''
    .directive
function_name:
'''

        self.assertEqual([ AsmFunction('function_name') ],
                         parse_compiler_asm_output(output))

    def test_empty_function(self):
        output = '''
function_name:
function_name2:
'''

        expected = [
            AsmFunction('function_name'),
            AsmFunction('function_name2'),
        ]
        self.assertEqual(expected, parse_compiler_asm_output(output))

    def test_function_with_directive(self):
        output = '''
function_name:
    .directive
'''

        expected = [
            AsmFunction('function_name'),
        ]
        self.assertEqual(expected, parse_compiler_asm_output(output))

    def test_function_with_trash_after_name(self):
        output = '''
function_name: @ some characters
    insn
'''

        expected = [
            AsmFunction('function_name', ['insn']),
        ]
        self.assertEqual(expected, parse_compiler_asm_output(output))

    def test_function_with_instructions(self):
        output = '''
function_name:
    insn1
    insn2 param
    insn3 param param
'''

        expected = [
            AsmFunction('function_name', ['insn1', 'insn2', 'insn3']),
        ]
        self.assertEqual(expected, parse_compiler_asm_output(output))

    def test_function_with_label(self):
        output = '''
function_name:
    insn1
    insn2 param
.label:
    insn3 param param
'''

        expected = [
            AsmFunction('function_name', ['insn1', 'insn2', 'insn3']),
        ]
        self.assertEqual(expected, parse_compiler_asm_output(output))

class TestInsnCountFromInsnList(unittest.TestCase):

    def test_empty(self):
        self.assertEqual({}, InsnCount.from_insn_list([]).insns)

    def test_single(self):
        insns = [ '1' ]
        expected = { '1' : 1 }
        self.assertEqual(expected, InsnCount.from_insn_list(insns).insns)

    def test_duplicates(self):
        insns = [ '1', '2', '1' ]
        expected = { '1' : 2, '2' : 1 }
        self.assertEqual(expected, InsnCount.from_insn_list(insns).insns)
