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

from __future__ import print_function

import argparse
import os
import sys

from asmtest.asm_collect import flatten_tests_by_cat
from asmtest.asm_collect import get_name_to_insn_set_map
from asmtest.asm_collect import get_output_location_for_settings
from asmtest.asm_collect import parse_insn_sets
from asmtest.asm_collect import perform_all_tests
from asmtest.asm_collect import write_results
from asmtest.compiler import detect_compiler
from asmtest.compiler import detect_supported_insn_sets
from asmtest.test_desc import Test
from asmtest.test_desc import TestGenerator
from asmtest.test_list import get_all_tests


def generate_test_list(category_to_tests, categories):
    ret = {}
    index = 0

    if categories is None:
        tests = category_to_tests
    else:
        tests = {}
        for cat in categories:
            if cat not in category_to_tests:
                raise Exception('Category {0} does not exist'.format(cat))
            tests[cat] = category_to_tests[cat]

    for category, test_gen_list in tests.items():
        test_list = []
        for t in test_gen_list:
            if isinstance(t, TestGenerator):
                for d in t.generate():
                    test_list.append(Test(d, "id" + str(index)))
                    index += 1
            else:
                test_list.append(Test(t, "id" + str(index)))
                index += 1
        ret[category] = test_list
    return ret


def write_results_to_files(output_root, compiler, test_and_config_list):
    for config, tests_by_cat in test_and_config_list:
        for cat in sorted(tests_by_cat.keys()):
            test_list = tests_by_cat[cat]

            rel_path = get_output_location_for_settings(compiler, config, cat)
            out_path = os.path.join(output_root, rel_path)
            out_path_dir = os.path.dirname(out_path)

            if not os.path.exists(out_path_dir):
                os.makedirs(out_path_dir)
            with open(out_path, 'w') as out_f:
                write_results(test_list, out_f)


def main():
    parser = argparse.ArgumentParser(prog='asm_collect')
    parser.add_argument(
        'cxx', type=str,
        help='Path to the compiler')
    parser.add_argument(
        'libsimdpp', type=str,
        help='Path to the libsimdpp library')
    parser.add_argument(
        '--instr_sets', type=str, default=None,
        help='Instruction sets to test. If not specified, attempts to ' +
        'detect supported instruction sets and tests them all. ' +
        'Allowed values: {0}'.format(
            ', '.join(get_name_to_insn_set_map().keys())))
    parser.add_argument(
        '--categories', type=str, default=None,
        help='Comma-separated list of test categories to generate results '
             'for.')
    parser.add_argument(
        '--tests_per_file', type=int, default=1000,
        help='The number of tests per single compiled file')
    parser.add_argument(
        '--output_root', type=str, default=None,
        help='If this option is given, saves the output to the following ' +
        'location: <output_root>/<compiler_id>/' +
        '<category>_<arch>_<enabled_insn_sets>.json. ' +
        'Missing directories are created if needed.')
    args = parser.parse_args()

    compiler = detect_compiler(args.cxx)
    if compiler is None:
        print('Could not detect compiler')
        sys.exit(1)

    if args.instr_sets is not None:
        insn_set_configs = [parse_insn_sets(args.instr_sets)]
    else:
        if args.output_root is None:
            print('Please set --output_root to test all instruction sets')
            sys.exit(1)
        insn_set_configs = detect_supported_insn_sets(args.libsimdpp, compiler)

        print('Supported instruction sets:')
        for config in insn_set_configs:
            lines = [','.join(config.short_ids()) + ':']
            lines += [('    ' + cap) for cap in config.capabilities]
            print('\n'.join(lines))

    categories = None
    if args.categories is not None:
        categories = args.categories.split(',')

    test_and_config_list = [(config,
                             generate_test_list(get_all_tests(config),
                                                categories)
                             ) for config in insn_set_configs]

    perform_all_tests(args.libsimdpp, compiler, test_and_config_list,
                      args.tests_per_file)

    if args.output_root:
        write_results_to_files(args.output_root, compiler,
                               test_and_config_list)
    else:
        write_results(flatten_tests_by_cat(test_and_config_list[0][1]),
                      sys.stdout)


if __name__ == "__main__":
    main()
