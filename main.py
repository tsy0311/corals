import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import json
import os
from PIL import Image, ImageTk
import base64
import io
from recipe_manager import RecipeManager
from image_scanner import ImageScanner
from recipe_scaler import RecipeScaler

class CookingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chef's Recipe Assistant")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f5f5f5')
        
        # Initialize managers
        self.recipe_manager = RecipeManager()
        self.image_scanner = ImageScanner()
        self.recipe_scaler = RecipeScaler()
        
        # Current recipe data
        self.current_recipe = None
        self.scanned_image_path = None
        
        self.create_widgets()
        self.load_recipes()
        
    def create_widgets(self):
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Tab 1: Recipe Scanner
        self.scanner_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.scanner_frame, text="Scan Dish")
        self.create_scanner_tab()
        
        # Tab 2: Recipe Manager
        self.recipe_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.recipe_frame, text="Recipe Manager")
        self.create_recipe_tab()
        
        # Tab 3: Bulk Calculator
        self.calculator_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.calculator_frame, text="Bulk Calculator")
        self.create_calculator_tab()
        
    def create_scanner_tab(self):
        # Left side - Image upload
        left_frame = ttk.Frame(self.scanner_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        ttk.Label(left_frame, text="Upload Dish Image", font=('Arial', 14, 'bold')).pack(pady=10)
        
        self.image_label = ttk.Label(left_frame, text="No image selected", background='white')
        self.image_label.pack(fill=tk.BOTH, expand=True, pady=10)
        
        btn_frame = ttk.Frame(left_frame)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="Select Image", command=self.select_image).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Scan Dish", command=self.scan_dish, state='disabled').pack(side=tk.LEFT, padx=5)
        self.scan_btn = btn_frame.winfo_children()[1]
        
        # Right side - Generated recipe
        right_frame = ttk.Frame(self.scanner_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        ttk.Label(right_frame, text="Generated Recipe", font=('Arial', 14, 'bold')).pack(pady=10)
        
        self.recipe_text = scrolledtext.ScrolledText(right_frame, wrap=tk.WORD, height=30, font=('Arial', 11))
        self.recipe_text.pack(fill=tk.BOTH, expand=True, pady=10)
        
        btn_frame2 = ttk.Frame(right_frame)
        btn_frame2.pack(pady=10)
        
        ttk.Button(btn_frame2, text="Save Recipe", command=self.save_scanned_recipe).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame2, text="Clear", command=self.clear_scanner).pack(side=tk.LEFT, padx=5)
        
    def create_recipe_tab(self):
        # Left side - Recipe list
        left_frame = ttk.Frame(self.recipe_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=10, pady=10, ipadx=5)
        
        ttk.Label(left_frame, text="Saved Recipes", font=('Arial', 14, 'bold')).pack(pady=10)
        
        # Recipe listbox with scrollbar
        list_frame = ttk.Frame(left_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.recipe_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set, font=('Arial', 11))
        self.recipe_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.recipe_listbox.yview)
        
        self.recipe_listbox.bind('<<ListboxSelect>>', self.on_recipe_select)
        
        btn_frame = ttk.Frame(left_frame)
        btn_frame.pack(pady=10, fill=tk.X)
        
        ttk.Button(btn_frame, text="New Recipe", command=self.new_recipe).pack(fill=tk.X, pady=2)
        ttk.Button(btn_frame, text="Save Recipe", command=self.save_recipe).pack(fill=tk.X, pady=2)
        ttk.Button(btn_frame, text="Delete Recipe", command=self.delete_recipe).pack(fill=tk.X, pady=2)
        
        # Right side - Recipe editor
        right_frame = ttk.Frame(self.recipe_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        ttk.Label(right_frame, text="Recipe Details", font=('Arial', 14, 'bold')).pack(pady=10)
        
        # Recipe name
        name_frame = ttk.Frame(right_frame)
        name_frame.pack(fill=tk.X, pady=5)
        ttk.Label(name_frame, text="Recipe Name:", width=15).pack(side=tk.LEFT)
        self.recipe_name_entry = ttk.Entry(name_frame, font=('Arial', 11))
        self.recipe_name_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Servings
        servings_frame = ttk.Frame(right_frame)
        servings_frame.pack(fill=tk.X, pady=5)
        ttk.Label(servings_frame, text="Servings:", width=15).pack(side=tk.LEFT)
        self.servings_entry = ttk.Entry(servings_frame, font=('Arial', 11))
        self.servings_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Ingredients
        ttk.Label(right_frame, text="Ingredients:", font=('Arial', 12)).pack(anchor=tk.W, pady=(10, 5))
        self.ingredients_text = scrolledtext.ScrolledText(right_frame, wrap=tk.WORD, height=15, font=('Arial', 11))
        self.ingredients_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Instructions
        ttk.Label(right_frame, text="Instructions:", font=('Arial', 12)).pack(anchor=tk.W, pady=(10, 5))
        self.instructions_text = scrolledtext.ScrolledText(right_frame, wrap=tk.WORD, height=10, font=('Arial', 11))
        self.instructions_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Save button
        ttk.Button(right_frame, text="Save Recipe", command=self.save_recipe).pack(pady=10)
        
    def create_calculator_tab(self):
        # Top frame - Recipe selection and scaling
        top_frame = ttk.Frame(self.calculator_frame)
        top_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(top_frame, text="Select Recipe:", font=('Arial', 12)).pack(side=tk.LEFT, padx=5)
        
        self.calc_recipe_var = tk.StringVar()
        self.calc_recipe_combo = ttk.Combobox(top_frame, textvariable=self.calc_recipe_var, 
                                             state='readonly', width=30, font=('Arial', 11))
        self.calc_recipe_combo.pack(side=tk.LEFT, padx=5)
        self.calc_recipe_combo.bind('<<ComboboxSelected>>', self.on_calc_recipe_select)
        
        ttk.Label(top_frame, text="Original Servings:", font=('Arial', 12)).pack(side=tk.LEFT, padx=10)
        self.original_servings_label = ttk.Label(top_frame, text="0", font=('Arial', 12, 'bold'))
        self.original_servings_label.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(top_frame, text="Target Servings:", font=('Arial', 12)).pack(side=tk.LEFT, padx=10)
        self.target_servings_entry = ttk.Entry(top_frame, width=10, font=('Arial', 11))
        self.target_servings_entry.pack(side=tk.LEFT, padx=5)
        self.target_servings_entry.insert(0, "1")
        
        ttk.Button(top_frame, text="Calculate", command=self.calculate_bulk).pack(side=tk.LEFT, padx=10)
        
        # Middle frame - Scaled ingredients
        middle_frame = ttk.Frame(self.calculator_frame)
        middle_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        ttk.Label(middle_frame, text="Scaled Ingredients List", font=('Arial', 14, 'bold')).pack(pady=10)
        
        self.scaled_ingredients_text = scrolledtext.ScrolledText(middle_frame, wrap=tk.WORD, 
                                                                  font=('Arial', 12), height=20)
        self.scaled_ingredients_text.pack(fill=tk.BOTH, expand=True)
        
        # Bottom frame - Export options
        bottom_frame = ttk.Frame(self.calculator_frame)
        bottom_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(bottom_frame, text="Export to Text", command=self.export_ingredients).pack(side=tk.LEFT, padx=5)
        ttk.Button(bottom_frame, text="Print Shopping List", command=self.print_ingredients).pack(side=tk.LEFT, padx=5)
        
    def select_image(self):
        file_path = filedialog.askopenfilename(
            title="Select Dish Image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")]
        )
        if file_path:
            self.scanned_image_path = file_path
            self.display_image(file_path)
            self.scan_btn.config(state='normal')
    
    def display_image(self, file_path):
        try:
            img = Image.open(file_path)
            img.thumbnail((400, 400), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            self.image_label.config(image=photo, text="")
            self.image_label.image = photo
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image: {str(e)}")
    
    def scan_dish(self):
        if not self.scanned_image_path:
            messagebox.showwarning("Warning", "Please select an image first")
            return
        
        self.recipe_text.delete(1.0, tk.END)
        
        # Check if API key is configured
        if not self.image_scanner.api_key:
            self.recipe_text.insert(tk.END, "⚠️ OpenAI API key not configured.\n\n")
            self.recipe_text.insert(tk.END, "To enable image recognition:\n")
            self.recipe_text.insert(tk.END, "1. Get an API key from https://platform.openai.com/api-keys\n")
            self.recipe_text.insert(tk.END, "2. Set OPENAI_API_KEY environment variable, OR\n")
            self.recipe_text.insert(tk.END, "3. Create data/api_config.json with your API key\n\n")
            self.recipe_text.insert(tk.END, "Using template recipe for now...\n")
            self.root.update()
        else:
            self.recipe_text.insert(tk.END, "🔍 Analyzing image with AI...\n")
            self.recipe_text.insert(tk.END, "This may take a few seconds...\n\n")
            self.root.update()
        
        try:
            recipe = self.image_scanner.scan_and_generate_recipe(self.scanned_image_path)
            self.current_recipe = recipe
            
            # Display recipe
            self.recipe_text.delete(1.0, tk.END)
            recipe_text = f"Recipe Name: {recipe.get('name', 'Unknown Dish')}\n\n"
            recipe_text += f"Servings: {recipe.get('servings', 4)}\n\n"
            recipe_text += "Ingredients:\n"
            for ingredient in recipe.get('ingredients', []):
                recipe_text += f"  • {ingredient}\n"
            recipe_text += "\nInstructions:\n"
            for i, instruction in enumerate(recipe.get('instructions', []), 1):
                recipe_text += f"{i}. {instruction}\n"
            
            self.recipe_text.insert(tk.END, recipe_text)
            
            if self.image_scanner.api_key:
                messagebox.showinfo("Success", "Recipe generated from image analysis!")
            else:
                messagebox.showinfo("Template Recipe", "Template recipe generated. Please edit with actual ingredients.\n\nTo enable AI image recognition, configure your OpenAI API key.")
        except Exception as e:
            error_msg = str(e)
            messagebox.showerror("Error", f"Failed to scan dish: {error_msg}")
            self.recipe_text.delete(1.0, tk.END)
            self.recipe_text.insert(tk.END, f"Error: {error_msg}\n\n")
            self.recipe_text.insert(tk.END, "Falling back to template recipe...\n")
            try:
                recipe = self.image_scanner._generate_template_recipe(self.scanned_image_path)
                self.current_recipe = recipe
                recipe_text = f"Template Recipe: {recipe.get('name', 'Unknown Dish')}\n\n"
                recipe_text += f"Servings: {recipe.get('servings', 4)}\n\n"
                recipe_text += "Ingredients:\n"
                for ingredient in recipe.get('ingredients', []):
                    recipe_text += f"  • {ingredient}\n"
                recipe_text += "\nInstructions:\n"
                for i, instruction in enumerate(recipe.get('instructions', []), 1):
                    recipe_text += f"{i}. {instruction}\n"
                self.recipe_text.insert(tk.END, recipe_text)
            except:
                pass
    
    def save_scanned_recipe(self):
        if not self.current_recipe:
            messagebox.showwarning("Warning", "No recipe to save. Please scan a dish first.")
            return
        
        recipe_name = self.current_recipe.get('name', 'Scanned Recipe')
        self.recipe_manager.save_recipe(self.current_recipe)
        self.load_recipes()
        messagebox.showinfo("Success", f"Recipe '{recipe_name}' saved successfully!")
        self.clear_scanner()
    
    def clear_scanner(self):
        self.scanned_image_path = None
        self.current_recipe = None
        self.image_label.config(image="", text="No image selected")
        self.image_label.image = None
        self.recipe_text.delete(1.0, tk.END)
        self.scan_btn.config(state='disabled')
    
    def load_recipes(self):
        recipes = self.recipe_manager.get_all_recipes()
        self.recipe_listbox.delete(0, tk.END)
        recipe_names = []
        for recipe in recipes:
            name = recipe.get('name', 'Unnamed Recipe')
            self.recipe_listbox.insert(tk.END, name)
            recipe_names.append(name)
        
        # Update calculator combo
        self.calc_recipe_combo['values'] = recipe_names
    
    def on_recipe_select(self, event):
        selection = self.recipe_listbox.curselection()
        if selection:
            recipe_name = self.recipe_listbox.get(selection[0])
            recipe = self.recipe_manager.get_recipe(recipe_name)
            if recipe:
                self.display_recipe(recipe)
    
    def display_recipe(self, recipe):
        self.current_recipe = recipe
        self.recipe_name_entry.delete(0, tk.END)
        self.recipe_name_entry.insert(0, recipe.get('name', ''))
        
        self.servings_entry.delete(0, tk.END)
        self.servings_entry.insert(0, str(recipe.get('servings', 4)))
        
        self.ingredients_text.delete(1.0, tk.END)
        ingredients = '\n'.join(recipe.get('ingredients', []))
        self.ingredients_text.insert(tk.END, ingredients)
        
        self.instructions_text.delete(1.0, tk.END)
        instructions = '\n'.join(recipe.get('instructions', []))
        self.instructions_text.insert(tk.END, instructions)
    
    def new_recipe(self):
        self.current_recipe = None
        self.recipe_name_entry.delete(0, tk.END)
        self.servings_entry.delete(0, tk.END)
        self.servings_entry.insert(0, "4")
        self.ingredients_text.delete(1.0, tk.END)
        self.instructions_text.delete(1.0, tk.END)
    
    def save_recipe(self):
        name = self.recipe_name_entry.get().strip()
        if not name:
            messagebox.showwarning("Warning", "Please enter a recipe name")
            return
        
        try:
            servings = int(self.servings_entry.get() or "4")
        except ValueError:
            servings = 4
        
        ingredients_text = self.ingredients_text.get(1.0, tk.END).strip()
        ingredients = [line.strip() for line in ingredients_text.split('\n') if line.strip()]
        
        instructions_text = self.instructions_text.get(1.0, tk.END).strip()
        instructions = [line.strip() for line in instructions_text.split('\n') if line.strip()]
        
        recipe = {
            'name': name,
            'servings': servings,
            'ingredients': ingredients,
            'instructions': instructions
        }
        
        self.recipe_manager.save_recipe(recipe)
        self.load_recipes()
        messagebox.showinfo("Success", f"Recipe '{name}' saved successfully!")
    
    def delete_recipe(self):
        selection = self.recipe_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a recipe to delete")
            return
        
        recipe_name = self.recipe_listbox.get(selection[0])
        if messagebox.askyesno("Confirm", f"Delete recipe '{recipe_name}'?"):
            self.recipe_manager.delete_recipe(recipe_name)
            self.load_recipes()
            self.new_recipe()
            messagebox.showinfo("Success", "Recipe deleted successfully!")
    
    def on_calc_recipe_select(self, event):
        recipe_name = self.calc_recipe_var.get()
        recipe = self.recipe_manager.get_recipe(recipe_name)
        if recipe:
            self.original_servings_label.config(text=str(recipe.get('servings', 4)))
    
    def calculate_bulk(self):
        recipe_name = self.calc_recipe_var.get()
        if not recipe_name:
            messagebox.showwarning("Warning", "Please select a recipe")
            return
        
        recipe = self.recipe_manager.get_recipe(recipe_name)
        if not recipe:
            messagebox.showerror("Error", "Recipe not found")
            return
        
        try:
            target_servings = float(self.target_servings_entry.get())
            if target_servings <= 0:
                raise ValueError("Servings must be positive")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number of servings")
            return
        
        scaled_recipe = self.recipe_scaler.scale_recipe(recipe, target_servings)
        
        # Display scaled ingredients
        self.scaled_ingredients_text.delete(1.0, tk.END)
        output = f"Recipe: {scaled_recipe['name']}\n"
        output += f"Original Servings: {recipe['servings']}\n"
        output += f"Target Servings: {target_servings}\n"
        output += f"Scale Factor: {scaled_recipe['scale_factor']:.2f}x\n\n"
        output += "SCALED INGREDIENTS:\n"
        output += "=" * 50 + "\n"
        for ingredient in scaled_recipe['scaled_ingredients']:
            output += f"  • {ingredient}\n"
        
        self.scaled_ingredients_text.insert(tk.END, output)
    
    def export_ingredients(self):
        content = self.scaled_ingredients_text.get(1.0, tk.END)
        if not content.strip():
            messagebox.showwarning("Warning", "No ingredients to export")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                messagebox.showinfo("Success", f"Ingredients exported to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export: {str(e)}")
    
    def print_ingredients(self):
        content = self.scaled_ingredients_text.get(1.0, tk.END)
        if not content.strip():
            messagebox.showwarning("Warning", "No ingredients to print")
            return
        
        # Simple print dialog (can be enhanced with actual printing)
        print_window = tk.Toplevel(self.root)
        print_window.title("Shopping List")
        print_window.geometry("600x700")
        
        text_widget = scrolledtext.ScrolledText(print_window, wrap=tk.WORD, font=('Arial', 12))
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        text_widget.insert(tk.END, content)
        text_widget.config(state='disabled')
        
        ttk.Button(print_window, text="Close", command=print_window.destroy).pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = CookingApp(root)
    root.mainloop()

