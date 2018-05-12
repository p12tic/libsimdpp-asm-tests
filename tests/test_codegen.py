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
extern "C"
const char* test_id_ident1_end(char* pr, const char* pa)
{
    static const unsigned B = 20;
    using namespace simdpp;

    code();
    return "ident1";
}

'''
        desc = TestDesc('code();', 20, [])

        self.maxDiff = None
        self.assertEqual(expected, get_code_for_single_test(desc, 'ident1'))

    def test_1_vector_type(self):
        expected = '''\
extern "C"
const char* test_id_ident1_end(char* pr, const char* pa)
{
    static const unsigned B = 20;
    using namespace simdpp;

    float32<4> vr = load(pa+B*0);
    store(pr+B*0, vr);
    code();
    store(pr+B*1, vr);
    return "ident1";
}

'''
        desc = TestDesc('code();', 20, ['float32<4>'])

        self.maxDiff = None
        self.assertEqual(expected, get_code_for_single_test(desc, 'ident1'))

    def test_4_vector_types(self):
        expected = '''\
extern "C"
const char* test_id_ident1_end(char* pr, const char* pa)
{
    static const unsigned B = 20;
    using namespace simdpp;

    uint32<16> va = load(pa+B*0);
    uint16<16> vb = load(pa+B*1);
    uint8<16> vc = load(pa+B*2);
    float32<4> vr = load(pa+B*3);
    store(pr+B*0, va);
    store(pr+B*1, vb);
    store(pr+B*2, vc);
    store(pr+B*3, vr);
    code();
    store(pr+B*4, vr);
    return "ident1";
}

'''
        desc = TestDesc('code();', 20, ['float32<4>', 'uint32<16>',
                                        'uint16<16>', 'uint8<16>'])

        self.maxDiff = None
        self.assertEqual(expected, get_code_for_single_test(desc, 'ident1'))

    def test_vector_no_rtype(self):
        expected = '''\
extern "C"
const char* test_id_ident1_end(char* pr, const char* pa)
{
    static const unsigned B = 20;
    using namespace simdpp;

    uint32<16> va = load(pa+B*0);
    uint16<16> vb = load(pa+B*1);
    uint8<16> vc = load(pa+B*2);
    store(pr+B*0, va);
    store(pr+B*1, vb);
    store(pr+B*2, vc);
    code();
    return "ident1";
}

'''
        desc = TestDesc('code();', 20, [None, 'uint32<16>',
                                        'uint16<16>', 'uint8<16>'])

        self.maxDiff = None
        self.assertEqual(expected, get_code_for_single_test(desc, 'ident1'))

    def test_scalar(self):
        expected = '''\
extern "C"
const char* test_id_ident1_end(char* pr, const char* pa)
{
    static const unsigned B = 20;
    using namespace simdpp;

    int va = *reinterpret_cast<const int*>(pa+B*0);
    float vb = *reinterpret_cast<const float*>(pa+B*1);
    unsigned vc = *reinterpret_cast<const unsigned*>(pa+B*2);
    long long vr = *reinterpret_cast<const long long*>(pa+B*3);
    *reinterpret_cast<int*>(pr+B*0) = va;
    *reinterpret_cast<float*>(pr+B*1) = vb;
    *reinterpret_cast<unsigned*>(pr+B*2) = vc;
    *reinterpret_cast<long long*>(pr+B*3) = vr;
    code();
    *reinterpret_cast<long long*>(pr+B*4) = vr;
    return "ident1";
}

'''
        desc = TestDesc('code();', 20, ['long long', 'int',
                                        'float', 'unsigned'])

        self.maxDiff = None
        self.assertEqual(expected, get_code_for_single_test(desc, 'ident1'))

