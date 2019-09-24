#!/usr/bin/env bash
set -eo pipefail

python setup.py develop
pre-commit run -a
python -m pytest src/test