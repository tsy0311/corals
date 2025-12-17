# Setting Up Image Recognition (ChatGPT-style)

The image scanner now uses OpenAI's Vision API to analyze dish images and generate recipes, just like ChatGPT does when you upload images.

## Quick Setup

### Option 1: Environment Variable (Recommended)

1. Get your OpenAI API key from https://platform.openai.com/api-keys
2. Set the environment variable:
   
   **Windows:**
   ```cmd
   set OPENAI_API_KEY=your-api-key-here
   ```
   
   **macOS/Linux:**
   ```bash
   export OPENAI_API_KEY=your-api-key-here
   ```

3. Run the application - it will automatically use the API key

### Option 2: Config File

1. Get your OpenAI API key from https://platform.openai.com/api-keys
2. Create a file: `data/api_config.json`
3. Add your API key:
   ```json
   {
     "api_key": "sk-your-actual-api-key-here"
   }
   ```
4. The application will automatically load it

## Installation

Make sure you have the OpenAI package installed:

```bash
pip install openai
```

Or install all requirements:

```bash
pip install -r requirements.txt
```

## How It Works

1. **Upload Image**: Select a dish image in the "Scan Dish" tab
2. **AI Analysis**: The image is sent to OpenAI's Vision API (GPT-4o) for analysis
3. **Recipe Generation**: The AI identifies:
   - The dish name
   - All visible ingredients with amounts
   - Cooking instructions based on the dish
   - Estimated serving size
4. **Review & Edit**: You can review and edit the generated recipe before saving

## Features

- ✅ Real image recognition (not just templates)
- ✅ Identifies dish names automatically
- ✅ Extracts ingredients with measurements
- ✅ Generates cooking instructions
- ✅ Estimates serving sizes
- ✅ Falls back to template if API is unavailable
- ✅ Works with JPG, PNG, and other image formats

## Cost

OpenAI Vision API usage is charged per image:
- GPT-4o: ~$0.01-0.03 per image (depending on image size)
- Very affordable for personal use

## Troubleshooting

**"OpenAI package not installed"**
- Run: `pip install openai`

**"API key not configured"**
- Set the `OPENAI_API_KEY` environment variable, or
- Create `data/api_config.json` with your API key

**"API call failed"**
- Check your API key is valid
- Ensure you have credits in your OpenAI account
- Check your internet connection

**Falls back to template**
- If the API fails, the app automatically uses a template recipe
- You can still edit and save it manually

## Security Note

- Never commit your API key to version control
- The `data/api_config.json` file is in `.gitignore`
- Use environment variables for production deployments

