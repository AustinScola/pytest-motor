#!/bin/bash

set -eu

./format.sh

./lint.sh

./coverage.sh

./type_check.sh
