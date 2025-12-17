import re

class RecipeScaler:
    def __init__(self):
        # Common unit conversions
        self.unit_conversions = {
            'cup': {'cups': 1, 'tablespoons': 16, 'teaspoons': 48, 'ml': 236.588},
            'tablespoon': {'cups': 1/16, 'tablespoons': 1, 'teaspoons': 3, 'ml': 14.7868},
            'teaspoon': {'cups': 1/48, 'tablespoons': 1/3, 'teaspoons': 1, 'ml': 4.92892},
            'pound': {'pounds': 1, 'ounces': 16, 'grams': 453.592},
            'ounce': {'pounds': 1/16, 'ounces': 1, 'grams': 28.3495},
            'gram': {'pounds': 0.00220462, 'ounces': 0.035274, 'grams': 1},
            'kg': {'pounds': 2.20462, 'ounces': 35.274, 'grams': 1000},
        }
    
    def scale_recipe(self, recipe, target_servings):
        """
        Scale a recipe to a different number of servings.
        
        Args:
            recipe: Dictionary with 'name', 'servings', 'ingredients', 'instructions'
            target_servings: Desired number of servings
        
        Returns:
            Dictionary with scaled recipe
        """
        original_servings = recipe.get('servings', 4)
        if original_servings <= 0:
            original_servings = 4
        
        scale_factor = target_servings / original_servings
        
        scaled_ingredients = []
        for ingredient in recipe.get('ingredients', []):
            scaled_ingredient = self._scale_ingredient(ingredient, scale_factor)
            scaled_ingredients.append(scaled_ingredient)
        
        return {
            'name': recipe.get('name', 'Recipe'),
            'original_servings': original_servings,
            'target_servings': target_servings,
            'scale_factor': scale_factor,
            'scaled_ingredients': scaled_ingredients,
            'instructions': recipe.get('instructions', [])
        }
    
    def _scale_ingredient(self, ingredient, scale_factor):
        """
        Scale a single ingredient string.
        Extracts and scales the FIRST number (whole, decimal, fraction, or mixed) found in the ingredient.
        """
        # Find the first number pattern in the ingredient
        # Try patterns in order of specificity: mixed > fraction > decimal > whole
        
        # Pattern 1: Mixed numbers: "1 1/2" or "2 3/4"
        mixed_match = re.search(r'(\d+)\s+(\d+/\d+)', ingredient)
        if mixed_match:
            whole = int(mixed_match.group(1))
            frac_str = mixed_match.group(2)
            parts = frac_str.split('/')
            numerator = int(parts[0])
            denominator = int(parts[1])
            amount = whole + (numerator / denominator)
            
            # Find the unit after the mixed number
            end_pos = mixed_match.end()
            unit_match = re.search(r'\s*([a-zA-Z]+)', ingredient[end_pos:])
            unit = unit_match.group(1) if unit_match else ''
            
            # Scale and format
            scaled = amount * scale_factor
            formatted = self._format_amount(scaled)
            
            # Replace the entire number + unit
            if unit:
                replacement = f"{formatted} {unit}"
                # Find where unit ends
                unit_end = end_pos + len(unit_match.group(0))
                return ingredient[:mixed_match.start()] + replacement + ingredient[unit_end:]
            else:
                replacement = formatted
                return ingredient[:mixed_match.start()] + replacement + ingredient[end_pos:]
        
        # Pattern 2: Fractions: "1/2" or "3/4"
        fraction_match = re.search(r'(\d+/\d+)', ingredient)
        if fraction_match:
            frac_str = fraction_match.group(1)
            parts = frac_str.split('/')
            numerator = int(parts[0])
            denominator = int(parts[1])
            amount = numerator / denominator
            
            # Find the unit after the fraction
            end_pos = fraction_match.end()
            unit_match = re.search(r'\s*([a-zA-Z]+)', ingredient[end_pos:])
            unit = unit_match.group(1) if unit_match else ''
            
            # Scale and format
            scaled = amount * scale_factor
            formatted = self._format_amount(scaled)
            
            # Replace
            if unit:
                replacement = f"{formatted} {unit}"
                unit_end = end_pos + len(unit_match.group(0))
                return ingredient[:fraction_match.start()] + replacement + ingredient[unit_end:]
            else:
                replacement = formatted
                return ingredient[:fraction_match.start()] + replacement + ingredient[end_pos:]
        
        # Pattern 3: Decimals: "1.5" or "2.75"
        decimal_match = re.search(r'(\d+\.\d+)', ingredient)
        if decimal_match:
            amount = float(decimal_match.group(1))
            
            # Find the unit after the decimal
            end_pos = decimal_match.end()
            unit_match = re.search(r'\s*([a-zA-Z]+)', ingredient[end_pos:])
            unit = unit_match.group(1) if unit_match else ''
            
            # Scale and format
            scaled = amount * scale_factor
            formatted = self._format_amount(scaled)
            
            # Replace
            if unit:
                replacement = f"{formatted} {unit}"
                unit_end = end_pos + len(unit_match.group(0))
                return ingredient[:decimal_match.start()] + replacement + ingredient[unit_end:]
            else:
                replacement = formatted
                return ingredient[:decimal_match.start()] + replacement + ingredient[end_pos:]
        
        # Pattern 4: Whole numbers: "2" or "10"
        whole_match = re.search(r'\b(\d+)\b', ingredient)
        if whole_match:
            # Make sure it's not part of a decimal or fraction
            start = whole_match.start()
            end = whole_match.end()
            
            # Skip if it's part of a decimal
            if end < len(ingredient) and ingredient[end] == '.':
                # This is part of a decimal, should have been caught above
                pass
            # Skip if it's part of a fraction
            elif end < len(ingredient) and ingredient[end] == '/':
                # This is part of a fraction, should have been caught above
                pass
            else:
                amount = float(whole_match.group(1))
                
                # Find the unit after the number
                unit_match = re.search(r'\s*([a-zA-Z]+)', ingredient[end:])
                unit = unit_match.group(1) if unit_match else ''
                
                # Scale and format
                scaled = amount * scale_factor
                formatted = self._format_amount(scaled)
                
                # Replace
                if unit:
                    replacement = f"{formatted} {unit}"
                    unit_end = end + len(unit_match.group(0))
                    return ingredient[:start] + replacement + ingredient[unit_end:]
                else:
                    replacement = formatted
                    return ingredient[:start] + replacement + ingredient[end:]
        
        # No number found
        return f"{ingredient} (scale by {scale_factor:.2f}x)"
    
    def _format_amount(self, amount):
        """Format a scaled amount nicely"""
        if amount <= 0:
            return "0"
        
        # For very small amounts, use fraction
        if 0 < amount < 1:
            fraction = self._decimal_to_fraction(amount)
            if fraction:
                return fraction
            # Try to simplify to a reasonable fraction
            simplified = self._simplify_fraction(amount)
            if simplified:
                return simplified
            return f"{amount:.2f}".rstrip('0').rstrip('.')
        
        # For amounts >= 1, check if it's close to a whole number
        if abs(amount - round(amount)) < 0.01:
            return str(int(round(amount)))
        
        # Check if it's a simple mixed number
        whole = int(amount)
        decimal_part = amount - whole
        
        if decimal_part > 0.01:
            fraction = self._decimal_to_fraction(decimal_part)
            if fraction:
                return f"{whole} {fraction}" if whole > 0 else fraction
            simplified = self._simplify_fraction(decimal_part)
            if simplified:
                return f"{whole} {simplified}" if whole > 0 else simplified
        
        # Default: show 2 decimal places, remove trailing zeros
        return f"{amount:.2f}".rstrip('0').rstrip('.')
    
    def _simplify_fraction(self, decimal, max_denominator=16):
        """Convert decimal to simplified fraction"""
        if decimal <= 0 or decimal >= 1:
            return None
        
        # Try common denominators
        for denom in range(2, max_denominator + 1):
            for num in range(1, denom):
                value = num / denom
                if abs(decimal - value) < 0.01:
                    # Simplify the fraction
                    gcd = self._gcd(num, denom)
                    simplified_num = num // gcd
                    simplified_den = denom // gcd
                    return f"{simplified_num}/{simplified_den}"
        
        return None
    
    def _gcd(self, a, b):
        """Calculate greatest common divisor"""
        while b:
            a, b = b, a % b
        return a
    
    def _decimal_to_fraction(self, decimal):
        """
        Convert a decimal to a simple fraction (1/2, 1/3, 1/4, etc.)
        """
        common_fractions = {
            0.125: '1/8',
            0.25: '1/4',
            0.333: '1/3',
            0.375: '3/8',
            0.5: '1/2',
            0.667: '2/3',
            0.625: '5/8',
            0.75: '3/4',
            0.875: '7/8'
        }
        
        # Check for close matches
        for value, fraction in common_fractions.items():
            if abs(decimal - value) < 0.01:
                return fraction
        
        return None

