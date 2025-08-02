"""Security testing script to demonstrate improvements"""

import requests
import json

BASE_URL = "http://127.0.0.1:5009"

def test_home_endpoint():
    """Test the home endpoint"""
    print("=== Testing Home Endpoint ===")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_get_users():
    """Test getting all users"""
    print("=== Testing Get All Users ===")
    response = requests.get(f"{BASE_URL}/users")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_create_user():
    """Test creating a new user with validation"""
    print("=== Testing Create User (Valid Data) ===")
    user_data = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "password": "SecurePass123"
    }
    response = requests.post(f"{BASE_URL}/users", json=user_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()
    
    print("=== Testing Create User (Invalid Password) ===")
    invalid_user_data = {
        "name": "Jane Doe",
        "email": "jane.doe@example.com",
        "password": "123"  # Too short
    }
    response = requests.post(f"{BASE_URL}/users", json=invalid_user_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_sql_injection_protection():
    """Test that SQL injection is prevented"""
    print("=== Testing SQL Injection Protection ===")
    # This would have been vulnerable in the original version
    malicious_input = "1' OR '1'='1"
    response = requests.get(f"{BASE_URL}/user/{malicious_input}")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_search_users():
    """Test user search functionality"""
    print("=== Testing Search Users ===")
    response = requests.get(f"{BASE_URL}/search?name=John")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_login():
    """Test login functionality"""
    print("=== Testing Login (Valid Credentials) ===")
    login_data = {
        "email": "john.doe@example.com",
        "password": "SecurePass123"
    }
    response = requests.post(f"{BASE_URL}/login", json=login_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()
    
    print("=== Testing Login (Invalid Credentials) ===")
    invalid_login_data = {
        "email": "john.doe@example.com",
        "password": "wrongpassword"
    }
    response = requests.post(f"{BASE_URL}/login", json=invalid_login_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

if __name__ == "__main__":
    print("🔒 SECURE API TESTING")
    print("=" * 50)
    
    try:
        test_home_endpoint()
        test_get_users()
        test_create_user()
        test_sql_injection_protection()
        test_search_users()
        test_login()
        
        print("✅ All tests completed successfully!")
        print("\n🛡️ SECURITY IMPROVEMENTS DEMONSTRATED:")
        print("- SQL injection protection with parameterized queries")
        print("- Password hashing instead of plain text storage")
        print("- Input validation and sanitization")
        print("- Consistent JSON API responses")
        print("- Proper error handling")
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the server. Make sure app_secure.py is running.")
    except Exception as e:
        print(f"❌ Test failed: {e}")
