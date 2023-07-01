#!/usr/bin/env bash
curl https://bootstrap.pypa.io/get-pip.py | python
pip install pipenv
pipenv --python 3.11
pipenv install
pipenv install pre-commit
pre-commit install
