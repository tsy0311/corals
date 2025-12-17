#!/bin/bash

echo "Building Chef's Recipe Assistant Executable..."
echo ""

# Check if PyInstaller is installed
if ! python -c "import PyInstaller" 2>/dev/null; then
    echo "PyInstaller not found. Installing..."
    pip install pyinstaller
fi

echo ""
echo "Creating executable..."
pyinstaller --onefile --windowed --name "ChefRecipeAssistant" --add-data "data:data" main.py

echo ""
echo "Build complete! Check the dist folder for ChefRecipeAssistant"
echo "Note: On macOS/Linux, you may need to create a .app bundle separately"

