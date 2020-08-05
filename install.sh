#!/usr/bin/env bash

# read install instructions in README.md before executing this file

python3 -m venv env
source "./env/bin/activate"

pip install chevron
pip install simple-term-menu

deactivate
