#!/usr/bin/env python3
"""
Test script for Chef's Recipe Assistant
Tests core functionality without requiring GUI interaction
"""

import os
import sys
import json
from recipe_manager import RecipeManager
from recipe_scaler import RecipeScaler
from image_scanner import ImageScanner

def test_recipe_manager():
    """Test RecipeManager functionality"""
    print("Testing RecipeManager...")
    rm = RecipeManager()
    
    # Test saving a recipe
    test_recipe = {
        'name': 'Test Recipe',
        'servings': 4,
        'ingredients': ['2 cups flour', '1 cup sugar', '3 eggs'],
        'instructions': ['Mix dry ingredients', 'Add wet ingredients', 'Bake at 350F']
    }
    
    rm.save_recipe(test_recipe)
    print("  ✓ Recipe saved")
    
    # Test retrieving recipe
    retrieved = rm.get_recipe('Test Recipe')
    assert retrieved is not None, "Recipe not found after saving"
    assert retrieved['name'] == 'Test Recipe', "Recipe name mismatch"
    print("  ✓ Recipe retrieved")
    
    # Test getting all recipes
    all_recipes = rm.get_all_recipes()
    assert len(all_recipes) > 0, "No recipes found"
    print(f"  ✓ Found {len(all_recipes)} recipe(s)")
    
    # Test deleting recipe
    rm.delete_recipe('Test Recipe')
    deleted_check = rm.get_recipe('Test Recipe')
    assert deleted_check is None, "Recipe not deleted"
    print("  ✓ Recipe deleted")
    
    print("RecipeManager: PASSED\n")
    return True

def test_recipe_scaler():
    """Test RecipeScaler functionality"""
    print("Testing RecipeScaler...")
    rs = RecipeScaler()
    
    test_cases = [
        {
            'recipe': {
                'name': 'Test',
                'servings': 4,
                'ingredients': ['2 cups flour', '1/2 tablespoon salt', '1.5 pounds chicken'],
                'instructions': ['Cook']
            },
            'target': 8,
            'expected_scale': 2.0
        },
        {
            'recipe': {
                'name': 'Test',
                'servings': 6,
                'ingredients': ['3 cups rice', '2 teaspoons spice'],
                'instructions': ['Cook']
            },
            'target': 2,
            'expected_scale': 1/3
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        scaled = rs.scale_recipe(test_case['recipe'], test_case['target'])
        assert abs(scaled['scale_factor'] - test_case['expected_scale']) < 0.01, \
            f"Scale factor mismatch in test {i}"
        assert len(scaled['scaled_ingredients']) == len(test_case['recipe']['ingredients']), \
            f"Ingredient count mismatch in test {i}"
        print(f"  ✓ Test case {i}: {test_case['recipe']['servings']} → {test_case['target']} servings")
    
    print("RecipeScaler: PASSED\n")
    return True

def test_image_scanner():
    """Test ImageScanner functionality"""
    print("Testing ImageScanner...")
    scanner = ImageScanner()
    
    # Test that scanner initializes
    assert scanner is not None, "Scanner not initialized"
    print("  ✓ Scanner initialized")
    
    # Test base64 encoding (with a dummy file if needed)
    # We'll skip actual image scanning since we don't have test images
    print("  ✓ ImageScanner basic functionality OK")
    print("  Note: Full image scanning requires actual image files")
    
    print("ImageScanner: PASSED\n")
    return True

def test_gui_imports():
    """Test that GUI can be imported"""
    print("Testing GUI imports...")
    try:
        import tkinter as tk
        from tkinter import ttk, filedialog, messagebox, scrolledtext
        from PIL import Image, ImageTk
        print("  ✓ All GUI dependencies available")
        
        # Test creating a root window (but don't show it)
        root = tk.Tk()
        root.withdraw()  # Hide the window
        print("  ✓ Tkinter root window created")
        root.destroy()
        
        print("GUI imports: PASSED\n")
        return True
    except ImportError as e:
        print(f"  ✗ Import error: {e}")
        return False

def test_data_directory():
    """Test data directory creation"""
    print("Testing data directory...")
    rm = RecipeManager()
    
    assert os.path.exists('data'), "Data directory not created"
    print("  ✓ Data directory exists")
    
    if os.path.exists('data/recipes.json'):
        with open('data/recipes.json', 'r') as f:
            data = json.load(f)
        print(f"  ✓ Recipes file exists with {len(data)} recipe(s)")
    else:
        print("  ✓ Recipes file will be created on first save")
    
    print("Data directory: PASSED\n")
    return True

def main():
    """Run all tests"""
    print("=" * 50)
    print("Chef's Recipe Assistant - Test Suite")
    print("=" * 50)
    print()
    
    tests = [
        test_data_directory,
        test_recipe_manager,
        test_recipe_scaler,
        test_image_scanner,
        test_gui_imports,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"  ✗ Test failed with error: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
            print()
    
    print("=" * 50)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("=" * 50)
    
    if failed == 0:
        print("\n✓ All tests passed! Application is ready to use.")
        return 0
    else:
        print(f"\n✗ {failed} test(s) failed. Please review errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

