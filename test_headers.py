#!/usr/bin/env python3
"""
Simple test script to verify CORS and security headers
"""
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from service import app, talisman
import unittest

class TestHeaders(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()
        # Disable forced HTTPS for testing
        talisman.force_https = False
    
    def test_cors_headers(self):
        """Test CORS headers"""
        resp = self.client.get("/")
        print(f"Response status: {resp.status_code}")
        print(f"Response headers: {dict(resp.headers)}")
        
        # Check for CORS headers
        self.assertEqual(resp.headers.get('Access-Control-Allow-Origin'), '*')
        print("✓ CORS headers working")
    
    def test_security_headers(self):
        """Test security headers"""
        resp = self.client.get("/")
        print(f"Response status: {resp.status_code}")
        print(f"Response headers: {dict(resp.headers)}")
        
        # Check for security headers
        self.assertEqual(resp.headers.get('X-Frame-Options'), 'SAMEORIGIN')
        self.assertEqual(resp.headers.get('X-Content-Type-Options'), 'nosniff')
        print("✓ Security headers working")

if __name__ == '__main__':
    unittest.main()
