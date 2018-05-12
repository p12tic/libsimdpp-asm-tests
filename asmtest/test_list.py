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

from .test_desc import *

def get_all_tests():
    # Returns a dict with test categories as keys and list of tests or test
    # generators as values

    # We are using the following shorthands to make the test list less verbose
    b = [16, 32, 64]

    s8 = "int8<B>"
    s16 = "int16<B/2>"
    s32 = "int32<B/4>"
    s64 = "int64<B/8>"
    u8 = "uint8<B>"
    u16 = "uint16<B/2>"
    u32 = "uint32<B/4>"
    u64 = "uint64<B/8>"
    f32 = "float32<B/4>"
    f64 = "float64<B/8>"

    uint3 = [
        (u8, u8, u8),
        (u16, u16, u16),
        (u32, u32, u32),
        (u64, u64, u64),
    ]

    float3 = [
        (f32, f32, f32),
        (f64, f64, f64),
    ]

    TG = TestGenerator
    CC = CodeCombinator

    return {
        'math' : [
            TG("vr = add(va, vb);", b, uint3 + float3),
            TG("vr = va + vb;", b, uint3 + float3),
            TG("vr = sub(va, vb);", b, uint3 + float3),
            TG("vr = va - vb;", b, uint3 + float3),
        ],
        'shuffle' : [
            TG(CC("vr = shuffle4x2<{0}, {1}, {2}, {3}>(va, vb);",
                ["0", "1", "2", "3", "4", "5", "6", "7"],
                ["0", "1", "2", "3", "4", "5", "6", "7"],
                ["0", "1", "2", "3", "4", "5", "6", "7"],
                ["0", "1", "2", "3", "4", "5", "6", "7"]),
                b, [
                    (u32, u32, u32),
                    (f32, f32, f32),
                ]
            ),
        ],
    }
