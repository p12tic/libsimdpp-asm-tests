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


import os


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
