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
from concurrent import futures

from asmtest.asm_collect import get_output_location_for_settings
from asmtest.asm_collect import merge_equivalent_insns
from asmtest.asm_collect import parse_insn_sets
from asmtest.asm_collect import parse_test_insns
from asmtest.asm_collect import perform_all_tests
from asmtest.asm_collect import write_results
from asmtest.asm_parser import InsnCount
from asmtest.compiler import CompilerBase
from asmtest.insn_set import InsnSet
from asmtest.insn_set import InsnSetConfig
from asmtest.test_desc import Test
from asmtest.test_desc import TestDesc

if sys.version_info[0] < 3:
    # io.StringIO only supports unicode strings
    import mock
    from StringIO import StringIO
else:
    from io import StringIO
    from unittest import mock  # noqa: pylint: disable=ungrouped-imports


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

    def test_does_not_leave_zero(self):
        count = InsnCount()
        count.insns = {'movapd': 3, 'movaps': -3}

        merge_equivalent_insns(count)

        self.assertEqual({}, count.insns)


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


class TestParseTestInsns(unittest.TestCase):

    def test_simple_gcc(self):

        desc = TestDesc('code;code', 16, ['float32<4>', 'int32<4>'])
        test = Test(desc, 'id123')
        test_base = Test(desc, 'id123_base')

        asm = '''\
test_id_id123_end:
    movaps
    movaps
    mov
    mov

test_id_id123_base_end:
    movapd
    movapd
    mov
'''

        parse_test_insns(asm, [test], [test_base])
        self.assertEqual({'mov': 1}, test.insns.insns)

    def test_simple_msvc(self):

        desc = TestDesc('code;code', 16, ['float32<4>', 'int32<4>'])
        test = Test(desc, 'id123')
        test_base = Test(desc, 'id123_base')

        asm = '''\
_test_id_id123_end PROC             ; COMDAT
    movaps
    movaps
    mov
    mov
_test_id_id123_end ENDP

_test_id_id123_base_end PROC        ; COMDAT
    movapd
    movapd
    mov
_test_id_id123_base_end ENDP
'''

        parse_test_insns(asm, [test], [test_base])
        self.assertEqual({'mov': 1}, test.insns.insns)


class TestPerformAllTests(unittest.TestCase):

    @mock.patch('concurrent.futures.ProcessPoolExecutor',
                side_effect=futures.ThreadPoolExecutor)
    @mock.patch('asmtest.asm_collect.perform_single_compilation')
    @mock.patch('multiprocessing.cpu_count', side_effect=lambda: 2)
    def test_split(self, _, perform_single_compilation_mock, _2):

        config1 = mock.Mock()
        config2 = mock.Mock()

        test1_1 = mock.Mock()
        test1_2 = mock.Mock()
        test2_1 = mock.Mock()
        test2_2 = mock.Mock()
        test2_3 = mock.Mock()

        test_and_config_list = [
            (config1,
             {'cat': [test1_1, test1_2]}
             ),
            (config2,
             {'cat': [test2_1, test2_2, test2_3]}
             ),
        ]

        path = 'path/to/libsimdpp'
        compiler = mock.Mock()

        stderr = StringIO()
        stdout = StringIO()

        perform_all_tests(path, compiler, test_and_config_list, 2,
                          stdout=stdout, stderr=stderr)

        expected = [
            mock.call(path, mock.ANY, compiler, config1, [test1_1, test1_2]),
            mock.call(path, mock.ANY, compiler, config2, [test2_1, test2_2]),
            mock.call(path, mock.ANY, compiler, config2, [test2_3]),
        ]

        self.assertEqual(expected,
                         perform_single_compilation_mock.call_args_list)

        expected_stdout = '''\
Using 3 threads

Compiled 2/5
Compiled 4/5
Compiled 5/5
'''
        self.assertEqual(expected_stdout, stdout.getvalue())

        expected_stderr = ''
        self.assertEqual(expected_stderr, stderr.getvalue())
