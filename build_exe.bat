@echo off
echo Building Chef's Recipe Assistant Executable...
echo.

REM Check if PyInstaller is installed
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo PyInstaller not found. Installing...
    pip install pyinstaller
)

echo.
echo Creating executable...
pyinstaller --onefile --windowed --name "ChefRecipeAssistant" --add-data "data;data" main.py

echo.
echo Build complete! Check the dist folder for ChefRecipeAssistant.exe
pause

