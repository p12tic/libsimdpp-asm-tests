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

import copy
import json
import multiprocessing
import os
import shutil
import sys
import tempfile
from concurrent import futures

from asmtest.asm_parser import InsnCount
from asmtest.asm_parser import parse_compiler_asm_output
from asmtest.codegen import get_code_for_tests
from asmtest.compiler import compile_code_to_asm
from asmtest.insn_set import InsnSet
from asmtest.insn_set import InsnSetConfig
from asmtest.json_utils import NoIndent
from asmtest.json_utils import NoIndentJsonEncoder
from asmtest.test_desc import group_tests_by_code
from asmtest.utils import rmtree_with_retry


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

    return os.path.join(f'{compiler.name}_{compiler_version}',
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
        function_name = f'test_id_{test.ident}_end'
        found_function = None
        for fun in functions:
            if function_name in fun.name:
                found_function = fun
                break
        if found_function is None:
            raise Exception(f'Could not find ident {test.ident}')
        test.insns = InsnCount.from_insn_list(found_function.insns)

    # subtract baseline
    for i, (test, baseline_test) in \
            enumerate(zip(test_list, baseline_test_list)):

        test.insns.sub(baseline_test.insns)
        merge_equivalent_insns(test.insns)


def split_test_list_into_chunks(test_list, tests_per_file):
    for x in range(0, len(test_list), tests_per_file):
        yield test_list[x: x + tests_per_file]


def flatten_tests_by_cat(tests_by_cat):
    ret = []
    for cat in sorted(tests_by_cat.keys()):
        ret += tests_by_cat[cat]
    return ret


def perform_single_compilation(libsimdpp_path, test_dir, compiler,
                               insn_set_config, tests_chunk):
    # compile a second copy of the tests to find out baseline number
    # of instructions that the test scaffolding emits
    tests_baseline_chunk = copy.deepcopy(tests_chunk)
    for i in tests_baseline_chunk:
        i.ident = i.ident + "_zero"
        i.desc.code = ""

    test_code = get_code_for_tests(insn_set_config,
                                   tests_chunk + tests_baseline_chunk)

    # we deliberately don't use tempfile.TemporaryDirectory() so that
    # the result of failed compilations is preserved if an exception is raised
    curr_test_dir = tempfile.mkdtemp(dir=test_dir)

    asm_output = compile_code_to_asm(libsimdpp_path, compiler,
                                     insn_set_config, test_code,
                                     curr_test_dir)

    parse_test_insns(asm_output, tests_chunk, tests_baseline_chunk)

    # MSVC likes to keep files locked even after returning control to the
    # invoking shell
    rmtree_with_retry(curr_test_dir)


def perform_all_tests(libsimdpp_path, compiler, test_and_config_list,
                      tests_per_file, stdout=sys.stdout, stderr=sys.stderr):
    num_threads = multiprocessing.cpu_count() + 1
    print(f"Using {num_threads} threads\n", file=stdout)

    with futures.ProcessPoolExecutor(max_workers=num_threads) as executor:

        # we deliberately don't use tempfile.TemporaryDirectory() so that
        # the result of failed compilations is preserved if an exception is
        # raised
        tmp_dir = tempfile.mkdtemp()

        work_futures = []

        # get the number of test cases for progress tracking
        processed_pos = 0

        for config, tests_by_cat in test_and_config_list:
            test_list = flatten_tests_by_cat(tests_by_cat)

            for tests_chunk in split_test_list_into_chunks(test_list,
                                                           tests_per_file):
                processed_pos += len(tests_chunk)
                work_futures += [
                    (processed_pos,
                     executor.submit(perform_single_compilation,
                                     libsimdpp_path,
                                     tmp_dir, compiler, config, tests_chunk)
                     )
                ]

        total_test_count = processed_pos
        for processed_pos, future in work_futures:
            try:
                future.result()
            except Exception as e:
                for _, future in work_futures:
                    future.cancel()
                print("Failed to compile...", file=stdout)
                print(e, file=stderr)
                return
            print(f'Compiled {processed_pos}/{total_test_count}', file=stdout)

        shutil.rmtree(tmp_dir)
