HERE="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
REPO_ROOT="$(realpath "${HERE}/..")"
REQUIREMENTS_DIRECTORY="${REPO_ROOT}/requirements"
FROZEN_REQUIREMENTS_DIRECTORY="${REQUIREMENTS_DIRECTORY}/frozen"

source "${REPO_ROOT}/scripts/library/string.sh"
source "${REPO_ROOT}/scripts/library/venv.sh"

function freeze_requirements() {
    local REQUIREMENTS_FILE_PATH="$1"
    echo "Freezing '${REQUIREMENTS_FILE_PATH}'..."

    local VENV_NAME="$(get_venv_name_from_requirements_file "${REQUIREMENTS_FILE_PATH}")"
    echo "Using virtual environment name '${VENV_NAME}'."

    local REQUIREMENTS_FILE="$(basename "${REQUIREMENTS_FILE_PATH}")"
    use_clean_venv "${VENV_NAME}" "${REQUIREMENTS_FILE}"

    local FROZEN_REQUIREMENTS="$(get_frozen_requirements)"

    deactivate_venv

    FROZEN_REQUIREMENTS_FILE_NAME="frozen_${REQUIREMENTS_FILE}"
    FROZEN_REQUIREMENTS_FILE_PATH="${FROZEN_REQUIREMENTS_DIRECTORY}/${FROZEN_REQUIREMENTS_FILE_NAME}"

    touch "${FROZEN_REQUIREMENTS_FILE_PATH}"
    echo "${FROZEN_REQUIREMENTS}" > "${FROZEN_REQUIREMENTS_FILE_PATH}"

    echo "Done freezing requirements for '${REQUIREMENTS_FILE_PATH}'."
}

REQUIREMENTS_FILE_PATHS="$(find "${REQUIREMENTS_DIRECTORY}" -maxdepth 1 -name "*_requirements.txt")"

NUMBER_OF_REQUIREMENTS_FILE_PATHS="$(number_of_lines "${REQUIREMENTS_FILE_PATHS}")"

echo "Found ${NUMBER_OF_REQUIREMENTS_FILE_PATHS} requirements files to freeze."

for_each_line "${REQUIREMENTS_FILE_PATHS}" freeze_requirements
