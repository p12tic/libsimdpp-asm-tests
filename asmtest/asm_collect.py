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

import os

from asmtest.insn_set import InsnSet
from asmtest.insn_set import InsnSetConfig


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
