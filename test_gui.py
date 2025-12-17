#!/usr/bin/env python3
"""
Quick GUI test - verifies the application can start without errors
"""

import sys
import tkinter as tk

def test_gui_startup():
    """Test that the GUI application can initialize"""
    print("Testing GUI startup...")
    
    try:
        # Import main module
        import main
        
        # Create root window but don't show it
        root = tk.Tk()
        root.withdraw()  # Hide window
        
        # Try to create the app
        app = main.CookingApp(root)
        print("  ✓ Application initialized successfully")
        print("  ✓ All widgets created")
        
        # Check that all tabs exist
        assert app.notebook is not None, "Notebook not created"
        assert len(app.notebook.tabs()) == 3, "Expected 3 tabs"
        print("  ✓ All tabs created")
        
        # Clean up
        root.destroy()
        print("\n✓ GUI startup test PASSED")
        print("  The application is ready to run!")
        return True
        
    except Exception as e:
        print(f"\n✗ GUI startup test FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_gui_startup()
    sys.exit(0 if success else 1)

