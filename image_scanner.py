import os
import base64
import json

class ImageScanner:
    def __init__(self):
        self.api_key = None
        self._load_api_key()
    
    def _load_api_key(self):
        """Load API key from environment variable or config file"""
        # Try environment variable first
        self.api_key = os.getenv('OPENAI_API_KEY')
        
        # If not in environment, try config file
        if not self.api_key:
            config_file = os.path.join("data", "api_config.json")
            if os.path.exists(config_file):
                try:
                    with open(config_file, 'r') as f:
                        config = json.load(f)
                        self.api_key = config.get('api_key')
                except Exception:
                    pass
    
    def scan_and_generate_recipe(self, image_path):
        """
        Scans a dish image using OpenAI Vision API and generates a recipe.
        Falls back to template if API is not available.
        """
        try:
            # Try to use OpenAI Vision API if key is available
            if self.api_key:
                try:
                    return self._analyze_with_openai(image_path)
                except Exception as e:
                    # If API fails, fall back to template
                    print(f"API call failed: {e}, using template fallback")
                    return self._generate_template_recipe(image_path)
            else:
                # No API key, use template
                return self._generate_template_recipe(image_path)
        except Exception as e:
            raise Exception(f"Failed to scan image: {str(e)}")
    
    def _analyze_with_openai(self, image_path):
        """
        Analyze image using OpenAI Vision API (like ChatGPT does)
        """
        try:
            from openai import OpenAI
            
            client = OpenAI(api_key=self.api_key)
            
            # Encode image to base64
            base64_image = self._encode_image_to_base64(image_path)
            
            # Prepare the prompt
            prompt = """Analyze this food dish image and generate a detailed recipe. 
            Provide the response in JSON format with the following structure:
            {
                "name": "Dish name",
                "servings": 4,
                "ingredients": ["ingredient 1 with amount", "ingredient 2 with amount", ...],
                "instructions": ["step 1", "step 2", ...]
            }
            
            Be specific about:
            - The dish name based on what you see
            - Exact ingredient amounts (use measurements like cups, tablespoons, etc.)
            - Detailed step-by-step cooking instructions
            - Estimate servings based on the portion size in the image
            
            Return ONLY valid JSON, no additional text."""
            
            # Try to use the best available vision model
            # gpt-4o is the latest, fallback to gpt-4-vision-preview if needed
            vision_models = ["gpt-4o", "gpt-4o-mini", "gpt-4-vision-preview"]
            model = vision_models[0]  # Start with the best one
            
            # Call OpenAI Vision API
            try:
                response = client.chat.completions.create(
                    model=model,
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": prompt},
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/jpeg;base64,{base64_image}"
                                    }
                                }
                            ]
                        }
                    ],
                    max_tokens=1500,
                    temperature=0.7
                )
            except Exception as model_error:
                # Try fallback models if primary fails
                if "gpt-4o" in str(model_error).lower() or "not found" in str(model_error).lower():
                    for fallback_model in vision_models[1:]:
                        try:
                            response = client.chat.completions.create(
                                model=fallback_model,
                                messages=[
                                    {
                                        "role": "user",
                                        "content": [
                                            {"type": "text", "text": prompt},
                                            {
                                                "type": "image_url",
                                                "image_url": {
                                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                                }
                                            }
                                        ]
                                    }
                                ],
                                max_tokens=1500,
                                temperature=0.7
                            )
                            model = fallback_model
                            break
                        except:
                            continue
                    else:
                        raise Exception(f"None of the vision models are available. Error: {model_error}")
                else:
                    raise
            
            # Extract and parse the response
            content = response.choices[0].message.content.strip()
            
            # Try to extract JSON from the response (in case there's extra text)
            json_start = content.find('{')
            json_end = content.rfind('}') + 1
            
            if json_start >= 0 and json_end > json_start:
                json_str = content[json_start:json_end]
                recipe = json.loads(json_str)
                
                # Validate and clean up the recipe
                recipe = self._validate_recipe(recipe)
                return recipe
            else:
                # If no JSON found, try to parse the whole response
                recipe = json.loads(content)
                recipe = self._validate_recipe(recipe)
                return recipe
                
        except ImportError:
            raise Exception("OpenAI package not installed. Install with: pip install openai")
        except json.JSONDecodeError as e:
            raise Exception(f"Failed to parse recipe from API response: {str(e)}")
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")
    
    def _validate_recipe(self, recipe):
        """Validate and ensure recipe has required fields"""
        if not isinstance(recipe, dict):
            raise ValueError("Recipe must be a dictionary")
        
        # Ensure all required fields exist
        validated = {
            'name': recipe.get('name', 'Unknown Dish'),
            'servings': int(recipe.get('servings', 4)),
            'ingredients': recipe.get('ingredients', [])
            if isinstance(recipe.get('ingredients'), list) else [],
            'instructions': recipe.get('instructions', [])
            if isinstance(recipe.get('instructions'), list) else []
        }
        
        # Ensure ingredients and instructions are lists of strings
        validated['ingredients'] = [str(ing) for ing in validated['ingredients'] if ing]
        validated['instructions'] = [str(inst) for inst in validated['instructions'] if inst]
        
        # If empty, add defaults
        if not validated['ingredients']:
            validated['ingredients'] = ["Ingredients to be determined"]
        if not validated['instructions']:
            validated['instructions'] = ["Instructions to be determined"]
        
        return validated
    
    def _encode_image_to_base64(self, image_path):
        """Encode image to base64 for API transmission"""
        with open(image_path, 'rb') as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    
    def _generate_template_recipe(self, image_path):
        """
        Generate a template recipe from image filename (fallback).
        """
        filename = os.path.basename(image_path)
        dish_name = os.path.splitext(filename)[0].replace('_', ' ').title()
        
        recipe = {
            'name': f"{dish_name}",
            'servings': 4,
            'ingredients': [
                "2 cups main ingredient (edit with actual amount)",
                "1 tablespoon seasoning (edit with actual type)",
                "1/2 cup vegetables (edit with actual type)",
                "Salt and pepper to taste",
                "2 tablespoons cooking oil"
            ],
            'instructions': [
                "Review the dish image and identify all ingredients",
                "Edit this template with the actual ingredients and amounts",
                "Add detailed cooking instructions based on the dish",
                "Adjust serving size and ingredient quantities as needed"
            ]
        }
        
        return recipe

