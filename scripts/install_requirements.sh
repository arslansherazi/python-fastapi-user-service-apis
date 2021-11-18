#!/usr/bin/env bash
curl https://bootstrap.pypa.io/get-pip.py | python
pip install pipenv
pipenv install
pre-commit install
