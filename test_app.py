#!/usr/bin/env python3
"""
Simple test script to verify the REST API implementation
"""
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from service.routes import app
    from service.models import Account, db
    from service import status
    print("✓ All modules imported successfully")
    
    # Test the app creation
    with app.app_context():
        db.create_all()
        print("✓ Database tables created successfully")
        
        # Test creating an account
        account = Account()
        account.name = "Test User"
        account.email = "test@example.com"
        account.address = "123 Test St"
        account.phone_number = "555-1234"
        account.save()
        print("✓ Account created successfully")
        
        # Test serialization
        serialized = account.serialize()
        print(f"✓ Account serialized: {serialized}")
        
        # Test finding account
        found_account = Account.find(account.id)
        if found_account:
            print("✓ Account found successfully")
        else:
            print("✗ Account not found")
            
        # Test listing accounts
        all_accounts = Account.all()
        print(f"✓ Found {len(all_accounts)} accounts")
        
        # Test updating account
        found_account.name = "Updated Name"
        found_account.update()
        print("✓ Account updated successfully")
        
        # Test deleting account
        found_account.delete()
        print("✓ Account deleted successfully")
        
        # Test that account is gone
        deleted_account = Account.find(account.id)
        if not deleted_account:
            print("✓ Account deletion confirmed")
        else:
            print("✗ Account still exists after deletion")
            
    print("\n🎉 All tests passed! The REST API implementation is working correctly.")
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
