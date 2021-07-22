#!/bin/bash

set -eu

poetry run yapf --pir .
poetry run isort -j 0 .
