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

import subprocess
import sys


def call_program(args, check_returncode=True, cwd=None):
    pr = subprocess.Popen(args, stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, cwd=cwd)
    out, err = pr.communicate()

    # on python2 the 'str' type only supports ascii. We don't want to limit
    # python3 users to that, but at the same time it does not make sense to
    # convert the codebase to use unicode strings.
    out_encoding = 'utf-8' if sys.version_info >= (3, 0) else 'ascii'

    if check_returncode and pr.returncode != 0:
        msg = '\ncode: {0}\nstdout:\n{1}\nstderr:\n{2}\n'.format(
            str(pr.returncode),
            out.decode(out_encoding, errors='ignore'),
            err.decode(out_encoding, errors='ignore'))
        raise Exception(msg)

    return out.decode(out_encoding, errors='ignore')
