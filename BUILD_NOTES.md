# Building Executable Notes

## Python Version Compatibility

### Python 3.11 and below
- PyInstaller 4.5.1 works fine
- Use the standard build scripts: `build_exe.bat` (Windows) or `build_exe.sh` (macOS/Linux)

### Python 3.12 and above
- PyInstaller 4.5.1 may have issues with the `imp` module (removed in Python 3.12+)
- **Solutions:**

#### Option 1: Use PyInstaller 6.0+ (if available)
```bash
pip install --upgrade pyinstaller
pyinstaller --onefile --windowed --name "ChefRecipeAssistant" main.py
```

#### Option 2: Use Python 3.11 for building
- Install Python 3.11 alongside your current Python
- Use Python 3.11 only for building the executable
- The application itself works fine on Python 3.12+

#### Option 3: Manual build with newer PyInstaller
Check for the latest PyInstaller version:
```bash
pip install --upgrade pyinstaller
pip install pyinstaller --upgrade --force-reinstall
```

#### Option 4: Run as Python script (no build needed)
The application works perfectly as a Python script:
```bash
python main.py
```

## Current Status

- ✅ Application runs perfectly on Python 3.15 as a script
- ⚠️ PyInstaller 4.5.1 has compatibility issues with Python 3.12+
- ✅ All core features work without building an executable

## Alternative: Use cx_Freeze or py2exe

If PyInstaller doesn't work, consider:
- **cx_Freeze**: Works with newer Python versions
- **py2exe**: Windows-specific, may have better Python 3.12+ support

## Recommendation

For Python 3.12+, the easiest approach is to:
1. Run the application directly: `python main.py`
2. Create a simple launcher script/batch file for users
3. Or use a Python distribution tool like PyInstaller 6.0+ when available

