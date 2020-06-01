#!/usr/bin/env bash

source "./venv/bin/activate"

python invoice.py "$@"

deactivate