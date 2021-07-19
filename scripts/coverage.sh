#!/bin/bash

set -eu

HERE="$(dirname "$(readlink -f "$BASH_SOURCE")")"
REPO_ROOT="$(realpath "${HERE}/..")"

cd "${REPO_ROOT}"

source "${REPO_ROOT}/scripts/library/venv.sh"
use_venv "coverage" frozen_coverage_requirements.txt

python3 -m pytest -m unit --cov=pytest_motor --cov-report  term-missing
