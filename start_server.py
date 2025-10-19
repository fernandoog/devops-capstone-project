#!/usr/bin/env python3
"""
Start the REST API Server
This script starts the Flask server for testing the REST API endpoints
"""
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from service.routes import app
    
    print("🚀 Starting Account Service REST API Server...")
    print("📍 Server will be available at: http://127.0.0.1:5000")
    print("\n📋 Available Endpoints:")
    print("  POST   /accounts        - Create a new account")
    print("  GET    /accounts        - List all accounts")
    print("  GET    /accounts/{id}   - Get account by ID")
    print("  PUT    /accounts/{id}   - Update account by ID")
    print("  DELETE /accounts/{id}  - Delete account by ID")
    print("  GET    /health          - Health check")
    print("\n🔧 Example curl commands:")
    print("  # Create account:")
    print('  curl -X POST http://127.0.0.1:5000/accounts \\')
    print('    -H "Content-Type: application/json" \\')
    print('    -d \'{"name":"John Doe","email":"john@doe.com","address":"123 Main St","phone_number":"555-1212"}\'')
    print("\n  # List accounts:")
    print("  curl -X GET http://127.0.0.1:5000/accounts")
    print("\n  # Get account by ID:")
    print("  curl -X GET http://127.0.0.1:5000/accounts/1")
    print("\n  # Update account:")
    print('  curl -X PUT http://127.0.0.1:5000/accounts/1 \\')
    print('    -H "Content-Type: application/json" \\')
    print('    -d \'{"name":"John Updated","email":"john.updated@doe.com","address":"456 New St","phone_number":"555-9999"}\'')
    print("\n  # Delete account:")
    print("  curl -X DELETE http://127.0.0.1:5000/accounts/1")
    print("\n  # Health check:")
    print("  curl -X GET http://127.0.0.1:5000/health")
    print("\n" + "="*60)
    print("Press Ctrl+C to stop the server")
    print("="*60)
    
    # Start the Flask server
    app.run(host="0.0.0.0", port=5000, debug=True)
    
except ImportError as e:
    print(f"❌ Error importing modules: {e}")
    print("Make sure all required files are in the correct location.")
except Exception as e:
    print(f"❌ Error starting server: {e}")
    import traceback
    traceback.print_exc()
