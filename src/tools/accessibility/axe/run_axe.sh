#!/bin/bash

# Source the user's profile to get PATH and other environment variables
if [ -f "$HOME/.zshrc" ]; then
    # shellcheck source=/dev/null
    . "$HOME/.zshrc" >/dev/null 2>&1
elif [ -f "$HOME/.bash_profile" ]; then
    # shellcheck source=/dev/null
    . "$HOME/.bash_profile" >/dev/null 2>&1
elif [ -f "$HOME/.profile" ]; then
    # shellcheck source=/dev/null
    . "$HOME/.profile" >/dev/null 2>&1
fi

# Add common npm locations to PATH if they exist
for npm_path in "/usr/local/bin" "/opt/homebrew/bin" "$HOME/.nvm/versions/node/*/bin" "$HOME/.npm-global/bin"; do
    if [ -d "$npm_path" ]; then
        PATH="$npm_path:$PATH"
    fi
done

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/../../../.." && pwd )"

# Add project root to PYTHONPATH
export PYTHONPATH="${PROJECT_ROOT}:${PYTHONPATH:-}"

# Define paths
VENV_PATH="${SCRIPT_DIR}/venv"
PYTHON_SCRIPT="${SCRIPT_DIR}/axe_audit.py"

# Function to create virtual environment and install dependencies
setup_venv() {
    echo "Setting up virtual environment..."
    python3 -m venv "${VENV_PATH}"
    # shellcheck source=/dev/null
    . "${VENV_PATH}/bin/activate"
    "${VENV_PATH}/bin/pip" install --quiet pyperclip rich python-dotenv psutil
    # Install Windows-specific packages if on Windows
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
        "${VENV_PATH}/bin/pip" install --quiet pywin32
    fi
    echo "Virtual environment setup complete"
}

# Check if virtual environment exists
if [ ! -d "${VENV_PATH}" ]; then
    setup_venv
else
    # Check if the virtual environment is working and has required packages
    if ! . "${VENV_PATH}/bin/activate" 2>/dev/null || ! "${VENV_PATH}/bin/python3" -c "import pyperclip, rich, dotenv" 2>/dev/null; then
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