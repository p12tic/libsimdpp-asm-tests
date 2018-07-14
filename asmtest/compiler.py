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
import multiprocessing
import os
import re
import tempfile
from concurrent import futures

from asmtest.asm_parser import parse_compiler_asm_output
from asmtest.codegen import get_code_for_testing_insn_set_support
from asmtest.insn_set import InsnSet
from asmtest.insn_set import get_all_capabilities
from asmtest.insn_set import get_all_insn_set_configs
from asmtest.utils import call_program


class CompilerInvocation:
    def __init__(self, insn_set, simdpp_path, src_path, dst_path):
        self.insn_set = insn_set
        self.simdpp_path = simdpp_path
        self.src_path = src_path
        self.dst_path = dst_path

class CompilerBase:
    def __init__(self):
        self.name = None
        self.path = None
        self.target_arch = None
        self.version = None

    def add_insn_set_flags(self, insn_to_flags, flags, insn_sets):
        for insn_set in insn_sets:
            found = False
            for insn_set2, flags2 in insn_to_flags:
                if insn_set == insn_set2:
                    found = True
                    flags += flags2
                    break
            if not found:
                return None
        return flags

class CompilerGccBase(CompilerBase):
    def get_flags(self, invocation):
        return [
            '-c', invocation.src_path, '-o', invocation.dst_path,
            # Needed for successful compilation
            '-std=c++11', '-I' + invocation.simdpp_path,
            # Needed to get clean asm output
            '-O2', '-g0', '--save-temps', '-fomit-frame-pointer',
            '-fno-stack-protector'
        ]

class CompilerGcc(CompilerGccBase):
    def get_flags(self, invocation):
        flags = super().get_flags(invocation)
        insn_to_flags = (
            ( InsnSet.X86_SSE2, [ '-msse2' ] ),
            ( InsnSet.X86_SSE3, [ '-msse3' ] ),
            ( InsnSet.X86_SSSE3, [ '-mssse3' ] ),
            ( InsnSet.X86_POPCNT, [ '-mssse3', '-mpopcnt' ] ),
            ( InsnSet.X86_SSE4_1, [ '-msse4.1' ] ),
            ( InsnSet.X86_AVX, [ '-mavx' ] ),
            ( InsnSet.X86_AVX2, [ '-mavx2' ] ),
            ( InsnSet.X86_FMA3, [ '-mfma' ] ),
            ( InsnSet.X86_FMA4, [ '-mfma4' ] ),
            ( InsnSet.X86_XOP, [ '-mxop' ] ),
            ( InsnSet.X86_AVX512F, [ '-mavx512f' ] ),
            ( InsnSet.X86_AVX512BW, [ '-mavx512bw' ] ),
            ( InsnSet.X86_AVX512DQ, [ '-mavx512dq' ] ),
            ( InsnSet.X86_AVX512VL, [ '-mavx512vl' ] ),
            ( InsnSet.ARM_NEON, [ '-mfpu=neon' ] ),
            ( InsnSet.ARM_NEON_FLT_SP, [ '-mfpu=neon' ] ),
            ( InsnSet.ARM64_NEON, [ '-mcpu=generic+simd' ] ),
            ( InsnSet.MIPS_MSA, [ '-mips64r5', '-mmsa', '-mhard-float',
                                  '-mfp64', '-mnan=legacy' ] ),
            ( InsnSet.POWER_ALTIVEC, [ '-maltivec' ] ),
            ( InsnSet.POWER_VSX_206, [ '-mvsx' ] ),
            ( InsnSet.POWER_VSX_207, [ '-mvsx', '-mcpu=power8' ] ),
        )
        return self.add_insn_set_flags(insn_to_flags, flags,
                                   invocation.insn_set.insn_sets)

class CompilerGccIntel(CompilerGccBase):
    def get_flags(self, invocation):
        flags = super().get_flags(invocation)
        insn_to_flags = (
            ( InsnSet.X86_SSE2, [ '-msse2' ] ),
            ( InsnSet.X86_SSE3, [ '-msse3' ] ),
            ( InsnSet.X86_SSSE3, [ '-mssse3' ] ),
            ( InsnSet.X86_POPCNT, [ '-mssse3', '-mpopcnt' ] ),
            ( InsnSet.X86_SSE4_1, [ '-msse4.1' ] ),
            ( InsnSet.X86_AVX, [ '-mavx' ] ),
            ( InsnSet.X86_AVX2, [ '-xCORE-AVX2' ] ),
            ( InsnSet.X86_FMA3, [ '-xCORE-AVX2' ] ),
            ( InsnSet.X86_AVX512F, [ '-xCOMMON-AVX512' ] ),
            ( InsnSet.X86_AVX512BW, [ '-xCORE-AVX512' ] ),
            ( InsnSet.X86_AVX512VL, [ '-xCORE-AVX512' ] ),
        )
        return self.add_insn_set_flags(insn_to_flags, flags,
                                   invocation.insn_set.insn_sets)

class CompilerMsvcBase(CompilerBase):
    def get_flags(self, invocation):
        return [
            '-c', invocation.src_path, '-o', invocation.dst_path,
            # Needed for successful compilation
            '/Qstd=c++11', '/I' + invocation.simdpp_path,
            # Needed to get clean asm output
            '/O2', '-g0', '--save-temps', '/Oy',
            '/GS-'
        ]

class CompilerMsvc(CompilerMsvcBase):
    def get_flags(self, invocation):
        flags = super().get_flags(invocation)
        insn_to_flags = (
            ( InsnSet.X86_SSE2, [ '/arch:SSE2' ] ),
            ( InsnSet.X86_SSE3, [ '/arch:SSE2' ] ),
            ( InsnSet.X86_SSSE3, [ '/arch:SSE2' ] ),
            ( InsnSet.X86_POPCNT, [ '/arch:SSE4.2' ] ),
            ( InsnSet.X86_SSE4_1, [ '/arch:SSE2' ] ),
            ( InsnSet.X86_AVX, [ '/arch:AVX' ] ),
            ( InsnSet.X86_AVX2, [ '/arch:AVX' ] ),
            ( InsnSet.X86_FMA3, [ '/arch:AVX' ] ),
            ( InsnSet.X86_FMA4, [ '/arch:AVX' ] ),
        )
        return self.add_insn_set_flags(insn_to_flags, flags,
                                   invocation.insn_set.insn_sets)

class CompilerMsvcIntel(CompilerMsvcBase):
    def get_flags(self, invocation):
        flags = super().get_flags(invocation)
        insn_to_flags = (
            ( InsnSet.X86_SSE2, [ '/arch:SSE2' ] ),
            ( InsnSet.X86_SSE3, [ '/arch:SSE3' ] ),
            ( InsnSet.X86_SSSE3, [ '/arch:SSSE3' ] ),
            ( InsnSet.X86_POPCNT, [ '/arch:SSE4.2' ] ),
            ( InsnSet.X86_SSE4_1, [ '/arch:SSE4.1' ] ),
            ( InsnSet.X86_AVX, [ '/arch:AVX' ] ),
            ( InsnSet.X86_AVX2, [ '/arch:CORE-AVX2' ] ),
            ( InsnSet.X86_FMA3, [ '/arch:CORE-AVX2' ] ),
            ( InsnSet.X86_FMA4, [ '/arch:AVX' ] ),
            ( InsnSet.X86_AVX512F, [ '/arch:COMMON-AVX512' ] ),
            ( InsnSet.X86_AVX512BW, [ '/arch:CORE-AVX512' ] ),
            ( InsnSet.X86_AVX512DQ, [ '/arch:CORE-AVX512' ] ),
            ( InsnSet.X86_AVX512VL, [ '/arch:CORE-AVX512' ] ),
        )
        return self.add_insn_set_flags(insn_to_flags, flags,
                                   invocation.insn_set.insn_sets)

def detect_compiler_from_version_output(output):
    lines = output.splitlines()

    if 'g++' in lines[0]:
        m = re.match('.*\([^)]*\)\s*([\d.-]+)(?:|\s.*)', lines[0])
        if m:
            return ('gcc', m.group(1))

    m = re.match('clang version ([\d.-]+)\s.*', lines[0])
    if m:
        return ('clang', m.group(1))

    return (None, None)

def get_target_arch(compiler_path, compiler_name):
    if compiler_name in [ 'gcc', 'clang', 'gcc-intel' ]:
        try:
            out = call_program([ compiler_path, '-dumpmachine' ])
            return out.split('-')[0]
        except:
            return None
    return None

def create_compiler_by_name(name):
    cxx_name_to_compiler = {
        'gcc' : CompilerGcc,
        'clang' : CompilerGcc,
        'gcc-intel' : CompilerGccIntel,
        'msvc' : CompilerMsvc,
        'msvc-intel' : CompilerMsvcIntel,
    }
    if name not in cxx_name_to_compiler:
        raise Exception('Unknown cxx_type {0}'.format(name))
    return cxx_name_to_compiler[name]()

def detect_compiler(compiler_path):
    args_to_test = [
        [ '--version' ],
    ]

    for args in args_to_test:
        out = call_program([ compiler_path ] + args, check_returncode=False)
        name, version = detect_compiler_from_version_output(out)
        if name is not None:
            target_arch = get_target_arch(compiler_path, name)
            compiler = create_compiler_by_name(name)
            compiler.name = name
            compiler.path = compiler_path
            compiler.target_arch = target_arch
            compiler.version = version
            return compiler

    return None

def compile_code_to_asm(libsimdpp_path, compiler, insn_set_config,
                        code, test_dir):
    # returns output assembly or raises exception on error. The artifacts are
    # put into test_dir
    src_path = os.path.join(test_dir, 'test.cc')
    dst_path = os.path.join(test_dir, 'test.o')
    asm_path = os.path.join(test_dir, 'test.s')
    command_path = os.path.join(test_dir, 'compiler.cmd')

    with open(src_path, 'w') as out_f:
        out_f.write(code)

    invocation = CompilerInvocation(insn_set_config, libsimdpp_path,
                                    src_path, dst_path)

    flags = compiler.get_flags(invocation)
    cmd = [ compiler.path ] + flags

    with open(command_path, 'w') as out_f:
        out_f.write(' '.join(cmd) + '\n')

    call_program(cmd, check_returncode=True, cwd=test_dir)

    with open(asm_path, 'r') as in_f:
        return in_f.read()

def parse_supported_capabilities(asm, capabilities):
    functions = parse_compiler_asm_output(asm)
    function_names = [ f.name for f in functions ]

    supported_capabilities = []

    for cap in capabilities:
        if 'has_{0}_cap'.format(cap) in function_names:
            supported_capabilities.append(cap)
        elif 'has_no_{0}_cap'.format(cap) in function_names:
            pass
        else:
            raise Exception('Unknown capability {0}'.format(cap))
    return supported_capabilities

def detect_insn_set_support(libsimdpp_path, compiler, insn_set_config):
    with tempfile.TemporaryDirectory() as tmp_dir:
        caps = get_all_capabilities()
        code = get_code_for_testing_insn_set_support(insn_set_config, caps)
        try:
            # the following call will throw an exception if the compilation
            # fails. Unsupported instruction sets are disabled within
            # libsimdp source
            asm = compile_code_to_asm(libsimdpp_path, compiler, insn_set_config,
                                      code, tmp_dir)
        except:
            return False, []

        return True, parse_supported_capabilities(asm, caps)

def detect_supported_insn_sets(libsimdpp_path, compiler):
    supported_configs = []
    all_configs = get_all_insn_set_configs()

    num_threads = multiprocessing.cpu_count() + 1
    with futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        work_futures = [ ( config,
                           executor.submit(detect_insn_set_support,
                                           libsimdpp_path, compiler, config) )
                         for config in all_configs ]

        for config, future in work_futures:
            is_supported, capabilities = future.result()
            if is_supported:
                config = copy.deepcopy(config)
                config.capabilities = capabilities
                supported_configs.append(config)
    return supported_configs
