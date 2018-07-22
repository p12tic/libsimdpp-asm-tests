#!/bin/bash
flake8 --config=config/flake8rc asm_collect.py asmtest tests
pylint --rcfile=config/pylintrc asmtest tests
pylint3 --rcfile=config/pylintrc asmtest tests
python -m unittest discover
python3 -m unittest discover
isort --recursive --apply asmtest tests asm_collect.py
