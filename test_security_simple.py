#!/usr/bin/env python3
"""
Simple test script to validate security headers and CORS
"""
import sys
import os

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(__file__))

try:
    from service import app, talisman
    print("Successfully imported app and talisman")
    
    # Test the app
    with app.test_client() as client:
        # Disable forced HTTPS for testing
        talisman.force_https = False
        
        # Test the root endpoint
        response = client.get('/')
        print(f"Status Code: {response.status_code}")
        print("Headers:")
        for header, value in response.headers:
            print(f"  {header}: {value}")
        
        # Check for security headers
        security_headers = {
            'X-Frame-Options': 'SAMEORIGIN',
            'X-Content-Type-Options': 'nosniff',
            'Content-Security-Policy': 'default-src \'self\'; object-src \'none\'',
            'Referrer-Policy': 'strict-origin-when-cross-origin'
        }
        
        print("\nChecking security headers:")
        for header, expected_value in security_headers.items():
            actual_value = response.headers.get(header)
            if actual_value == expected_value:
                print(f"  ✓ {header}: {actual_value}")
            else:
                print(f"  ✗ {header}: expected '{expected_value}', got '{actual_value}'")
        
        # Check for CORS headers
        cors_headers = {
            'Access-Control-Allow-Origin': '*'
        }
        
        print("\nChecking CORS headers:")
        for header, expected_value in cors_headers.items():
            actual_value = response.headers.get(header)
            if actual_value == expected_value:
                print(f"  ✓ {header}: {actual_value}")
            else:
                print(f"  ✗ {header}: expected '{expected_value}', got '{actual_value}'")

except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure Flask-Talisman and Flask-Cors are installed")
except Exception as e:
    print(f"Error: {e}")
