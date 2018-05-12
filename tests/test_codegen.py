#   Copyright (C) 2018  Povilas Kanapickas <povilas@radix.lt>
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

from asmtest import *
import unittest

class TestGetCodeForSingleTest(unittest.TestCase):

    def test_null_types(self):
        expected = '''\


namespace ns_ident1 {
static const unsigned B = 20;
using namespace simdpp;

extern "C"
const char* test_id_ident1_end(char* pr, const char* pa)
{
    uint32x4 va = load(pa);
    uint32x4 vb = load(pa+B);
    uint32x4 vc = load(pa+B*2);
    uint32x4 vr = load(pa+B*3);
    store(pr, va);
    store(pr+B, vb);
    store(pr+B*2, vc);
    store(pr+B*3, vr);
    code();
    store(pr+B*4, vr);
    return "ident1";
}
}
'''
        desc = TestDesc('code();', 20, [])

        self.maxDiff = None
        self.assertEqual(expected, get_code_for_single_test(desc, 'ident1'))

    def test_1_vector_type(self):
        expected = '''\


namespace ns_ident1 {
static const unsigned B = 20;
using namespace simdpp;

extern "C"
const char* test_id_ident1_end(char* pr, const char* pa)
{
    uint32x4 va = load(pa);
    uint32x4 vb = load(pa+B);
    uint32x4 vc = load(pa+B*2);
    float32<4> vr = load(pa+B*3);
    store(pr, va);
    store(pr+B, vb);
    store(pr+B*2, vc);
    store(pr+B*3, vr);
    code();
    store(pr+B*4, vr);
    return "ident1";
}
}
'''
        desc = TestDesc('code();', 20, ['float32<4>'])

        self.maxDiff = None
        self.assertEqual(expected, get_code_for_single_test(desc, 'ident1'))

    def test_4_vector_types(self):
        expected = '''\


namespace ns_ident1 {
static const unsigned B = 20;
using namespace simdpp;

extern "C"
const char* test_id_ident1_end(char* pr, const char* pa)
{
    uint32<16> va = load(pa);
    uint16<16> vb = load(pa+B);
    uint8<16> vc = load(pa+B*2);
    float32<4> vr = load(pa+B*3);
    store(pr, va);
    store(pr+B, vb);
    store(pr+B*2, vc);
    store(pr+B*3, vr);
    code();
    store(pr+B*4, vr);
    return "ident1";
}
}
'''
        desc = TestDesc('code();', 20, ['float32<4>', 'uint32<16>',
                                        'uint16<16>', 'uint8<16>'])

        self.maxDiff = None
        self.assertEqual(expected, get_code_for_single_test(desc, 'ident1'))

    def test_vector_no_rtype(self):
        expected = '''\


namespace ns_ident1 {
static const unsigned B = 20;
using namespace simdpp;

extern "C"
const char* test_id_ident1_end(char* pr, const char* pa)
{
    uint32<16> va = load(pa);
    uint16<16> vb = load(pa+B);
    uint8<16> vc = load(pa+B*2);
    uint32x4 vr = load(pa+B*3);
    store(pr, va);
    store(pr+B, vb);
    store(pr+B*2, vc);
    store(pr+B*3, vr);
    code();
    store(pr+B*4, vr);
    return "ident1";
}
}
'''
        desc = TestDesc('code();', 20, [None, 'uint32<16>',
                                        'uint16<16>', 'uint8<16>'])

        self.maxDiff = None
        self.assertEqual(expected, get_code_for_single_test(desc, 'ident1'))

    def test_scalar(self):
        expected = '''\


namespace ns_ident1 {
static const unsigned B = 20;
using namespace simdpp;

extern "C"
const char* test_id_ident1_end(char* pr, const char* pa)
{
    int va = load(pa);
    float vb = load(pa+B);
    unsigned vc = load(pa+B*2);
    long long vr = load(pa+B*3);
    store(pr, va);
    store(pr+B, vb);
    store(pr+B*2, vc);
    store(pr+B*3, vr);
    code();
    store(pr+B*4, vr);
    return "ident1";
}
}
'''
        desc = TestDesc('code();', 20, ['long long', 'int',
                                        'float', 'unsigned'])

        self.maxDiff = None
        self.assertEqual(expected, get_code_for_single_test(desc, 'ident1'))

