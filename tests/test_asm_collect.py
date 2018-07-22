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

import sys
import unittest

from asmtest.asm_collect import get_output_location_for_settings
from asmtest.asm_collect import merge_equivalent_insns
from asmtest.asm_collect import parse_insn_sets
from asmtest.asm_collect import write_results
from asmtest.asm_parser import InsnCount
from asmtest.compiler import CompilerBase
from asmtest.insn_set import InsnSet
from asmtest.insn_set import InsnSetConfig
from asmtest.test_desc import Test
from asmtest.test_desc import TestDesc

if sys.version_info[0] < 3:
    # io.StringIO only supports unicode strings
    from StringIO import StringIO
else:
    from io import StringIO


class TestGetOutputLocationForSettings(unittest.TestCase):

    def test_gcc_x86_64_4_9_2_ssse3(self):
        compiler = CompilerBase()
        compiler.name = 'gcc'
        compiler.version = '4.9.0'
        compiler.target_arch = 'x86_64'

        config = InsnSetConfig([InsnSet.X86_SSE2,
                                InsnSet.X86_SSE3,
                                InsnSet.X86_SSSE3,
                                InsnSet.X86_SSE4_1])

        expected = 'gcc_4.9/cat_x86_64_sse2_sse3_ssse3_sse4.1.json'
        result = get_output_location_for_settings(compiler, config, 'cat')
        self.assertEqual(expected, result)

    def test_gcc_x86_64_5_3_1_avx512_all(self):
        compiler = CompilerBase()
        compiler.name = 'gcc'
        compiler.version = '5.3.1'
        compiler.target_arch = 'x86'

        config = InsnSetConfig([InsnSet.X86_SSE2,
                                InsnSet.X86_SSE3,
                                InsnSet.X86_SSSE3,
                                InsnSet.X86_SSE4_1,
                                InsnSet.X86_AVX,
                                InsnSet.X86_AVX2,
                                InsnSet.X86_FMA3,
                                InsnSet.X86_AVX512F,
                                InsnSet.X86_AVX512BW,
                                InsnSet.X86_AVX512DQ,
                                InsnSet.X86_AVX512VL])

        expected = 'gcc_5/cat_x86_sse2_sse3_ssse3_sse4.1_avx_avx2_' \
                   'fma3_avx512f_avx512bw_avx512dq_avx512vl.json'
        result = get_output_location_for_settings(compiler, config, 'cat')
        self.assertEqual(expected, result)


class TestParseInsnSets(unittest.TestCase):

    def test_single(self):
        expected = [InsnSet.X86_FMA3]

        self.assertEqual(expected,
                         parse_insn_sets('HAS_FMA3').insn_sets)

    def test_multiple(self):
        expected = [InsnSet.X86_FMA3, InsnSet.X86_FMA4]

        self.assertEqual(expected,
                         parse_insn_sets('HAS_FMA3,HAS_FMA4').insn_sets)


class TestMergeEquivalentInsns(unittest.TestCase):

    def test_no_eq(self):
        count = InsnCount()
        count.insns = {'movapd': 3}

        merge_equivalent_insns(count)

        expected = {'movaps': 3}

        self.assertEqual(expected, count.insns)

    def test_eq_same_group(self):
        count = InsnCount()
        count.insns = {'movapd': 3, 'movaps': 2}

        merge_equivalent_insns(count)

        expected = {'movaps': 5}

        self.assertEqual(expected, count.insns)

    def test_eq_same_group_neg(self):
        count = InsnCount()
        count.insns = {'movapd': 3, 'movaps': -2}

        merge_equivalent_insns(count)

        expected = {'movaps': 1}

        self.assertEqual(expected, count.insns)

    def test_eq_different_group(self):
        count = InsnCount()
        count.insns = {'movapd': 3, 'vmovapd': 2}

        merge_equivalent_insns(count)

        expected = {'movaps': 3, 'vmovaps': 2}

        self.assertEqual(expected, count.insns)


class TestWriteResults(unittest.TestCase):

    def test_failure(self):
        desc = TestDesc('code;code', 16, ['float32<4>', 'int32<4>'])
        test = Test(desc, 'id123')

        file = StringIO()
        write_results([test], file)

        expected = '''\
[
  {"bytes": 16, "code": "code;code", "success": false, "va": "int32<4>", "vr": "float32<4>"}
]'''  # noqa: max-line-length

        self.assertEqual(expected, file.getvalue())

    def test_success(self):
        desc = TestDesc('code;code', 16, ['float32<4>', 'int32<4>'])
        test = Test(desc, 'id123')
        insns = InsnCount()
        insns.insns = {'movaps': 3, 'mulps': 2}
        test.insns = insns

        file = StringIO()
        write_results([test], file)

        expected = '''\
[
  {"bytes": 16, "code": "code;code", "va": "int32<4>", "vr": "float32<4>", "zinsns": {"movaps": 3, "mulps": 2}}
]'''  # noqa: max-line-length

        self.assertEqual(expected, file.getvalue())
