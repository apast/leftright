#!/bin/bash

set -u
set -e

ROOT_DIR="$(dirname $0)/"

VENV_ROOT="${ROOT_DIR}venv/"

virtualenv "$VENV_ROOT"

cd $ROOT_DIR

pip install -r requirements.txt

cd "${ROOT_DIR}src"
python -m leftright -p 8080

set +e
set +u
