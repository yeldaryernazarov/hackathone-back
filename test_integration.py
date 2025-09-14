#!/usr/bin/env python3
"""
Test script to verify the integration between read-clean.py and read-stiches.py
"""

import os
import sys
import json
from read_clean import analyze_four_photos, count_dirty_words, car_state
from read_stitches import analyze_eight_photos, count_class_words, car_condition

def test_imports():
    """Test if all modules can be imported successfully"""
    print("Testing imports...")
    try:
        from read_clean import analyze_four_photos, count_dirty_words, car_state
        from read_stitches import analyze_eight_photos, count_class_words, car_condition
        print("✓ All imports successful")
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_functions():
    """Test if all functions can be called without errors"""
    print("\nTesting function calls...")
    
    try:
        # Test car_state function
        result = car_state(0)
        print(f"✓ car_state(0) = {result}")
        
        result = car_state(1)
        print(f"✓ car_state(1) = {result}")
        
        result = car_state(3)
        print(f"✓ car_state(3) = {result}")
        
    except Exception as e:
        print(f"✗ car_state error: {e}")
        return False
    
    try:
        # Test car_condition function
        result = car_condition(0)
        print(f"✓ car_condition(0) = {result}")
        
        result = car_condition(1)
        print(f"✓ car_condition(1) = {result}")
        
        result = car_condition(5)
        print(f"✓ car_condition(5) = {result}")
        
    except Exception as e:
        print(f"✗ car_condition error: {e}")
        return False
    
    try:
        # Test count functions with sample data
        sample_outputs = [
            {"predicted_label": "clean", "probability": 0.85},
            {"predicted_label": "dirty", "probability": 0.72},
            {"predicted_label": "clean", "probability": 0.88}
        ]
        
        dirty_count = count_dirty_words(sample_outputs)
        print(f"✓ count_dirty_words with sample data = {dirty_count}")
        
        class_count = count_class_words(sample_outputs)
        print(f"✓ count_class_words with sample data = {class_count}")
        
    except Exception as e:
        print(f"✗ count functions error: {e}")
        return False
    
    return True

def test_app_import():
    """Test if the Flask app can be imported"""
    print("\nTesting Flask app import...")
    try:
        from app import app
        print("✓ Flask app imported successfully")
        return True
    except Exception as e:
        print(f"✗ Flask app import error: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing Car Condition Assessment Integration")
    print("=" * 50)
    
    all_tests_passed = True
    
    # Test imports
    if not test_imports():
        all_tests_passed = False
    
    # Test functions
    if not test_functions():
        all_tests_passed = False
    
    # Test Flask app
    if not test_app_import():
        all_tests_passed = False
    
    print("\n" + "=" * 50)
    if all_tests_passed:
        print("🎉 All tests passed! The integration is working correctly.")
        print("\nTo start the server, run:")
        print("  python run_server.py")
        print("\nThen open http://localhost:5001 in your browser")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
