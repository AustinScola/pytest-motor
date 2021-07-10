#!/bin/bash

set -eu

HERE="$(dirname "$(readlink -f "$BASH_SOURCE")")"
REPO_ROOT="$(realpath "${HERE}/..")"

cd "${REPO_ROOT}"

source "${REPO_ROOT}/scripts/library/venv.sh"
use_venv "build" frozen_build_requirements.txt

python3 setup.py sdist bdist_wheel

rm -rf pytest_motor.egg-info build
