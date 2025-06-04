#!/bin/bash

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Determine the terminal command based on OS
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    terminal -e "python3 \"$SCRIPT_DIR/lighthouse_audit.py\" -d; read -p 'Press Enter to exit...'"
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    # Windows (Git Bash or Cygwin)
    start cmd //c "python3 \"$SCRIPT_DIR/lighthouse_audit.py\" -d && pause"
else
    # Linux (and others)
    if command -v gnome-terminal &> /dev/null; then
        gnome-terminal -- bash -c "python3 \"$SCRIPT_DIR/lighthouse_audit.py\" -d; read -p 'Press Enter to exit...'"
    elif command -v xterm &> /dev/null; then
        xterm -e "python3 \"$SCRIPT_DIR/lighthouse_audit.py\" -d; read -p 'Press Enter to exit...'"
    elif command -v konsole &> /dev/null; then
        konsole -e "python3 \"$SCRIPT_DIR/lighthouse_audit.py\" -d; read -p 'Press Enter to exit...'"
    else
        echo "No supported terminal emulator found"
        exit 1
    fi
fi 