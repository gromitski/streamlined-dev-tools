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
echo ""
echo "To set up the Lighthouse audit button:"
echo "1. Create a new button in Stream Deck"
echo "2. Choose 'System: Open' action"
echo "3. Set the path to the lighthouse_audit.py script in this repository:"
echo "   - Windows: %UserProfile%\\path\\to\\streamlined-dev-tools\\src\\tools\\accessibility\\lighthouse\\lighthouse_audit.py"
echo "   - macOS: \$HOME/path/to/streamlined-dev-tools/src/tools/accessibility/lighthouse/lighthouse_audit.py"
echo "   - Linux: \$HOME/path/to/streamlined-dev-tools/src/tools/accessibility/lighthouse/lighthouse_audit.py"
echo "4. Set 'Open with' to: python3"
echo ""
echo "Note: Replace 'path/to' with the actual path where you cloned this repository" 