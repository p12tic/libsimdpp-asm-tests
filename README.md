
This repository contains tools related to assembly tests for the libsimdpp
project.

asm_collect.py
--------------

Collects instruction counts for the tests defined in `asmtest/test_list.py`.

The following invocation will update instruction counts for a particular
compiler:

`./asm_collect.py g++ <path/to/libsimdpp/checkout> --output_root=instruction_counts`

License
-------

> This program is free software: you can redistribute it and/or modify
> it under the terms of the GNU General Public License as published by
> the Free Software Foundation, either version 3 of the License, or
> (at your option) any later version.
>
> This program is distributed in the hope that it will be useful,
> but WITHOUT ANY WARRANTY; without even the implied warranty of
> MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
> GNU General Public License for more details.
>
> You should have received a copy of the GNU General Public License
> along with this program.  If not, see http://www.gnu.org/licenses/.
