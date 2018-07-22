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

import json
import os

from asmtest.asm_parser import InsnCount
from asmtest.asm_parser import parse_compiler_asm_output
from asmtest.insn_set import InsnSet
from asmtest.insn_set import InsnSetConfig
from asmtest.json_utils import NoIndent
from asmtest.json_utils import NoIndentJsonEncoder
from asmtest.test_desc import group_tests_by_code


def get_output_location_for_settings(compiler, insn_set_config, category):
    compiler_version = compiler.version.split('.')
    version_components = 2

    if compiler.name == 'gcc':
        if int(compiler_version[0]) >= 5:
            version_components = 1
        else:
            version_components = 2

    if compiler.name == 'clang':
        if int(compiler_version[0]) >= 4:
            version_components = 1
        else:
            version_components = 2

    # remove bugfix and minor version components if needed
    compiler_version = '.'.join(compiler_version[:version_components])

    target_arch = compiler.target_arch
    if target_arch is None:
        target_arch = 'unknown'

    short_ids = insn_set_config.short_ids()
    if len(short_ids) == 0:
        short_ids = ['none']

    return os.path.join('{0}_{1}'.format(compiler.name, compiler_version),
                        '_'.join([category, compiler.target_arch] +
                                 short_ids) + '.json')


def get_name_to_insn_set_map():
    return {
        'HAS_SSE2':     InsnSet.X86_SSE2,
        'HAS_SSE3':     InsnSet.X86_SSE3,
        'HAS_SSSE3':    InsnSet.X86_SSSE3,
        'HAS_SSE4_1':   InsnSet.X86_SSE4_1,
        'HAS_POPCNT':   InsnSet.X86_SSE4_1,
        'HAS_AVX':      InsnSet.X86_AVX,
        'HAS_AVX2':     InsnSet.X86_AVX2,
        'HAS_FMA3':     InsnSet.X86_FMA3,
        'HAS_FMA4':     InsnSet.X86_FMA4,
        'HAS_XOP':      InsnSet.X86_XOP,
        'HAS_AVX512F':  InsnSet.X86_AVX512F,
        'HAS_AVX512BW': InsnSet.X86_AVX512BW,
        'HAS_AVX512DQ': InsnSet.X86_AVX512DQ,
        'HAS_AVX512VL': InsnSet.X86_AVX512VL,
        'HAS_NEON':     InsnSet.ARM_NEON,
    }


def parse_insn_sets(insn_set_list):
    insn_id_to_insn_set = get_name_to_insn_set_map()
    insn_sets = []
    for insn_id in sorted(insn_id_to_insn_set.keys()):
        if insn_id in insn_set_list:
            insn_sets.append(insn_id_to_insn_set[insn_id])
    return InsnSetConfig(insn_sets)


def merge_equivalent_insns(insns):
    ''' This function merges the instruction counts of equivalent instructions.
        This is needed in cases the architecture supports several effectively
        equivalent instructions and the compiler is free to choose any of them.
    '''
    groups = {
        'movaps': ['movapd', 'movdqa'],
        'movups': ['movupd', 'movdqu'],
        'vmovaps': ['vmovapd', 'vmovdqa'],
        'vmovups': ['vmovupd', 'vmovdqu'],
    }

    for main_insn in groups:
        eq_insns = groups[main_insn]
        for eq_insn in eq_insns:
            if eq_insn in insns.insns:
                count = insns.insns[eq_insn]
                insns.sub_insn(eq_insn, count)
                insns.add_insn(main_insn, count)


def test_sort_key(test):
    return (test.desc.code, test.desc.bytes, test.desc.rtype,
            test.desc.atype, test.desc.btype, test.desc.ctype)


def write_results(test_list, file):
    ''' Given a list of Test instances, writes everything to a file as json.
        We want json output to be compact, but readable at the same time.
        We group tests that have the same code snippet and also disable json
        indentation for data of each individual test.
    '''
    json_data = []
    for group in group_tests_by_code(test_list):
        if len(group) > 1:
            json_group_tests = [test.to_json()
                                for test in sorted(group, key=test_sort_key)]
            for json_test in json_group_tests:
                json_test.pop('code')
            json_group = {
                'code': group[0].desc.code,
                'tests': [NoIndent(json_test)
                          for json_test in json_group_tests],
            }
            json_data.append(json_group)
        else:
            json_data.append(NoIndent(group[0].to_json()))

    json.dump(json_data, file, sort_keys=True, indent=2,
              cls=NoIndentJsonEncoder)


def parse_test_insns(asm_output, test_list, baseline_test_list):
    # The result is stored to the insns member of each object in test_list
    functions = parse_compiler_asm_output(asm_output)

    for test in test_list + baseline_test_list:
        function_name = 'test_id_{0}_end'.format(test.ident)
        found_function = None
        for fun in functions:
            if function_name in fun.name:
                found_function = fun
                break
        if found_function is None:
            raise Exception('Could not find ident {0}'.format(
                test.ident))
        test.insns = InsnCount.from_insn_list(found_function.insns)

    # subtract baseline
    for i, (test, baseline_test) in \
            enumerate(zip(test_list, baseline_test_list)):

        test.insns.sub(baseline_test.insns)
        merge_equivalent_insns(test.insns)
