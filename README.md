# Chef's Recipe Assistant

A comprehensive desktop application for chefs to manage recipes, scan dishes, and calculate bulk ingredient amounts for large-scale cooking.

## Features

1. **Dish Scanner**: Upload images of dishes and generate recipes automatically
2. **Recipe Manager**: Create, edit, and manage your recipe collection
3. **Bulk Calculator**: Scale recipes to any number of servings with automatic ingredient calculations

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python main.py
```

## Building Executable (.exe)

To create a standalone Windows executable:

1. Install PyInstaller (if not already installed):
```bash
pip install pyinstaller
```

2. Build the executable:
```bash
pyinstaller --onefile --windowed --name "ChefRecipeAssistant" --icon=NONE main.py
```

The executable will be created in the `dist` folder.

### Advanced Build Options

For a more optimized build with an icon:
```bash
pyinstaller --onefile --windowed --name "ChefRecipeAssistant" --icon=icon.ico --add-data "data;data" main.py
```

## Usage

### Scanning Dishes
1. Go to the "Scan Dish" tab
2. Click "Select Image" and choose a dish photo
3. Click "Scan Dish" to generate a recipe
4. Review and edit the generated recipe
5. Click "Save Recipe" to add it to your collection

### Managing Recipes
1. Go to the "Recipe Manager" tab
2. Select a recipe from the list to view/edit
3. Click "New Recipe" to create a recipe manually
4. Edit ingredients and instructions
5. Click "Save Recipe" to save changes
6. Use "Delete Recipe" to remove recipes

### Bulk Calculations
1. Go to the "Bulk Calculator" tab
2. Select a recipe from the dropdown
3. Enter the target number of servings
4. Click "Calculate" to see scaled ingredients
5. Export or print the ingredient list

## Recipe Format

Recipes are stored in JSON format in the `data/recipes.json` file. Each recipe contains:
- `name`: Recipe name
- `servings`: Number of servings
- `ingredients`: List of ingredient strings
- `instructions`: List of cooking instructions

## Image Scanning (ChatGPT-style Recognition)

The image scanner now uses **OpenAI's Vision API** to analyze dish images and generate recipes, just like ChatGPT does when you upload images.

### Quick Setup

1. **Get OpenAI API Key**: Sign up at https://platform.openai.com/api-keys
2. **Set API Key** (choose one method):
   - **Environment Variable** (recommended): `export OPENAI_API_KEY=your-key`
   - **Config File**: Create `data/api_config.json` with `{"api_key": "your-key"}`
3. **Install OpenAI package**: `pip install openai`

See `SETUP_IMAGE_RECOGNITION.md` for detailed setup instructions.

### Features

- ✅ Real AI image recognition (not templates)
- ✅ Automatically identifies dish names
- ✅ Extracts ingredients with measurements
- ✅ Generates cooking instructions
- ✅ Falls back to template if API unavailable
- ✅ Works offline with template fallback

**Note**: API usage costs ~$0.01-0.03 per image. The app works without API key using templates.

## Notes

- All recipes are saved locally in the `data` folder
- The application automatically creates the data directory on first run
- Ingredient scaling handles fractions, decimals, and common units
- The bulk calculator supports scaling to any number of servings

## Troubleshooting

- If images don't load, ensure they are in supported formats (JPG, PNG, BMP, GIF)
- If recipes don't save, check that the `data` folder has write permissions
- For executable issues, ensure all dependencies are included in the build

## License

This project is provided as-is for educational and personal use.

