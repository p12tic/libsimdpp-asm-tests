#!/usr/bin/env python3

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

import argparse
import copy
import itertools
import json
import multiprocessing
import os
import shutil
import sys
import tempfile
import traceback
from concurrent import futures
from asmtest import *

def merge_equivalent_insns(insns):
    ''' This function merges the instruction counts of equivalent instructions.
        In certain casse the compiler is free to pick several instructions and
        happens to pick different ones in baseline and non-baseline case.
        This may lead to negative instruction counts when baseline instruction
        count is subtracted.
    '''
    groups = [
        ['movapd', 'movaps', 'movdqa' ],
        ['movupd', 'movups', 'movdqu' ],
        ['vmovapd', 'vmovaps', 'vmovdqa' ],
        ['vmovupd', 'vmovups', 'vmovdqu' ],
    ]

    for g in groups:
        for i in g:
            if i in insns.insns and insns.insns[i] > 0:
                for j in g:
                    if j != i and j in insns.insns and insns.insns[j] < 0:
                        diff = min(insns.insns[i], -insns.insns[j])
                        insns.insns[i] -= diff
                        insns.insns[j] += diff

def generate_test_list(tests):
    ret = []
    for t in tests:
        if isinstance(t, TestGenerator):
            for d in t.generate():
                ret.append(Test(d, "id" + str(len(ret))))
        else:
            ret.append(Test(t, "id" + str(len(ret))))
    return ret

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
    for insn_id in insn_id_to_insn_set:
        if insn_id in insn_set_list:
            insn_sets.append(insn_id_to_insn_set[insn_id])
    return InsnSetConfig(insn_sets)

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
    for i in range(0, len(test_list)):
        test_list[i].insns.sub(baseline_test_list[i].insns)
        merge_equivalent_insns(test_list[i].insns)

def perform_single_compilation(libsimdpp_path, test_dir, compiler,
                               insn_set_config, tests_chunk):
    try:
        # compile a second copy of the tests to find out baseline number
        # of instructions that the test scaffolding emits
        tests_baseline_chunk = copy.deepcopy(tests_chunk)
        for i in tests_baseline_chunk:
            i.ident = i.ident + "_zero"
            i.desc.code = ""

        test_code = get_code_for_tests(insn_set_config,
                                       tests_chunk + tests_baseline_chunk)

        # we deliberately don't use tempfile.TemporaryDirectory() so that
        # the result of failed compilations is preserved
        curr_test_dir = tempfile.mkdtemp(dir=test_dir)

        asm_output = compile_code_to_asm(libsimdpp_path, compiler,
                                         insn_set_config, test_code,
                                         curr_test_dir)

        parse_test_insns(asm_output, tests_chunk, tests_baseline_chunk)

        shutil.rmtree(curr_test_dir)

    except:
        print("Got exception...")
        traceback.print_exc()

def test_sort_key(test):
    return (test.desc.code, test.desc.bytes, test.desc.rtype,
            test.desc.atype, test.desc.btype, test.desc.ctype)

def print_results(test_list, file):
    ''' We want json output to be compact, but readable at the same time.
        We group tests that have the same code snippet and also disable json
        indentation for data of each individual test.
    '''
    json_data = []
    for group in group_tests_by_code(test_list):
        if len(group) > 1:
            json_group_tests = [ test.to_json()
                                 for test in sorted(group, key=test_sort_key) ]
            for json_test in json_group_tests:
                json_test.pop('code')
            json_group = {
                'code' : group[0].desc.code,
                'tests' : [ NoIndent(json_test)
                            for json_test in json_group_tests ],
            }
            json_data.append(json_group)
        else:
            json_data.append(NoIndent(group[0].to_json()))

    json.dump(json_data, file, sort_keys=True, indent=2,
              cls=NoIndentJsonEncoder)

def split_test_list_into_chunks(test_list, tests_per_file):
    for x in range(0, len(test_list), tests_per_file):
        yield test_list[x : x+tests_per_file]

def perform_all_tests(libsimdpp_path, compiler, test_and_config_list,
                      tests_per_file):
    num_threads = multiprocessing.cpu_count() + 1
    print("Using {0} threads\n".format(num_threads))

    with tempfile.TemporaryDirectory() as tmp_dir,\
         futures.ThreadPoolExecutor(max_workers=num_threads) as executor:

        work_futures = []

        # get the number of test cases for progress tracking
        processed_pos = 0

        for config, test_list in test_and_config_list:

            for tests_chunk in split_test_list_into_chunks(test_list,
                                                           tests_per_file):
                processed_pos += len(tests_chunk)
                work_futures += [
                    ( processed_pos,
                      executor.submit(perform_single_compilation,
                                      libsimdpp_path,
                                      tmp_dir, compiler, config, tests_chunk)
                    )
                ]

        total_test_count = processed_pos
        for processed_pos, future in work_futures:
            future.result()
            print('Compiled {0}/{1}'.format(processed_pos, total_test_count))

def get_output_location_for_settings(compiler, insn_set_config):
    # only include the major.minor versions into the compiler id
    compiler_version = '.'.join(compiler.version.split('.')[:2])

    target_arch = compiler.target_arch
    if target_arch is None:
        target_arch = 'unknown'

    short_ids = insn_set_config.short_ids()
    if len(short_ids) == 0:
        short_ids = [ 'none' ]

    return os.path.join('{0}_{1}'.format(compiler.name, compiler_version),
                        '_'.join([ compiler.target_arch ] +
                                 short_ids) + '.json')

def main():
    parser = argparse.ArgumentParser(prog='asm_collect')
    parser.add_argument('cxx', type=str,
            help='Path to the compiler')
    parser.add_argument('libsimdpp', type=str,
            help='Path to the libsimdpp library')
    parser.add_argument('--instr_sets', type=str, default=None,
            help='Instruction sets to test. If not specified, attempts to '+
                'detect supported instruction sets and tests them all. ' +
                'Allowed values: {0}'.format(
                ', '.join(get_name_to_insn_set_map().keys())))
    parser.add_argument('--tests_per_file', type=int, default=1000,
            help='The number of tests per single compiled file')
    parser.add_argument('--output_root', type=str, default=None,
            help='If this option is given, saves the output to the following '+
                'location: <output_root>/<compiler_id>/'+
                '<subcategory>_<arch>_<enabled_insn_sets>.json. '+
                'Missing directories are created if needed.')
    args = parser.parse_args()

    compiler = detect_compiler(args.cxx)
    if compiler is None:
        print('Could not detect compiler')
        sys.exit(1)

    if args.instr_sets is not None:
        insn_set_configs = [ parse_insn_sets(args.instr_sets) ]
    else:
        if args.output_root is None:
            print('Please set --output_root to test all instruction sets')
            sys.exit(1)
        insn_set_configs = detect_supported_insn_sets(args.libsimdpp, compiler)

        print('Supported instruction sets:')
        for config in insn_set_configs:
            print(','.join(config.short_ids()))

    test_list = generate_test_list(get_all_tests())

    test_and_config_list = [ ( config, copy.deepcopy(test_list) )
                             for config in insn_set_configs ]

    perform_all_tests(args.libsimdpp, compiler, test_and_config_list,
                      args.tests_per_file)

    if args.output_root:
        for config, test_list in test_and_config_list:
            out_path = os.path.join(
                    args.output_root,
                    get_output_location_for_settings(compiler, config))


            os.makedirs(os.path.dirname(out_path), exist_ok=True)
            with open(out_path, 'w') as out_f:
                print_results(test_list, out_f)
    else:
        print_results(test_list, sys.stdout)

if __name__ == "__main__":
    main()
