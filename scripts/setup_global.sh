#!/bin/bash

echo "Setting up global dependencies for Streamlined Dev Tools..."

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "npm is not installed. Please install Node.js and npm first."
    exit 1
fi

# Install Lighthouse globally
echo "Installing Lighthouse CLI globally..."
npm install -g lighthouse

# Install required Python packages globally
echo "Installing Python packages globally..."
pip3 install --break-system-packages pyperclip rich python-dotenv requests

echo "Setup complete! You can now point your Stream Deck buttons to the scripts in src/tools/"
echo "For example, to set up the Lighthouse audit button:"
echo "1. Create a new button in Stream Deck"
echo "2. Choose 'System: Open' action"
echo "3. Set the path to: $(pwd)/src/tools/accessibility/lighthouse/lighthouse_audit.py"
echo "4. Set 'Open with' to: python3" 