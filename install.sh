#!/usr/bin/env bash

python3 -m venv env
source "./env/bin/activate"

pip install chevron
pip install simple-term-menu

deactivate
