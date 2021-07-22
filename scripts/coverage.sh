#!/bin/bash

set -eu

poetry run pytest -m unit --cov-report term-missing --cov=pytest_motor
