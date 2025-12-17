# Quick Start Guide

## Running the Application

1. **Install Python 3.8+** if you haven't already

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python main.py
   ```

## Building the Executable

### Windows
Double-click `build_exe.bat` or run:
```bash
build_exe.bat
```

### macOS/Linux
Run:
```bash
./build_exe.sh
```

Or manually:
```bash
pyinstaller --onefile --windowed --name "ChefRecipeAssistant" main.py
```

The executable will be in the `dist` folder.

## Using the Application

### 1. Scan a Dish
- Click "Scan Dish" tab
- Click "Select Image" and choose a dish photo
- Click "Scan Dish" to generate a recipe template
- Edit the generated recipe as needed
- Click "Save Recipe"

### 2. Create/Edit Recipes
- Click "Recipe Manager" tab
- Select a recipe from the list or click "New Recipe"
- Enter recipe name, servings, ingredients, and instructions
- Ingredients should be one per line (e.g., "2 cups flour")
- Click "Save Recipe"

### 3. Calculate Bulk Amounts
- Click "Bulk Calculator" tab
- Select a recipe from the dropdown
- Enter the target number of servings
- Click "Calculate" to see scaled ingredients
- Export or print the ingredient list

## Recipe Ingredient Format

For best scaling results, format ingredients like:
- `2 cups flour`
- `1/2 tablespoon salt`
- `1.5 pounds chicken`
- `3 teaspoons vanilla extract`

The calculator will automatically scale these amounts.

## Optional: AI Vision API Integration

To enable real dish recognition:

1. Get an API key from OpenAI (or Google Vision API)
2. Create `data/api_config.json`:
   ```json
   {
     "provider": "openai",
     "api_key": "your-actual-api-key"
   }
   ```
3. Install the API package:
   ```bash
   pip install openai
   ```
4. Restart the application

The scanner will now use AI to analyze dish images and generate accurate recipes.

## Tips

- Recipes are saved automatically in `data/recipes.json`
- You can manually edit the JSON file if needed
- The bulk calculator handles fractions, decimals, and common units
- Export ingredient lists for shopping or prep work

