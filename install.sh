#!/usr/bin/env bash

virtualenv venv
source "./venv/bin/activate"

pip install chevron
pip install simple-term-menu

deactivate