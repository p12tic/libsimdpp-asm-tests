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
        return 'AsmFunction(name={0}, insns=[{1}])'.format(self.name,
                ','.join(self.insns))

def parse_compiler_asm_output(output):
    ''' Parses given compiler output string to a list of AsmFunction
    '''
    lines = output.split("\n")

    functions = []
    cur_function = None

    for line in lines:
        if len(line) == 0:
            continue

        if line[0] in ' \t':
            # may be an instruction
            if cur_function is None:
                continue
            parts = line.split()
            if len(parts) == 0:
                continue
            if parts[0][0] == '.':
                continue # a directive
            cur_function.add(parts[0])
        else:
            # may be a function name
            m = re.match('(\w*):.*', line)
            if m is not None:
                function_name = m.group(1)
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
        else:
            self.insns[insn] = count

    def sub_insn(self, insn, count=1):
        if insn in self.insns:
            self.insns[insn] -= count
            if self.insns[insn] == 0:
                del self.insns[insn]
        else:
            self.insns[insn] = -count

    def sub(self, other):
        for insn, count in other.insns.items():
            self.sub_insn(insn, count)

    def merge_equivalent(self, equivalents):
        ''' Merges equivalent instructions given a list of lists of equivalent
            instructions.
        '''
        for insn_list in equivalents:
            if len(insn_list) < 2:
                continue
            preferred_insn = insn_list[0]
            for insn in insn_list:
                if insn in self.insns:
                    self.add_insn(preferred_insn, self.insns[insn])
                    del self.insns[insn]
