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

import re


class AsmFunction:

    ''' Defines a function parsed from compiler output. Stores a list of
        parsed instruction names and function name
    '''

    def __init__(self, name, insns=None):
        self.name = name
        self.insns = []
        if insns is not None:
            self.insns = insns

    def add(self, insn_name):
        self.insns.append(insn_name)

    def __eq__(self, other):
        if not isinstance(other, AsmFunction):
            return NotImplemented

        return self.__dict__ == other.__dict__

    def __repr__(self):
        insns = ','.join(self.insns)
        return f'AsmFunction(name={self.name}, insns=[{insns}])'


def parse_instruction(line):
    if line[0] not in ' \t':
        return None
    parts = line.split()
    if len(parts) == 0:
        return None
    if parts[0][0] == '.':
        return None  # a directive
    return parts[0]


def parse_function_name(line):
    # may be a function name
    m = re.match(r'(\w*):.*', line)
    if m is not None:
        return m.group(1)

    m = re.match(r'_(\w*)\s*PROC.*', line)
    if m is not None:
        return m.group(1)

    return None


def parse_compiler_asm_output(output):
    ''' Parses given compiler output string to a list of AsmFunction
    '''
    lines = output.split("\n")

    functions = []
    cur_function = None

    for line in lines:
        if len(line) == 0:
            continue

        insn = parse_instruction(line)
        if insn:
            if cur_function is None:
                continue
            cur_function.add(insn)
        else:
            function_name = parse_function_name(line)
            if function_name is not None:
                if cur_function is not None:
                    functions.append(cur_function)
                cur_function = AsmFunction(function_name)

    if cur_function is not None:
        functions.append(cur_function)
    return functions


class InsnCount:

    ''' Represents a mapping between instruction name and instruction count.
    '''

    def __init__(self):
        self.insns = {}

    @staticmethod
    def from_insn_list(insns):
        ic = InsnCount()
        for insn in insns:
            ic.add_insn(insn)
        return ic

    def add_insn(self, insn, count=1):
        if insn in self.insns:
            self.insns[insn] += count
            if self.insns[insn] == 0:
                del self.insns[insn]
        elif count != 0:
            self.insns[insn] = count

    def sub_insn(self, insn, count=1):
        if insn in self.insns:
            self.insns[insn] -= count
            if self.insns[insn] == 0:
                del self.insns[insn]
        elif count != 0:
            self.insns[insn] = -count

    def sub(self, other):
        for insn, count in other.insns.items():
            self.sub_insn(insn, count)
