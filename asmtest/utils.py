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

import subprocess


def call_program(args, check_returncode=True, cwd=None):
    pr = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd)
    out, err = pr.communicate()
    if check_returncode and pr.returncode != 0:
        raise Exception("\ncode: " + str(pr.returncode) +
                        "\nstdout:\n" + out.decode("utf-8") +
                        "\nstderr:\n" + err.decode("utf-8"))
    return out.decode('utf-8', errors='ignore')
