#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/../../../.." && pwd )"

# Add project root to PYTHONPATH
export PYTHONPATH="${PROJECT_ROOT}:${PYTHONPATH:-}"

# Define paths
VENV_PATH="${SCRIPT_DIR}/venv"
PYTHON_SCRIPT="${SCRIPT_DIR}/validate.py"

# Function to create virtual environment and install dependencies
setup_venv() {
    echo "Setting up virtual environment..."
    python3 -m venv "${VENV_PATH}"
    # shellcheck source=/dev/null
    . "${VENV_PATH}/bin/activate"
    "${VENV_PATH}/bin/pip" install --quiet pyperclip
    echo "Virtual environment setup complete"
}

# Check if virtual environment exists
if [ ! -d "${VENV_PATH}" ]; then
    setup_venv
else
    # Check if the virtual environment is working and has required packages
    if ! . "${VENV_PATH}/bin/activate" 2>/dev/null || ! "${VENV_PATH}/bin/python3" -c "import pyperclip" 2>/dev/null; then
        echo "Virtual environment is broken or missing packages"
        rm -rf "${VENV_PATH}"
        setup_venv
    else
        # shellcheck source=/dev/null
        . "${VENV_PATH}/bin/activate"
    fi
fi

# Run the Python script with any arguments passed to this script
"${VENV_PATH}/bin/python3" "${PYTHON_SCRIPT}" "$@"

# Deactivate virtual environment
deactivate
