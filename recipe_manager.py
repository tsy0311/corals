import json
import os

class RecipeManager:
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        self.recipes_file = os.path.join(data_dir, "recipes.json")
        self.ensure_data_dir()
        self.load_recipes()
    
    def ensure_data_dir(self):
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def load_recipes(self):
        if os.path.exists(self.recipes_file):
            try:
                with open(self.recipes_file, 'r', encoding='utf-8') as f:
                    self.recipes = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.recipes = {}
        else:
            self.recipes = {}
    
    def save_recipes(self):
        try:
            with open(self.recipes_file, 'w', encoding='utf-8') as f:
                json.dump(self.recipes, f, indent=2, ensure_ascii=False)
        except IOError as e:
            raise Exception(f"Failed to save recipes: {str(e)}")
    
    def save_recipe(self, recipe):
        name = recipe.get('name', 'Unnamed Recipe')
        # If recipe with same name exists, update it; otherwise add new
        self.recipes[name] = recipe
        self.save_recipes()
    
    def get_recipe(self, name):
        return self.recipes.get(name)
    
    def get_all_recipes(self):
        return list(self.recipes.values())
    
    def delete_recipe(self, name):
        if name in self.recipes:
            del self.recipes[name]
            self.save_recipes()
            return True
        return False

