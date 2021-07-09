#!/bin/bash

set -eu

function _venv_exists() {
    local VENV_NAME="$1"

    local VENV_PATH="$(get_venv_path "${VENV_NAME}")"
    if [[ -d "${VENV_PATH}" ]]; then
        echo "yes"
    else
        echo "no"
    fi
}

function _make_venv() {
    local VENV_PATH="$1"
    python3 -m venv --clear "${VENV_PATH}"
}

function _activate_venv() {
    source "${VENV_PATH}/bin/activate"
}

function deactivate_venv() {
    set +u
    deactivate
    set -u
}

function _install_requirements() {
    local REQUIREMENTS_FILE_NAME="$1"
    local REQUIREMENTS_FILE_PATH="${REPO_ROOT}/requirements/${REQUIREMENTS_FILE_NAME}"
    python3 -m pip install -r "${REQUIREMENTS_FILE_PATH}"
}

function _install_frozen_requirements() {
    local FROZEN_REQUIREMENTS_FILE_NAME="$1"
    local FROZEN_REQUIREMENTS_FILE_PATH="${REPO_ROOT}/requirements/frozen/${FROZEN_REQUIREMENTS_FILE_NAME}"
    python3 -m pip install -r "${FROZEN_REQUIREMENTS_FILE_PATH}"
}

function get_venv_name_from_requirements_file() {
    local REQUIREMENTS_FILE_PATH="$1"
    local REQUIREMENTS_FILE_NAME="$(basename "${REQUIREMENTS_FILE_PATH}")"
    local VENV_NAME="$( echo "${REQUIREMENTS_FILE_NAME}" | rev | cut --delimiter=_ --fields=2- | rev)"
    echo "${VENV_NAME}"
}

function get_venv_path() {
    local VENV_NAME="$1"
    local VENV_PATH="${REPO_ROOT}/venvs/${VENV_NAME}"
    echo "${VENV_PATH}"
}

function get_frozen_requirements() {
    local FROZEN_REQUIREMENTS="$(pip freeze | sed '/pkg-resources/d')"
    echo "${FROZEN_REQUIREMENTS}"
}

function requirements_match() {
    local VENV_NAME="$1"
    local FROZEN_REQUIREMENTS_FILE_NAME="$2"

    local VENV_PATH="$(get_venv_path "${VENV_NAME}")"

    _activate_venv "${VENV_PATH}"
    local ACTUAL_FROZEN_REQUIREMENTS="$(get_frozen_requirements)"
    deactivate_venv

    local FROZEN_REQUIREMENTS_FILE_PATH="${REPO_ROOT}/requirements/frozen/${FROZEN_REQUIREMENTS_FILE_NAME}"
    local EXPECTED_FROZEN_REQUIREMENTS="$(cat "${FROZEN_REQUIREMENTS_FILE_PATH}")"

    if [[ "${ACTUAL_FROZEN_REQUIREMENTS}" == "${EXPECTED_FROZEN_REQUIREMENTS}" ]]; then
        echo "yes"
    else
        echo "no"
    fi
}

function use_clean_venv() {
    local VENV_NAME="$1"
    local REQUIREMENTS_FILE_NAME="$2"

    local VENV_PATH="$(get_venv_path "${VENV_NAME}")"

    _make_venv "${VENV_PATH}"
    _activate_venv "${VENV_PATH}"
    _install_requirements "basic_requirements.txt"
    _install_requirements "${REQUIREMENTS_FILE_NAME}"
}

function use_clean_venv_from_frozen_requirements() {
    local VENV_NAME="$1"
    local FROZEN_REQUIREMENTS_FILE_NAME="$2"

    local VENV_PATH="$(get_venv_path "${VENV_NAME}")"

    _make_venv "${VENV_PATH}"
    _activate_venv "${VENV_PATH}"
    _install_requirements "basic_requirements.txt"
    _install_frozen_requirements "${FROZEN_REQUIREMENTS_FILE_NAME}"
}

function _maybe_reuse_venv() {
    local VENV_NAME="$1"
    local FROZEN_REQUIREMENTS_FILE_NAME="$2"

    local REQUIREMENTS_MATCH="$(requirements_match "${VENV_NAME}" "${FROZEN_REQUIREMENTS_FILE_NAME}")"
    if [[ "${REQUIREMENTS_MATCH}" == "yes" ]]; then
        local VENV_PATH="$(get_venv_path "${VENV_NAME}")"
        _activate_venv "${VENV_PATH}"
    else
        use_clean_venv_from_frozen_requirements "${VENV_NAME}" "${FROZEN_REQUIREMENTS_FILE_NAME}"
    fi
}

function use_venv() {
    local VENV_NAME="$1"
    local FROZEN_REQUIREMENTS_FILE_NAME="$2"

    local VENV_EXISTS="$(_venv_exists "${VENV_NAME}" )"

    if [[ "${VENV_EXISTS}" == "yes" ]]; then
        _maybe_reuse_venv "${VENV_NAME}" "${FROZEN_REQUIREMENTS_FILE_NAME}"
    else
        use_clean_venv_from_frozen_requirements "${VENV_NAME}" "${FROZEN_REQUIREMENTS_FILE_NAME}"
    fi
}
