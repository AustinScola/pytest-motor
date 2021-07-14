#!/bin/bash

set -eu

HERE="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

cd "${HERE}"

./format.sh

./lint.sh

./coverage.sh

./type_check.sh
