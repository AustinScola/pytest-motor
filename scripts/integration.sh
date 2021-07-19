#!/bin/bash

set -eu

HERE="$(dirname "$(readlink -f "$BASH_SOURCE")")"
REPO_ROOT="$(realpath "${HERE}/..")"

cd "${HERE}"

./test.sh -m integration
