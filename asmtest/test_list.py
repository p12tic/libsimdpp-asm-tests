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

def get_all_tests(config):
    # Returns a dict with test categories as keys and list of tests or test
    # generators as values

    # We are using the following shorthands to make the test list less verbose
    # Note that type lists may include other lists, the TestGenerator class
    # will flatten them.
    b = [16, 32, 64]

    # 1xB width vectors
    i8 = 'int8<B>'
    i16 = 'int16<B/2>'
    i32 = 'int32<B/4>'
    i64 = 'int64<B/8>'
    u8 = 'uint8<B>'
    u16 = 'uint16<B/2>'
    u32 = 'uint32<B/4>'
    u64 = 'uint64<B/8>'
    f32 = 'float32<B/4>'
    f64 = 'float64<B/8>'

    mi8 = 'mask_int8<B>'
    mi16 = 'mask_int16<B/2>'
    mi32 = 'mask_int32<B/4>'
    mi64 = 'mask_int64<B/8>'
    mf32 = 'mask_float32<B/4>'
    mf64 = 'mask_float64<B/8>'

    i8_2 =   [ (i8,   i8)   ] if config.has_int8() else []
    u8_2 =   [ (u8,   u8)   ] if config.has_int8() else []
    mi8_2 =  [ (mi8,  mi8)  ] if config.has_int8() else []
    i16_2 =  [ (i16,  i16)  ] if config.has_int16() else []
    u16_2 =  [ (u16,  u16)  ] if config.has_int16() else []
    mi16_2 = [ (mi16, mi16) ] if config.has_int16() else []
    i32_2 =  [ (i32,  i32)  ] if config.has_int32() else []
    u32_2 =  [ (u32,  u32)  ] if config.has_int32() else []
    mi32_2 = [ (mi32, mi32) ] if config.has_int32() else []
    i64_2 =  [ (i64,  i64)  ] if config.has_int64() else []
    u64_2 =  [ (u64,  u64)  ] if config.has_int64() else []
    mi64_2 = [ (mi64, mi64) ] if config.has_int64() else []
    f32_2 =  [ (f32,  f32)  ] if config.has_float32() else []
    mf32_2 = [ (mf32, mf32) ] if config.has_float32() else []
    f64_2 =  [ (f64,  f64)  ] if config.has_float64() else []
    mf64_2 = [ (mf64, mf64) ] if config.has_float64() else []

    int_2 = i8_2 + i16_2 + i32_2 + i64_2
    uint_2 = u8_2 + u16_2 + u32_2 + u64_2
    float_2 = f32_2 + f64_2
    mask_2 = mi8_2 + mi16_2 + mi32_2 + mi64_2 + mf32_2 + mf64_2

    i8_3 =   [ (i8,   i8,   i8)   ] if config.has_int8() else []
    u8_3 =   [ (u8,   u8,   u8)   ] if config.has_int8() else []
    mi8_3 =  [ (mi8,  mi8,  mi8)  ] if config.has_int8() else []
    i16_3 =  [ (i16,  i16,  i16)  ] if config.has_int16() else []
    u16_3 =  [ (u16,  u16,  u16)  ] if config.has_int16() else []
    mi16_3 = [ (mi16, mi16, mi16) ] if config.has_int16() else []
    i32_3 =  [ (i32,  i32,  i32)  ] if config.has_int32() else []
    u32_3 =  [ (u32,  u32,  u32)  ] if config.has_int32() else []
    mi32_3 = [ (mi32, mi32, mi32) ] if config.has_int32() else []
    i64_3 =  [ (i64,  i64,  i64)  ] if config.has_int64() else []
    u64_3 =  [ (u64,  u64,  u64)  ] if config.has_int64() else []
    mi64_3 = [ (mi64, mi64, mi64) ] if config.has_int64() else []
    f32_3 =  [ (f32,  f32,  f32)  ] if config.has_float32() else []
    mf32_3 = [ (mf32, mf32, mf32) ] if config.has_float32() else []
    f64_3 =  [ (f64,  f64,  f64)  ] if config.has_float64() else []
    mf64_3 = [ (mf64, mf64, mf64) ] if config.has_float64() else []

    int_3 = i8_3 + i16_3 + i32_3 + i64_3
    uint_3 = u8_3 + u16_3 + u32_3 + u64_3
    float_3 = f32_3 + f64_3
    mask_3 = mi8_3 + mi16_3 + mi32_3 + mi64_3 + mf32_3 + mf64_3

    uint_3_sc = [
        (u8, u8, 'uint32_t'),
        (u16, u16, 'uint32_t'),
        (u32, u32, 'uint32_t'),
        (u64, u64, 'uint64_t'),
    ]

    float_3_sc = [
        (f32, f32, 'float'),
        (f64, f64, 'double'),
    ]

    # 2xB wide vectors
    i8_x2 = 'int8<B*2>'
    i16_x2 = 'int16<B>'
    i32_x2 = 'int32<B/2>'
    i64_x2 = 'int64<B/4>'
    u8_x2 = 'uint8<B*2>'
    u16_x2 = 'uint16<B>'
    u32_x2 = 'uint32<B/2>'
    u64_x2 = 'uint64<B/4>'
    f32_x2 = 'float32<B/2>'
    f64_x2 = 'float64<B/4>'

    mi8_x2 = 'mask_int8<B*2>'
    mi16_x2 = 'mask_int16<B>'
    mi32_x2 = 'mask_int32<B/2>'
    mi64_x2 = 'mask_int64<B/4>'
    mf32_x2 = 'mask_float32<B/2>'
    mf64_x2 = 'mask_float64<B/4>'

    # 4xB wide vectors
    i8_x4 = 'int8<B*4>'
    i16_x4 = 'int16<B*2>'
    i32_x4 = 'int32<B>'
    i64_x4 = 'int64<B/2>'
    u8_x4 = 'uint8<B*4>'
    u16_x4 = 'uint16<B*2>'
    u32_x4 = 'uint32<B>'
    u64_x4 = 'uint64<B/2>'
    f32_x4 = 'float32<B>'
    f64_x4 = 'float64<B/2>'

    mi8_x4 = 'mask_int8<B*4>'
    mi16_x4 = 'mask_int16<B*2>'
    mi32_x4 = 'mask_int32<B>'
    mi64_x4 = 'mask_int64<B/2>'
    mf32_x4 = 'mask_float32<B>'
    mf64_x4 = 'mask_float64<B/2>'

    # 8xB wide vectors
    i8_x8 = 'int8<B*8>'
    i16_x8 = 'int16<B*4>'
    i32_x8 = 'int32<B*2>'
    i64_x8 = 'int64<B>'
    u8_x8 = 'uint8<B*8>'
    u16_x8 = 'uint16<B*4>'
    u32_x8 = 'uint32<B*2>'
    u64_x8 = 'uint64<B>'
    f32_x8 = 'float32<B*2>'
    f64_x8 = 'float64<B>'

    mi8_x8 = 'mask_int8<B*8>'
    mi16_x8 = 'mask_int16<B*4>'
    mi32_x8 = 'mask_int32<B*2>'
    mi64_x8 = 'mask_int64<B>'
    mf32_x8 = 'mask_float32<B*2>'
    mf64_x8 = 'mask_float64<B>'

    TG = TestGenerator
    CC = CodeCombinator

    ret = {}

    # use a function to add tests to ensure that we don't accidentally
    # overwrite category
    def add(category, tests):
        if category not in ret:
            ret[category] = tests
        else:
            ret[category] += tests

    bitwise_types = uint_3 + float_3 + mask_3 + [
        [ ( u8, u8, mi8 ) ] if config.has_int8() else [],
        [ ( u16, u16, mi16 ) ] if config.has_int16() else [],
        [ ( u32, u32, mi32 ) ] if config.has_int32() else [],
        [ ( u64, u64, mi64 ) ] if config.has_int64() else [],
        [ ( f32, f32, mf32 ) ] if config.has_float32() else [],
        [ ( f64, f64, mf64 ) ] if config.has_float64() else [],
    ]

    bitwise_sc_constant_types = uint_2 + float_2 + mask_2
    bitwise_sc_value_types = uint_3_sc + [
        [ ( f32, f32, 'uint32_t' ) ] if config.has_int32() else [],
        [ ( f64, f64, 'uint64_t' ) ] if config.has_int64() else [],
    ]

    add('bitwise', [
        TG('vr = bit_and(va, vb);', b, bitwise_types + bitwise_sc_value_types),
        TG('vr = bit_andnot(va, vb);', b,
            bitwise_types + bitwise_sc_value_types),
        TG('vr = bit_or(va, vb);', b, bitwise_types + bitwise_sc_value_types),
        TG('vr = bit_xor(va, vb);', b, bitwise_types + bitwise_sc_value_types),
        TG('vr = bit_not(va);', b, [ uint_2, float_2, mask_2 ]),
    ])

    add('math', [
        TG('vr = add(va, vb);', b, uint_3 + float_3 + uint_3_sc + float_3_sc),
        TG('vr = va + vb;', b, uint_3 + float_3 + uint_3_sc + float_3_sc),
        TG('vr = sub(va, vb);', b, uint_3 + float_3 + uint_3_sc + float_3_sc),
        TG('vr = va - vb;', b, uint_3 + float_3 + uint_3_sc + float_3_sc),
        TG('vr = add_sat(va, vb);', b, i8_3 + u8_3 + i16_3 + u16_3),
        TG('vr = sub_sat(va, vb);', b, i8_3 + u8_3 + i16_3 + u16_3),

        TG('vr = mul(va, vb);', b, float_3 + float_3_sc),
        TG('vr = mul_lo(va, vb);', b, i16_3 + u16_3 + i32_3 + u32_3),
        TG('vr = mul_hi(va, vb);', b, i16_3 + u16_3),

        TG('vr = div(va, vb);', b, float_3),

        TG('vr = neg(va);', b, int_2 + float_2),
        # TG('vr = -va;', b, int_2 + float_2), TODO

        TG('vr = add(va, 123);', b, uint_2 + float_2),
        TG('vr = va + 123;', b, uint_2 + float_2),
        TG('vr = sub(va, 123);', b, uint_2 + float_2),
        TG('vr = va - 123;', b, uint_2 + float_2),
        TG('vr = mul(va, 1213);', b, float_2),
        TG('vr = mul_lo(va, 123);', b, i16_2 + u16_2 + i32_2 + u32_2),
        TG('vr = mul_hi(va, 123);', b, i16_2 + u16_2),
    ])

    cmp_types = [
        [ ( mi8, i8, i8 ) ] if config.has_int8() else [],
        #( mi8, mi8, i8 ),
        #( mi8, mi8, mi8 ),
        [ ( mi16, i16, i16 ) ] if config.has_int16() else [],
        #( mi16, mi16, i16 ),
        #( mi16, mi16, mi16 ),
        [ ( mi32, i32, i32 ) ] if config.has_int32() else [],
        #( mi32, mi32, i32 ),
        #( mi32, mi32, mi32 ),
        [ ( mi64, i64, i64 ) ] if config.has_int64() else [],
        #( mi64, mi64, i64 ),
        #( mi64, mi64, mi64 ),
        [ ( mf32, f32, f32 ) ] if config.has_float32() else [],
        #( mf32, mf32, f32 ),
        #( mf32, mf32, mf32 ),
        [ ( mf64, f64, f64 ) ] if config.has_float64() else [],
        #( mf64, mf64, f64 ),
        #( mf64, mf64, mf64 ),
    ]

    shift_scalar_types = [
        [ ( i8, i8, 'unsigned' ),
          ( u8, u8, 'unsigned' ) ] if config.has_int8() else [],
        [ ( i16, i16, 'unsigned' ),
          ( u16, u16, 'unsigned' ) ] if config.has_int16() else [],
        [ ( i32, i32, 'unsigned' ),
          ( u32, u32, 'unsigned' ) ] if config.has_int32() else [],
        [ ( i64, i64, 'unsigned' ),
          ( u64, u64, 'unsigned' ) ] if config.has_int64() else [],
    ]

    shift_l_vector_types = [
        [ ( i8, i8, u8 ) ] if config.has_cap('INT8_SHIFT_L_BY_VECTOR') else [],
        [ ( u8, u8, u8 ) ] if config.has_cap('UINT8_SHIFT_L_BY_VECTOR') else [],
        [ ( i16, i16, u16 ) ] if config.has_cap('INT16_SHIFT_L_BY_VECTOR') else [],
        [ ( u16, u16, u16 ) ] if config.has_cap('UINT16_SHIFT_L_BY_VECTOR') else [],
        [ ( i32, i32, u32 ) ] if config.has_cap('INT32_SHIFT_L_BY_VECTOR') else [],
        [ ( u32, u32, u32 ) ] if config.has_cap('UINT32_SHIFT_L_BY_VECTOR') else [],
    ]

    shift_r_vector_types = [
        [ ( i8, i8, u8 ) ] if config.has_cap('INT8_SHIFT_R_BY_VECTOR') else [],
        [ ( u8, u8, u8 ) ] if config.has_cap('UINT8_SHIFT_R_BY_VECTOR') else [],
        [ ( i16, i16, u16 ) ] if config.has_cap('INT16_SHIFT_R_BY_VECTOR') else [],
        [ ( u16, u16, u16 ) ] if config.has_cap('UINT16_SHIFT_R_BY_VECTOR') else [],
        [ ( i32, i32, u32 ) ] if config.has_cap('INT32_SHIFT_R_BY_VECTOR') else [],
        [ ( u32, u32, u32 ) ] if config.has_cap('UINT32_SHIFT_R_BY_VECTOR') else [],
    ]

    reduce_int_types = [
        [ ( 'int8_t',  i8 ),
          ( 'uint8_t', u8 ) ] if config.has_int8() else [],
        [ ( 'int16_t',  i16 ),
          ( 'uint16_t', u16 ) ] if config.has_int16() else [],
        [ ( 'int32_t',  i32 ),
          ( 'uint32_t', u32 ) ] if config.has_int32() else [],
        [ ( 'int64_t',  i64 ),
          ( 'uint64_t', u64 ) ] if config.has_int64() else [],
    ]
    reduce_float_types = [
        ( 'float', f32 ),
        ( 'double', f64 ),
    ]

    add('math', [
        TG('vr = cmp_eq(va, vb);', b, cmp_types),
        TG('vr = va == vb;', b, cmp_types),
        TG('vr = cmp_neq(va, vb);', b, cmp_types),
        TG('vr = va != vb;', b, cmp_types),
        TG('vr = cmp_lt(va, vb);', b, cmp_types),
        TG('vr = va < vb;', b, cmp_types),
        TG('vr = cmp_le(va, vb);', b, cmp_types),
        TG('vr = va <= vb;', b, cmp_types),
        TG('vr = cmp_gt(va, vb);', b, cmp_types),
        TG('vr = va > vb;', b, cmp_types),
        TG('vr = cmp_ge(va, vb);', b, cmp_types),
        TG('vr = va >= vb;', b, cmp_types),

        TG('vr = avg(va, vb);', b,
            [ u8_3, i8_3, u16_3, i16_3, u32_3, i32_3 ]),
        TG('vr = avg_trunc(va, vb);', b,
            [ u8_3, i8_3, u16_3, i16_3, u32_3, i32_3 ]),

        TG('vr = abs(va);', b,
            [ [ (u8, i8) ] if config.has_int8() else [],
              [ (u16, i16) ] if config.has_int16() else [],
              [ (u32, i32) ] if config.has_int32() else [],
              [ (u64, i64) ] if config.has_int64() else [] ] + float_2),

        TG('vr = sign(va);', b, float_2),

        TG('vr = min(va, vb);', b, int_3 + uint_3 + float_3), # TODO: min might not be supported until AVX2
        TG('vr = max(va, vb);', b, int_3 + uint_3 + float_3), # TODO: max might not be supported

        TG('vr = isnan(va);', b, float_2),
        TG('vr = isnan2(va, vb);', b, float_3),

        TG('vr = sqrt(va);', b, float_2),
        TG('vr = rcp_e(va);', b, [ f32_2 ]),
        TG('vr = rcp_rh(va, vb);', b, [ f32_3 ]),
        TG('vr = rsqrt_e(va);', b, [ f32_2 ]),
        TG('vr = rsqrt_rh(va, vb);', b, [ f32_3 ]),
    ])

    add('math', [
        TG('vr = shift_l(va, vb);', b, shift_scalar_types),
        TG('vr = va << vb;', b, shift_scalar_types),
        TG('vr = shift_r(va, vb);', b, shift_scalar_types),
        TG('vr = va >> vb;', b, shift_scalar_types),

        TG('vr = shift_l(va, vb);', b, shift_l_vector_types),
        TG('vr = va << vb;', b, shift_l_vector_types),
        TG('vr = shift_r(va, vb);', b, shift_r_vector_types),
        TG('vr = va >> vb;', b, shift_r_vector_types),

        TG('vr = reduce_and(va);', b, reduce_int_types),
        TG('vr = reduce_or(va);', b, reduce_int_types),
        TG('vr = reduce_min(va);', b, reduce_int_types + reduce_float_types),
        TG('vr = reduce_max(va);', b, reduce_int_types + reduce_float_types),
        TG('vr = reduce_add(va);', b, reduce_float_types + [
            [ ( 'int16_t', i8 ),
              ( 'uint16_t', u8 ) ] if config.has_int8() else [],
            [ ( 'int32_t', i16 ),
              ( 'uint32_t', u16 ) ] if config.has_int16() else [],
            [ ( 'int32_t', i32 ),
              ( 'uint32_t', u32 ) ] if config.has_int32() else [],
            [ ( 'int64_t', i64 ),
              ( 'uint64_t', u64 ) ] if config.has_int64() else [],
        ]),
        TG('vr = reduce_mul(va);', b, reduce_float_types +[
            [ ( 'int32_t', i16 ),
              ( 'uint32_t', u16 ) ] if config.has_int16() else [],
            [ ( 'int32_t', i32 ),
              ( 'uint32_t', u32 ) ] if config.has_int32() else [],
        ]),
    ])

    def create_cvt_types(target_type):
        ret = [
            ( target_type, i8 ),
            ( target_type, u8 ),
            ( target_type, i16_x2 ),
            ( target_type, u16_x2 ),
            ( target_type, i32_x4 ),
            ( target_type, u32_x4 ),
        ]
        if (not target_type.startswith('float64<') or
            config.has_cap('INT64_TO_FLOAT64_CONVERSION')) and (
            not target_type.startswith('float32<') or
            config.has_cap('INT64_TO_FLOAT32_CONVERSION')):
            ret += [ ( target_type, i64_x8 ) ]

        if (not target_type.startswith('float64<') or
            config.has_cap('UINT64_TO_FLOAT64_CONVERSION')) and (
            not target_type.startswith('float32<') or
            config.has_cap('UINT64_TO_FLOAT32_CONVERSION')):
            ret += [ ( target_type, u64_x8 ) ]

        if (not target_type.startswith('int64<') or
            config.has_cap('FLOAT32_TO_INT64_CONVERSION')) and (
            not target_type.startswith('uint64<') or
            config.has_cap('FLOAT32_TO_UINT64_CONVERSION')):
            ret += [ ( target_type, f32_x4 ) ]

        if (not target_type.startswith('int64<') or
            config.has_cap('FLOAT64_TO_INT64_CONVERSION')) and (
            not target_type.startswith('uint64<') or
            config.has_cap('FLOAT64_TO_INT64_CONVERSION')) and (
            not target_type.startswith('uint32<') or
            config.has_cap('FLOAT64_TO_UINT32_CONVERSION')):
            ret += [ ( target_type, f64_x8 ) ]
        return ret

    add('convert', [
        TG('vr = to_int8(va);', [ 16 ], create_cvt_types(i8)),
        TG('vr = to_uint8(va);', [ 16 ], create_cvt_types(u8)),
        TG('vr = to_int16(va);', [ 16 ], create_cvt_types(i16_x2)),
        TG('vr = to_uint16(va);', [ 16 ], create_cvt_types(u16_x2)),
        TG('vr = to_int32(va);', [ 16 ], create_cvt_types(i32_x4)),
        TG('vr = to_uint32(va);', [ 16 ], create_cvt_types(u32_x4)),
        TG('vr = to_int64(va);', [ 16 ], create_cvt_types(i64_x8)),
        TG('vr = to_uint64(va);', [ 16 ], create_cvt_types(u64_x8)),
        TG('vr = to_float32(va);', [ 16 ], create_cvt_types(f32_x4)),
        TG('vr = to_float64(va);', [ 16 ], create_cvt_types(f64_x8)),
        TG('vr = to_mask(va);', b, [
            [ ( mi8, u8 )   ] if config.has_int8() else [],
            [ ( mi16, u16 ) ] if config.has_int16() else [],
            [ ( mi32, u32 ) ] if config.has_int32() else [],
            [ ( mi64, u64 ) ] if config.has_int64() else [],
            [ ( mf32, f32 ) ] if config.has_float32() else [],
            [ ( mf64, f64 ) ] if config.has_float64() else [],
        ]),
    ])

    permute_types = [
        [ ( u16, u16 ) ] if config.has_int16() else [],
        [ ( u32, u32 ) ] if config.has_int32() else [],
        [ ( u64, u64 ) ] if config.has_int64() else [],
        [ ( f32, f32 ) ] if config.has_float32() else [],
        [ ( f64, f64 ) ] if config.has_float64() else [],
        [ ( u16, mi16 ) ] if config.has_int16() else [],
        [ ( u32, mi32 ) ] if config.has_int32() else [],
        [ ( u64, mi64 ) ] if config.has_int64() else [],
        [ ( f32, mf32 ) ] if config.has_float32() else [],
        [ ( f64, mf64 ) ] if config.has_float64() else [],
    ]

    permute_bytes_types = [
        [ ( u8, u8, u8 ) ] if config.has_int8() else [],
        [ ( u16, u16, u16 ) ] if config.has_int16() else [],
        [ ( u32, u32, u32 ) ] if config.has_int32() else [],
        [ ( u64, u64, u64 ) ] if config.has_int64() else [],
        [ ( f32, f32, u32 ) ] if config.has_float32() else [],
        [ ( f64, f64, u64 ) ] if config.has_float64() else [],
    ]

    shuffle_bytes_types = [
        [ ( u8, u8, u8, u8 ) ] if config.has_int8() else [],
        [ ( u16, u16, u16, u16 ) ] if config.has_int16() else [],
        [ ( u32, u32, u32, u32 ) ] if config.has_int32() else [],
        [ ( u64, u64, u64, u64 ) ] if config.has_int64() else [],
        [ ( f32, f32, f32, u32 ) ] if config.has_float32() else [],
        [ ( f64, f64, f64, u64 ) ] if config.has_float64() else [],
    ]

    add('shuffle', [
        TG(CC('vr = shuffle4x2<{0}, {1}, {2}, {3}>(va, vb);',
            ['0', '1', '2', '3', '4', '5', '6', '7'],
            ['0', '1', '2', '3', '4', '5', '6', '7'],
            ['0', '1', '2', '3', '4', '5', '6', '7'],
            ['0', '1', '2', '3', '4', '5', '6', '7']),
            b, u32_3 + f32_3),
        TG(CC('vr = shuffle2x2<{0}, {1}>(va, vb);',
            ['0', '1', '2', '3'],
            ['0', '1', '2', '3'],
            ['0', '1', '2', '3'],
            ['0', '1', '2', '3']),
            b, u32_3 + f32_3),
        TG(CC('vr = permute2<{0}, {1}>(va);',
            ['0', '1'],
            ['0', '1'],
            ['0', '1'],
            ['0', '1']),
            b, permute_types),
        TG(CC('vr = permute4<{0}, {1}, {2}, {3}>(va);',
            ['0', '1', '2', '3'],
            ['0', '1', '2', '3'],
            ['0', '1', '2', '3'],
            ['0', '1', '2', '3']),
            [ 32, 64 ], permute_types),

        TG(CC('vr = align2<{0}>(va, vb);',
            ['0', '1', '2']),
            b, u64_3 + f64_3),
        TG(CC('vr = align4<{0}>(va, vb);',
            ['0', '1', '2', '3', '4']),
            b, u32_3 + f32_3),
        TG(CC('vr = align8<{0}>(va, vb);',
            ['0', '1', '2', '3', '4', '5', '6', '7', '8']),
            b, u16_3),
        TG(CC('vr = align16<{0}>(va, vb);',
            ['0', '1', '2', '3', '4', '5', '6', '7', '8',
             '9', '10', '11', '12', '13', '14', '15', '16']),
            b, u8_3),

        TG(CC('vr = splat2<{0}>(va);',
            ['0', '1']),
            b, u64_2 + f64_2),
        TG(CC('vr = splat4<{0}>(va);',
            ['0', '1', '2', '3']),
            b, u32_2 + f32_2),
        TG(CC('vr = splat8<{0}>(va);',
            ['0', '1', '2', '3', '4', '5', '6', '7']),
            b, u16_2),
        TG(CC('vr = splat16<{0}>(va);',
            ['0', '1', '2', '3', '4', '5', '6', '7',
             '8', '9', '10', '11', '12', '13', '14', '15']),
            b, u8_2),

        TG(CC('vr = move2_l<{0}>(va);',
            ['0', '1', '2']),
            b, u64_2 + f64_2),
        TG(CC('vr = move4_l<{0}>(va);',
            ['0', '1', '2', '3', '4']),
            b, u32_2 + f32_2),
        TG(CC('vr = move8_l<{0}>(va);',
            ['0', '1', '2', '3', '4', '5', '6', '7', '8']),
            b, u16_2),
        TG(CC('vr = move16_l<{0}>(va);',
            ['0', '1', '2', '3', '4', '5', '6', '7',
             '8', '9', '10', '11', '12', '13', '14', '15', '16']),
            b, u8_2),

        TG(CC('vr = move2_r<{0}>(va);',
            ['0', '1', '2']),
            b, u64_2 + f64_2),
        TG(CC('vr = move4_r<{0}>(va);',
            ['0', '1', '2', '3', '4']),
            b, u32_2 + f32_2),
        TG(CC('vr = move8_r<{0}>(va);',
            ['0', '1', '2', '3', '4', '5', '6', '7', '8']),
            b, u16_2),
        TG(CC('vr = move16_r<{0}>(va);',
            ['0', '1', '2', '3', '4', '5', '6', '7',
             '8', '9', '10', '11', '12', '13', '14', '15', '16']),
            b, u8_2),

        TG('vr = zip2_lo(va, vb);', b, u64_3 + f64_3),
        TG('vr = zip4_lo(va, vb);', b, u32_3 + f32_3),
        TG('vr = zip8_lo(va, vb);', b, u16_3),
        TG('vr = zip16_lo(va, vb);', b, u8_3),
        TG('vr = zip2_hi(va, vb);', b, u64_3 + f64_3),
        TG('vr = zip4_hi(va, vb);', b, u32_3 + f32_3),
        TG('vr = zip8_hi(va, vb);', b, u16_3),
        TG('vr = zip16_hi(va, vb);', b, u8_3),

        TG('vr = unzip2_lo(va, vb);', b, u64_3 + f64_3),
        TG('vr = unzip4_lo(va, vb);', b, u32_3 + f32_3),
        TG('vr = unzip8_lo(va, vb);', b, u16_3),
        TG('vr = unzip16_lo(va, vb);', b, u8_3),
        TG('vr = unzip2_hi(va, vb);', b, u64_3 + f64_3),
        TG('vr = unzip4_hi(va, vb);', b, u32_3 + f32_3),
        TG('vr = unzip8_hi(va, vb);', b, u16_3),
        TG('vr = unzip16_hi(va, vb);', b, u8_3),

        TG('vr = permute_bytes16(va, vb);', b, permute_bytes_types),
        TG('vr = permute_zbytes16(va, vb);', b, permute_bytes_types),
        TG('vr = shuffle_bytes16(va, vb, vc);', b, shuffle_bytes_types),
        TG('vr = shuffle_zbytes16(va, vb, vc);', b, shuffle_bytes_types),
    ])

    return ret
