#!/bin/bash

set -eu

HERE="$(dirname "$(readlink -f "$BASH_SOURCE")")"
REPO_ROOT="$(realpath "${HERE}/..")"
DISTRIBUTION_DIRECTORY="${REPO_ROOT}/dist"

VERSION_FILE="${REPO_ROOT}/VERSION.txt"
VERSION="$(cat "${VERSION_FILE}")"

WHEEL="${DISTRIBUTION_DIRECTORY}/pytest_motor-${VERSION}-py3-none-any.whl"
SOURCE_DISTRIBUTION="${DISTRIBUTION_DIRECTORY}/pytest-motor-${VERSION}.tar.gz"

# Check that the API token has been provided.
set +u
if [[ -z "${PYPI_TOKEN}" ]]; then
    echo "ERROR: PyPI API token not set. Please provide it as an environment varibale."
    exit 1
fi
set -u

source "${REPO_ROOT}/scripts/library/venv.sh"
use_venv deployment frozen_deployment_requirements.txt

python3 -m twine upload \
    --non-interactive \
    --username __token__ \
    --password "${PYPI_TOKEN}" \
    "${WHEEL}" "${SOURCE_DISTRIBUTION}"
