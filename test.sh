#!/bin/bash
flake8 --config=config/flake8rc
pylint --rcfile=config/pylintrc asmtest tests
pylint3 --rcfile=config/pylintrc asmtest tests

python -m unittest discover
python3 -m unittest discover
