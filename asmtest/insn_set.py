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

import copy

class InsnSet:
    X86_SSE2 = 1 << 0
    X86_SSE3 = 1 << 1
    X86_SSSE3 = 1 << 2
    X86_SSE4_1 = 1 << 3
    X86_POPCNT = 1 << 4
    X86_AVX = 1 << 5
    X86_AVX2 = 1 << 6
    X86_FMA3 = 1 << 7
    X86_FMA4 = 1 << 8
    X86_XOP = 1 << 9
    X86_AVX512F = 1 << 10
    X86_AVX512BW = 1 << 11
    X86_AVX512DQ = 1 << 12
    X86_AVX512VL = 1 << 13
    ARM_NEON = 1 << 14

class InsnSetConfig:
    def __init__(self, insn_sets):
        self.insn_sets = insn_sets
        self.capabilities = []

    def defines(self):
        insn_set_to_predefined_macro = {
            InsnSet.X86_SSE2 : "SIMDPP_ARCH_X86_SSE2",
            InsnSet.X86_SSE3: "SIMDPP_ARCH_X86_SSE3",
            InsnSet.X86_SSSE3: "SIMDPP_ARCH_X86_SSSE3",
            InsnSet.X86_SSE4_1: "SIMDPP_ARCH_X86_SSE4_1",
            InsnSet.X86_POPCNT: "SIMDPP_ARCH_X86_POPCNT",
            InsnSet.X86_AVX: "SIMDPP_ARCH_X86_AVX",
            InsnSet.X86_AVX2: "SIMDPP_ARCH_X86_AVX2",
            InsnSet.X86_FMA3: "SIMDPP_ARCH_X86_FMA3",
            InsnSet.X86_FMA4: "SIMDPP_ARCH_X86_FMA4",
            InsnSet.X86_XOP: "SIMDPP_ARCH_X86_XOP",
            InsnSet.X86_AVX512F: "SIMDPP_ARCH_X86_AVX512F",
            InsnSet.X86_AVX512BW: "SIMDPP_ARCH_X86_AVX512BW",
            InsnSet.X86_AVX512DQ: "SIMDPP_ARCH_X86_AVX512DQ",
            InsnSet.X86_AVX512VL: "SIMDPP_ARCH_X86_AVX512VL",
            InsnSet.ARM_NEON: "SIMDPP_ARCH_ARM_NEON",
        }
        return [ insn_set_to_predefined_macro[insn_set]
                 for insn_set in self.insn_sets ]

    def short_ids(self):
        insn_sets_to_short_id = {
            InsnSet.X86_SSE2 : "sse2",
            InsnSet.X86_SSE3: "sse3",
            InsnSet.X86_SSSE3: "ssse3",
            InsnSet.X86_SSE4_1: "sse4.1",
            InsnSet.X86_AVX: "avx",
            InsnSet.X86_AVX2: "avx2",
            InsnSet.X86_FMA3: "fma3",
            InsnSet.X86_FMA4: "fma4",
            InsnSet.X86_XOP: "xop",
            InsnSet.X86_AVX512F: "avx512f",
            InsnSet.X86_AVX512BW: "avx512bw",
            InsnSet.X86_AVX512DQ: "avx512dq",
            InsnSet.X86_AVX512VL: "avx512vl",
            InsnSet.ARM_NEON: "neon",
        }
        return [ insn_sets_to_short_id[insn_set]
                 for insn_set in self.insn_sets ]

    def mask(self):
        r = 0
        for insn_set in self.insn_sets:
            r = r | insn_set
        return r

    def has_cap(self, cap):
        if cap not in get_all_capabilities():
            raise Exception('Unknown capability {0}'.format(cap))
        return cap in self.capabilities


def get_all_insn_set_configs():
    return [
        InsnSetConfig([ InsnSet.X86_SSE2 ]),
        InsnSetConfig([ InsnSet.X86_SSE3 ]),
        InsnSetConfig([ InsnSet.X86_SSSE3 ]),
        InsnSetConfig([ InsnSet.X86_SSE4_1 ]),
        InsnSetConfig([ InsnSet.X86_AVX ]),
        InsnSetConfig([ InsnSet.X86_AVX2 ]),
        InsnSetConfig([ InsnSet.X86_FMA3 ]),
        InsnSetConfig([ InsnSet.X86_FMA4 ]),
        InsnSetConfig([ InsnSet.X86_XOP ]),
        InsnSetConfig([ InsnSet.X86_AVX512F ]),
        InsnSetConfig([ InsnSet.X86_AVX, InsnSet.X86_FMA3 ]),
        InsnSetConfig([ InsnSet.X86_AVX, InsnSet.X86_FMA4 ]),
    ]

def get_all_capabilities():
    return [
        'INT8_SIMD',
        'INT16_SIMD',
        'INT32_SIMD',
        'INT64_SIMD',
        'FLOAT32_SIMD',
        'FLOAT64_SIMD',

        'FLOAT64_TO_UINT32_CONVERSION',
        'INT64_TO_FLOAT64_CONVERSION',
        'INT64_TO_FLOAT32_CONVERSION',
        'UINT64_TO_FLOAT64_CONVERSION',
        'UINT64_TO_FLOAT32_CONVERSION',
        'FLOAT32_TO_INT64_CONVERSION',
        'FLOAT32_TO_UINT64_CONVERSION',
        'FLOAT64_TO_INT64_CONVERSION',
        'FLOAT64_TO_UINT64_CONVERSION',

        'INT8_SHIFT_L_BY_VECTOR',
        'UINT8_SHIFT_L_BY_VECTOR',
        'INT16_SHIFT_L_BY_VECTOR',
        'UINT16_SHIFT_L_BY_VECTOR',
        'INT32_SHIFT_L_BY_VECTOR',
        'UINT32_SHIFT_L_BY_VECTOR',

        'INT8_SHIFT_R_BY_VECTOR',
        'UINT8_SHIFT_R_BY_VECTOR',
        'UINT16_SHIFT_R_BY_VECTOR',
        'INT16_SHIFT_R_BY_VECTOR',
        'INT32_SHIFT_R_BY_VECTOR',
        'UINT32_SHIFT_R_BY_VECTOR',
    ]
