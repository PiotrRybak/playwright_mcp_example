#!/usr/bin/env python3
"""
Simple runner script that checks for virtual environment activation
"""
import sys
import os

def check_venv():
    """Check if we're running in a virtual environment"""
    return hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)

if __name__ == "__main__":
    if not check_venv():
        print("⚠️  Warning: You're not running in a virtual environment!")
        print("It's recommended to activate your virtual environment first:")
        print("  Windows: venv\\Scripts\\activate")
        print("  macOS/Linux: source venv/bin/activate")
        print()
        response = input("Continue anyway? (y/N): ").lower()
        if response != 'y':
            print("Please activate your virtual environment and try again.")
            sys.exit(1)
    
    print("🚀 Running MCP Agent Example...")
    print()
    
    # Import and run the main script
    try:
        import main
    except ImportError as e:
        print(f"❌ Error importing required modules: {e}")
        print("Make sure you've installed dependencies with: pip install -r requirements.txt")
        sys.exit(1) 