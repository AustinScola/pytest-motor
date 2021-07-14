#!/bin/bash

set -eu

HERE="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
REPO_ROOT="$(realpath "${HERE}/..")"

cd "${REPO_ROOT}"

source "${REPO_ROOT}/scripts/library/venv.sh"
use_venv "test" frozen_test_requirements.txt

python3 -m pytest "$@"
