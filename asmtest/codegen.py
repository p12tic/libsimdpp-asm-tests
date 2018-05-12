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

def get_code_for_single_test(test_desc, test_ident):
    template = '''

namespace ns_{1} {{
static const unsigned B = {0};
using namespace simdpp;

extern "C"
const char* test_id_{1}_end(char* pr, const char* pa)
{{
    {2} va = load(pa);
    {3} vb = load(pa+B);
    {4} vc = load(pa+B*2);
    {5} vr = load(pa+B*3);
    store(pr, va);
    store(pr+B, vb);
    store(pr+B*2, vc);
    store(pr+B*3, vr);
    {6}
    store(pr+B*4, vr);
    return "{1}";
}}
}}
'''

    def handle_null_type(t):
        if t == None:
            return "uint32x4"
        return t

    rtype = handle_null_type(test_desc.rtype)
    atype = handle_null_type(test_desc.atype)
    btype = handle_null_type(test_desc.btype)
    ctype = handle_null_type(test_desc.ctype)
    return template.format(test_desc.bytes, test_ident,
                           atype, btype, ctype, rtype,
                           test_desc.code)

def get_code_for_tests(insn_set_config, tests):
    parts = [ get_code_for_file_header(insn_set_config) ]
    for test in tests:
        parts.append(get_code_for_single_test(test.desc, test.ident))

    return ''.join(parts)

def get_code_for_testing_insn_set_support(insn_set_config):
    return get_code_for_file_header(insn_set_config)
