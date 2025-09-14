#!/usr/bin/env python3
"""
Startup script for Car Condition Assessment Backend
"""

import os
import sys
import subprocess

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import flask
        import boto3
        from inference_sdk import InferenceHTTPClient
        print("✓ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"✗ Missing dependency: {e}")
        print("Please install dependencies with: pip install -r requirements.txt")
        return False

def check_aws_credentials():
    """Check if AWS credentials are configured"""
    try:
        import boto3
        session = boto3.Session()
        credentials = session.get_credentials()
        if credentials:
            print("✓ AWS credentials found")
            return True
        else:
            print("⚠ AWS credentials not found. Make sure to configure AWS credentials for SageMaker")
            return False
    except Exception as e:
        print(f"⚠ Could not check AWS credentials: {e}")
        return False

def main():
    """Main startup function"""
    print("🚗 Starting Car Condition Assessment Backend...")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check AWS credentials
    check_aws_credentials()
    
    print("\n📋 Setup Information:")
    print("- Backend will run on: http://localhost:5001")
    print("- Frontend will be served from: http://localhost:5001")
    print("- Make sure you have AWS credentials configured for SageMaker")
    print("- Make sure you have the Roboflow API key configured in read-stiches.py")
    print("\n" + "=" * 50)
    
    # Start the Flask app
    try:
        from app import app
        print("🚀 Starting Flask server...")
        app.run(host='0.0.0.0', port=5001, debug=True)
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
