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
    all_bytes = [16, 32, 64]
    uint_types = [
        ("uint8<B>", "uint8<B>", "uint8<B>"),
        ("uint16<B/2>", "uint16<B/2>", "uint16<B/2>"),
        ("uint32<B/4>", "uint32<B/4>", "uint32<B/4>"),
        ("uint64<B/8>", "uint64<B/8>", "uint64<B/8>"),
    ]
    float_types = [
        ("float32<B/4>", "float32<B/4>", "float32<B/4>"),
        ("float64<B/8>", "float64<B/8>", "float64<B/8>"),
    ]

    return [
        TestGenerator("vr = add(va, vb);", all_bytes,
                      uint_types + float_types),
        TestGenerator("vr = va + vb;", all_bytes,
                      uint_types + float_types),
        TestGenerator("vr = sub(va, vb);", all_bytes,
                      uint_types + float_types),
        TestGenerator("vr = va - vb;", all_bytes,
                      uint_types + float_types),
        TestGenerator(
            CodeCombinator("vr = shuffle4x2<{0}, {1}, {2}, {3}>(va, vb);",
                           ["0", "1", "2", "3", "4", "5", "6", "7"],
                           ["0", "1", "2", "3", "4", "5", "6", "7"],
                           ["0", "1", "2", "3", "4", "5", "6", "7"],
                           ["0", "1", "2", "3", "4", "5", "6", "7"]),
            all_bytes, [
                ("uint32<B/4>", "uint32<B/4>", "uint32<B/4>"),
                ("float32<B/4>", "float32<B/4>", "float32<B/4>"),
            ]
        ),
    ]
