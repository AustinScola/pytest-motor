#!/bin/bash

set -eu

poetry run pylint -j 0 --output-format=colorized pytest_motor tests
