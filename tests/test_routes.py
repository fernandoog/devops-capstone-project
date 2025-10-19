"""
Test cases for Account Service
"""
import unittest
import json
from service import status
from service.routes import app
from service.models import Account, db
from service import talisman

BASE_URL = "/accounts"
HTTPS_ENVIRON = {'wsgi.url_scheme': 'https'}

class TestAccountService(unittest.TestCase):
    """Test Cases for Account Service"""
    
    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        cls.app = app
        cls.client = app.test_client()
        # Disable forced HTTPS for testing
        talisman.force_https = False
    
    def setUp(self):
        """This runs before each test"""
        with self.app.app_context():
            db.drop_all()
            db.create_all()
    
    def tearDown(self):
        """This runs after each test"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
    
    def _create_accounts(self, count):
        """Helper method to create accounts in bulk"""
        accounts = []
        with self.app.app_context():
            for i in range(count):
                account = Account()
                account.name = f"Test Account {i}"
                account.email = f"test{i}@example.com"
                account.address = f"{i} Test Street"
                account.phone_number = f"555-{i:04d}"
                account.save()
                accounts.append(account)
        return accounts
    
    def test_create_account(self):
        """It should Create a new Account"""
        account_data = {
            "name": "John Doe",
            "email": "john@doe.com",
            "address": "123 Main St.",
            "phone_number": "555-1212"
        }
        resp = self.client.post(BASE_URL, json=account_data)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        
        # Check the data is correct
        data = resp.get_json()
        self.assertEqual(data["name"], "John Doe")
        self.assertEqual(data["email"], "john@doe.com")
        self.assertEqual(data["address"], "123 Main St.")
        self.assertEqual(data["phone_number"], "555-1212")
        self.assertIsNotNone(data["id"])
    
    def test_get_account_list(self):
        """It should Get a list of Accounts"""
        self._create_accounts(5)
        resp = self.client.get(BASE_URL)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), 5)
    
    def test_read_an_account(self):
        """It should Read a single Account"""
        # Create an account first
        with self.app.app_context():
            test_account = Account()
            test_account.name = "Test Account"
            test_account.email = "test@example.com"
            test_account.address = "123 Test St"
            test_account.phone_number = "555-1234"
            test_account.save()
            account_id = test_account.id
        
        resp = self.client.get(f"{BASE_URL}/{account_id}")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["name"], "Test Account")
        self.assertEqual(data["email"], "test@example.com")
    
    def test_account_not_found(self):
        """It should not Read an Account that doesn't exist"""
        resp = self.client.get(f"{BASE_URL}/0")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_update_account(self):
        """It should Update an existing Account"""
        # Create an account first
        with self.app.app_context():
            test_account = Account()
            test_account.name = "Original Name"
            test_account.email = "original@example.com"
            test_account.address = "123 Original St"
            test_account.phone_number = "555-0000"
            test_account.save()
            account_id = test_account.id
        
        # Update the account
        updated_data = {
            "name": "Updated Name",
            "email": "updated@example.com",
            "address": "456 Updated St",
            "phone_number": "555-9999"
        }
        resp = self.client.put(f"{BASE_URL}/{account_id}", json=updated_data)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["name"], "Updated Name")
        self.assertEqual(data["email"], "updated@example.com")
    
    def test_update_account_not_found(self):
        """It should not Update an Account that doesn't exist"""
        updated_data = {
            "name": "Updated Name",
            "email": "updated@example.com"
        }
        resp = self.client.put(f"{BASE_URL}/0", json=updated_data)
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_delete_account(self):
        """It should Delete an Account"""
        # Create an account first
        with self.app.app_context():
            test_account = Account()
            test_account.name = "Test Account"
            test_account.email = "test@example.com"
            test_account.save()
            account_id = test_account.id
        
        resp = self.client.delete(f"{BASE_URL}/{account_id}")
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verify it's deleted
        resp = self.client.get(f"{BASE_URL}/{account_id}")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_delete_account_not_found(self):
        """It should not Delete an Account that doesn't exist"""
        resp = self.client.delete(f"{BASE_URL}/0")
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_method_not_allowed(self):
        """It should not allow an illegal method call"""
        resp = self.client.delete(BASE_URL)
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def test_security_headers(self):
        """It should return security headers"""
        resp = self.client.get("/", environ_overrides=HTTPS_ENVIRON)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        
        # Check for security headers
        self.assertEqual(resp.headers.get('X-Frame-Options'), 'SAMEORIGIN')
        self.assertEqual(resp.headers.get('X-Content-Type-Options'), 'nosniff')
        self.assertEqual(resp.headers.get('Content-Security-Policy'), 'default-src \'self\'; object-src \'none\'')
        self.assertEqual(resp.headers.get('Referrer-Policy'), 'strict-origin-when-cross-origin')
    
    def test_cors_headers(self):
        """It should return CORS headers"""
        resp = self.client.get("/", environ_overrides=HTTPS_ENVIRON)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        
        # Check for CORS headers
        self.assertEqual(resp.headers.get('Access-Control-Allow-Origin'), '*')
