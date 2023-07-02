#!/usr/bin/env bash
curl https://bootstrap.pypa.io/get-pip.py | python
pip install pipenv
pipenv --python 3.11  # create the virtual environment
pipenv shell  # activate the virtual environment
pipenv install
pipenv install pre-commit
pre-commit install
