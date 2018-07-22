#!/bin/bash
flake8 --config=config/flake8rc
pylint --rcfile=config/pylintrc asmtest tests

python3 -m unittest discover
