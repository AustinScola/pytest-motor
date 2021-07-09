#!/bin/bash

set -eu

HERE="$(dirname "$(readlink -f "$BASH_SOURCE")")"
REPO_ROOT="$(realpath "${HERE}/..")"

cd "${REPO_ROOT}"

source "${REPO_ROOT}/scripts/library/venv.sh"
use_venv "format" frozen_format_requirements.txt

source "${REPO_ROOT}/scripts/library/cpus.sh"
NUMBER_OF_CPUS="$(get_number_of_cpus)"

python3 -m yapf --parallel -i -r .
python3 -m isort --jobs "${NUMBER_OF_CPUS}" .
