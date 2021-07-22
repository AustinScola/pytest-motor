#!/bin/bash

set -eu

poetry run pytest "$@"
