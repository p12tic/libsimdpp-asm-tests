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

from .insn_set import *

def get_code_for_file_header(insn_set_config):
    defines_lines = ""
    for define in insn_set_config.defines():
        defines_lines += "#define {0}\n".format(define)

    template = '''
{0}
#include <simdpp/simd.h>
'''
    return template.format(defines_lines)

def get_load_stmt_for_type(type, var, idx):
    return '    {0} {1} = *reinterpret_cast<const {0}*>(pa+B*{2});'.format(
            type, var, idx)

def get_store_stmt_for_type(type, var, idx):
    return '    *reinterpret_cast<{0}*>(pr+B*{2}) = {1};'.format(
            type, var, idx)

def get_code_for_single_test(test_desc, test_ident):
    template = '''\
extern "C"
const char* test_id_{1}_end(char* pr, const char* pa)
{{
    static const unsigned B = {0};
    using namespace simdpp;

{2}
    return "{1}";
}}

'''

    lines_code = []
    lines_load = []
    lines_store = []
    pa_idx = 0
    pr_idx = 0

    if test_desc.code != '':
        lines_code.append('    ' + test_desc.code)

    if test_desc.atype is not None:
        lines_load.append(get_load_stmt_for_type(test_desc.atype,
                                                 'va', pa_idx))
        pa_idx += 1
        lines_store.append(get_store_stmt_for_type(test_desc.atype,
                                                   'va', pr_idx))
        pr_idx += 1
    if test_desc.btype is not None:
        lines_load.append(get_load_stmt_for_type(test_desc.btype,
                                                 'vb', pa_idx))
        pa_idx += 1
        lines_store.append(get_store_stmt_for_type(test_desc.btype,
                                                   'vb', pr_idx))
        pr_idx += 1
    if test_desc.ctype is not None:
        lines_load.append(get_load_stmt_for_type(test_desc.ctype,
                                                 'vc', pa_idx))
        pa_idx += 1
        lines_store.append(get_store_stmt_for_type(test_desc.ctype,
                                                   'vc', pr_idx))
        pr_idx += 1
    if test_desc.rtype is not None:
        lines_load.append(get_load_stmt_for_type(test_desc.rtype,
                                                 'vr', pa_idx))
        pa_idx += 1
        lines_store.append(get_store_stmt_for_type(test_desc.rtype,
                                                   'vr', pr_idx))
        pr_idx += 1
        lines_code.append(get_store_stmt_for_type(test_desc.rtype,
                                                  'vr', pr_idx))
        pr_idx += 1

    code = '\n'.join(lines_load + lines_store + lines_code)
    return template.format(test_desc.bytes, test_ident, code)

def get_code_for_single_capability(cap):
    return '''
#ifdef SIMDPP_HAS_{0}
#if SIMDPP_HAS_{0}
extern "C" void has_{0}_cap() {{}}
#else
extern "C" void has_no_{0}_cap() {{}}
#endif
#endif
'''.format(cap)

def get_code_for_tests(insn_set_config, tests):
    parts = [ get_code_for_file_header(insn_set_config) ]
    for test in tests:
        parts.append(get_code_for_single_test(test.desc, test.ident))

    return ''.join(parts)

def get_code_for_testing_insn_set_support(insn_set_config, capabilities):
    parts = [ get_code_for_file_header(insn_set_config) ]
    for cap in capabilities:
        parts.append(get_code_for_single_capability(cap))

    return ''.join(parts)
