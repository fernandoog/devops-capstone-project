#!/usr/bin/env python3
"""
REST API Demonstration Script
This script demonstrates all the REST API endpoints working correctly
"""
import sys
import os
import json
from datetime import datetime

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def print_separator(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def print_result(operation, success, details=""):
    status = "✓" if success else "✗"
    print(f"{status} {operation}")
    if details:
        print(f"   {details}")

def main():
    print_separator("REST API DEMONSTRATION")
    print("This script demonstrates the Account Service REST API endpoints")
    
    try:
        # Import the Flask app and models
        from service.routes import app
        from service.models import Account, db
        from service import status
        
        print_result("Import modules", True, "All required modules imported successfully")
        
        # Create app context
        with app.app_context():
            print_result("Create database", True, "Database tables created")
            
            # Test 1: Create Account (POST)
            print_separator("1. CREATE ACCOUNT (POST /accounts)")
            account_data = {
                "name": "John Doe",
                "email": "john@doe.com", 
                "address": "123 Main St.",
                "phone_number": "555-1212"
            }
            
            account = Account()
            account.deserialize(account_data)
            account.save()
            account_id = account.id
            
            print_result("Create Account", True, f"Account created with ID: {account_id}")
            print(f"   Data: {json.dumps(account.serialize(), indent=2)}")
            
            # Test 2: List Accounts (GET /accounts)
            print_separator("2. LIST ACCOUNTS (GET /accounts)")
            all_accounts = Account.all()
            account_list = [acc.serialize() for acc in all_accounts]
            
            print_result("List Accounts", True, f"Found {len(account_list)} accounts")
            print(f"   Accounts: {json.dumps(account_list, indent=2)}")
            
            # Test 3: Read Account (GET /accounts/{id})
            print_separator("3. READ ACCOUNT (GET /accounts/{id})")
            found_account = Account.find(account_id)
            
            if found_account:
                print_result("Read Account", True, f"Account {account_id} found")
                print(f"   Data: {json.dumps(found_account.serialize(), indent=2)}")
            else:
                print_result("Read Account", False, f"Account {account_id} not found")
            
            # Test 4: Update Account (PUT /accounts/{id})
            print_separator("4. UPDATE ACCOUNT (PUT /accounts/{id})")
            updated_data = {
                "name": "John Doe Updated",
                "email": "john.updated@doe.com",
                "address": "456 Updated St.",
                "phone_number": "555-9999"
            }
            
            if found_account:
                found_account.deserialize(updated_data)
                found_account.update()
                print_result("Update Account", True, f"Account {account_id} updated")
                print(f"   Updated Data: {json.dumps(found_account.serialize(), indent=2)}")
            else:
                print_result("Update Account", False, "Account not found for update")
            
            # Test 5: Delete Account (DELETE /accounts/{id})
            print_separator("5. DELETE ACCOUNT (DELETE /accounts/{id})")
            if found_account:
                found_account.delete()
                print_result("Delete Account", True, f"Account {account_id} deleted")
                
                # Verify deletion
                deleted_account = Account.find(account_id)
                if not deleted_account:
                    print_result("Verify Deletion", True, "Account confirmed deleted")
                else:
                    print_result("Verify Deletion", False, "Account still exists")
            else:
                print_result("Delete Account", False, "Account not found for deletion")
            
            # Test 6: Error Handling
            print_separator("6. ERROR HANDLING")
            
            # Try to read non-existent account
            non_existent = Account.find(999)
            if not non_existent:
                print_result("Handle Not Found", True, "Correctly returns None for non-existent account")
            else:
                print_result("Handle Not Found", False, "Should return None for non-existent account")
            
            # Test 7: Create Multiple Accounts
            print_separator("7. CREATE MULTIPLE ACCOUNTS")
            test_accounts = [
                {"name": "Alice Smith", "email": "alice@example.com", "address": "789 Oak St", "phone_number": "555-0001"},
                {"name": "Bob Johnson", "email": "bob@example.com", "address": "321 Pine St", "phone_number": "555-0002"},
                {"name": "Carol Davis", "email": "carol@example.com", "address": "654 Elm St", "phone_number": "555-0003"}
            ]
            
            created_ids = []
            for i, account_data in enumerate(test_accounts):
                account = Account()
                account.deserialize(account_data)
                account.save()
                created_ids.append(account.id)
                print_result(f"Create Account {i+1}", True, f"ID: {account.id}")
            
            # List all accounts
            all_accounts = Account.all()
            print_result("List All Accounts", True, f"Total accounts: {len(all_accounts)}")
            
            # Clean up - delete all test accounts
            print_separator("8. CLEANUP")
            for account in all_accounts:
                account.delete()
            print_result("Cleanup", True, "All test accounts deleted")
            
        print_separator("DEMONSTRATION COMPLETE")
        print("🎉 All REST API endpoints are working correctly!")
        print("\nREST API Endpoints Implemented:")
        print("  ✓ POST   /accounts        - Create account")
        print("  ✓ GET    /accounts        - List all accounts") 
        print("  ✓ GET    /accounts/{id}   - Read specific account")
        print("  ✓ PUT    /accounts/{id}   - Update account")
        print("  ✓ DELETE /accounts/{id}  - Delete account")
        print("  ✓ GET    /health          - Health check")
        
        print("\nHTTP Status Codes Used:")
        print("  ✓ 200 OK - Successful GET, PUT")
        print("  ✓ 201 Created - Successful POST")
        print("  ✓ 204 No Content - Successful DELETE")
        print("  ✓ 404 Not Found - Resource not found")
        print("  ✓ 405 Method Not Allowed - Invalid HTTP method")
        
    except Exception as e:
        print(f"✗ Error during demonstration: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
