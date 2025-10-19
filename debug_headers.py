#!/usr/bin/env python3
"""
Debug script to test CORS and security headers
"""
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from service import app, talisman
from flask import Flask

def test_headers():
    """Test if headers are being set correctly"""
    print("Testing headers...")
    
    # Create a test client
    app.config['TESTING'] = True
    client = app.test_client()
    
    # Make a request
    resp = client.get("/")
    print(f"Response status: {resp.status_code}")
    print(f"Response headers: {dict(resp.headers)}")
    
    # Check specific headers
    print(f"Access-Control-Allow-Origin: {resp.headers.get('Access-Control-Allow-Origin')}")
    print(f"X-Frame-Options: {resp.headers.get('X-Frame-Options')}")
    print(f"X-Content-Type-Options: {resp.headers.get('X-Content-Type-Options')}")
    
    # Check if Talisman is working
    print(f"Talisman force_https: {talisman.force_https}")
    print(f"Talisman app: {talisman.app}")

if __name__ == '__main__':
    test_headers()
