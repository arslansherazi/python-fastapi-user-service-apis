#!/usr/bin/env bash
curl https://bootstrap.pypa.io/get-pip.py | python
pip install pipenv
pipenv install
pip install pre-commit
pre-commit install
