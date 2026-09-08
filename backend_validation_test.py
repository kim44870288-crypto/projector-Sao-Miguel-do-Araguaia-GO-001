#!/usr/bin/env python3
"""
Clone-and-run validation test for FastAPI backend
Tests basic connectivity, admin login, and JWT authentication
"""
import requests
import sys

# Base URL from frontend/.env
BASE_URL = "https://donas-painel-preview.preview.emergentagent.com"
API_BASE = f"{BASE_URL}/api"

# Admin credentials
ADMIN_USERNAME = "donas"
ADMIN_PASSWORD = "Seinao10@@"


def test_root_endpoint():
    """Test 1: GET /api/ should respond 200 with JSON message"""
    print("\n" + "="*70)
    print("TEST 1: Root Endpoint (GET /api/)")
    print("="*70)
    
    url = f"{API_BASE}/"
    
    try:
        response = requests.get(url, timeout=10)
        print(f"URL: {url}")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code != 200:
            print(f"❌ FAILED: Expected 200, got {response.status_code}")
            print(f"Response: {response.text}")
            return False
        
        try:
            data = response.json()
            print(f"Response JSON: {data}")
            
            if 'message' not in data:
                print("❌ FAILED: Response JSON does not contain 'message' field")
                return False
            
            print(f"✅ PASSED: Root endpoint returns 200 with JSON message")
            print(f"   Message: {data['message']}")
            return True
            
        except Exception as e:
            print(f"❌ FAILED: Response is not valid JSON - {e}")
            print(f"Response text: {response.text}")
            return False
        
    except Exception as e:
        print(f"❌ FAILED: Exception - {e}")
        import traceback
        traceback.print_exc()
        return False


def test_admin_login():
    """Test 2: POST /api/admin/auth/login with donas/Seinao10@@"""
    print("\n" + "="*70)
    print("TEST 2: Admin Login (POST /api/admin/auth/login)")
    print("="*70)
    
    url = f"{API_BASE}/admin/auth/login"
    payload = {
        "username": ADMIN_USERNAME,
        "password": ADMIN_PASSWORD
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        print(f"URL: {url}")
        print(f"Payload: {payload}")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code != 200:
            print(f"❌ FAILED: Expected 200, got {response.status_code}")
            print(f"Response: {response.text}")
            return None
        
        try:
            data = response.json()
            print(f"Response JSON keys: {list(data.keys())}")
            
            # Verify token exists
            if 'token' not in data:
                print("❌ FAILED: No 'token' in response")
                print(f"Response: {data}")
                return None
            
            # Verify user object exists
            if 'user' not in data:
                print("❌ FAILED: No 'user' object in response")
                print(f"Response: {data}")
                return None
            
            # Verify user.username matches
            if data['user'].get('username') != ADMIN_USERNAME:
                print(f"❌ FAILED: user.username != '{ADMIN_USERNAME}'")
                print(f"   Expected: {ADMIN_USERNAME}")
                print(f"   Got: {data['user'].get('username')}")
                return None
            
            print(f"✅ PASSED: Login successful")
            print(f"   Token (first 30 chars): {data['token'][:30]}...")
            print(f"   Username: {data['user']['username']}")
            return data['token']
            
        except Exception as e:
            print(f"❌ FAILED: Response parsing error - {e}")
            print(f"Response text: {response.text}")
            return None
        
    except Exception as e:
        print(f"❌ FAILED: Exception - {e}")
        import traceback
        traceback.print_exc()
        return None


def test_protected_route_with_token(token):
    """Test 3a: GET /api/admin/auth/me WITH Authorization header (should return 200)"""
    print("\n" + "="*70)
    print("TEST 3a: Protected Route WITH Token (GET /api/admin/auth/me)")
    print("="*70)
    
    url = f"{API_BASE}/admin/auth/me"
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        print(f"URL: {url}")
        print(f"Authorization: Bearer {token[:30]}...")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code != 200:
            print(f"❌ FAILED: Expected 200, got {response.status_code}")
            print(f"Response: {response.text}")
            return False
        
        try:
            data = response.json()
            print(f"Response JSON: {data}")
            
            if 'username' not in data:
                print("⚠️  Warning: Response does not contain 'username' field")
            else:
                print(f"   Username: {data['username']}")
            
            print(f"✅ PASSED: Protected route returns 200 with valid token")
            return True
            
        except Exception as e:
            print(f"❌ FAILED: Response is not valid JSON - {e}")
            print(f"Response text: {response.text}")
            return False
        
    except Exception as e:
        print(f"❌ FAILED: Exception - {e}")
        import traceback
        traceback.print_exc()
        return False


def test_protected_route_without_token():
    """Test 3b: GET /api/admin/auth/me WITHOUT Authorization header (should return 401/403)"""
    print("\n" + "="*70)
    print("TEST 3b: Protected Route WITHOUT Token (GET /api/admin/auth/me)")
    print("="*70)
    
    url = f"{API_BASE}/admin/auth/me"
    
    try:
        response = requests.get(url, timeout=10)
        print(f"URL: {url}")
        print(f"Authorization: (none)")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code not in [401, 403]:
            print(f"❌ FAILED: Expected 401 or 403, got {response.status_code}")
            print(f"Response: {response.text}")
            return False
        
        print(f"✅ PASSED: Protected route correctly returns {response.status_code} without token")
        return True
        
    except Exception as e:
        print(f"❌ FAILED: Exception - {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all validation tests"""
    print("\n" + "="*70)
    print("CLONE-AND-RUN VALIDATION TEST")
    print("FastAPI Backend Authentication & JWT")
    print("="*70)
    print(f"Base URL: {BASE_URL}")
    print(f"API Base: {API_BASE}")
    print(f"Admin User: {ADMIN_USERNAME}")
    
    results = {
        'passed': 0,
        'failed': 0,
        'total': 4
    }
    
    # Test 1: Root endpoint
    if test_root_endpoint():
        results['passed'] += 1
    else:
        results['failed'] += 1
    
    # Test 2: Login
    token = test_admin_login()
    if token:
        results['passed'] += 1
    else:
        results['failed'] += 1
        print("\n❌ Cannot proceed with JWT tests without valid token.")
        print_summary(results)
        return 1
    
    # Test 3a: Protected route WITH token
    if test_protected_route_with_token(token):
        results['passed'] += 1
    else:
        results['failed'] += 1
    
    # Test 3b: Protected route WITHOUT token
    if test_protected_route_without_token():
        results['passed'] += 1
    else:
        results['failed'] += 1
    
    print_summary(results)
    
    return 0 if results['failed'] == 0 else 1


def print_summary(results):
    """Print test summary"""
    print("\n" + "="*70)
    print("VALIDATION TEST SUMMARY")
    print("="*70)
    print(f"Total Tests: {results['total']}")
    print(f"✅ Passed: {results['passed']}")
    print(f"❌ Failed: {results['failed']}")
    
    if results['failed'] == 0:
        print("\n🎉 ALL TESTS PASSED - Backend is working correctly!")
        print("   ✓ Backend is online and responding")
        print("   ✓ Admin login works with correct credentials")
        print("   ✓ JWT authentication is functioning")
        print("   ✓ Protected routes are properly secured")
    else:
        print(f"\n⚠️  {results['failed']} TEST(S) FAILED - See details above")
    
    print("="*70)


if __name__ == "__main__":
    sys.exit(main())
