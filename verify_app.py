import urllib.request
import urllib.parse
import json
import time
import sys

BASE_URL = "http://127.0.0.1:5000"
COOKIE_JAR = {}

def make_request(endpoint, method='GET', data=None, headers=None):
    url = f"{BASE_URL}{endpoint}"
    if headers is None:
        headers = {}
    
    headers['Content-Type'] = 'application/json'
    
    # Add cookies
    if COOKIE_JAR:
        cookie_str = '; '.join([f"{k}={v}" for k, v in COOKIE_JAR.items()])
        headers['Cookie'] = cookie_str

    if data:
        data_bytes = json.dumps(data).encode('utf-8')
    else:
        data_bytes = None

    req = urllib.request.Request(url, data=data_bytes, headers=headers, method=method)
    
    try:
        with urllib.request.urlopen(req) as response:
            # Handle cookies
            cookies = response.headers.get_all('Set-Cookie')
            if cookies:
                for cookie in cookies:
                    parts = cookie.split(';')[0].split('=')
                    if len(parts) == 2:
                        COOKIE_JAR[parts[0]] = parts[1]
            
            resp_body = response.read().decode('utf-8')
            return response.status, json.loads(resp_body)
    except urllib.error.HTTPError as e:
        resp_body = e.read().decode('utf-8')
        try:
            return e.code, json.loads(resp_body)
        except:
            return e.code, resp_body
    except Exception as e:
        print(f"Request failed: {e}")
        return 0, None

def test_api():
    print("Starting API Verification (urllib)...")
    
    # 1. Register
    print("\n[1] Testing Registration...")
    reg_data = {
        "username": f"testuser_{int(time.time())}",
        "email": f"test_{int(time.time())}@example.com",
        "password": "password123",
        "age": 25,
        "contact_number": "1234567890"
    }
    status, resp = make_request("/api/auth/register", method='POST', data=reg_data)
    print(f"Register Status: {status}")
    print(f"Register Response: {resp}")
    if status != 201:
        print("Registration failed!")
        return

    # 2. Login
    print("\n[2] Testing Login...")
    login_data = {
        "username": reg_data["username"],
        "password": "password123"
    }
    status, resp = make_request("/api/auth/login", method='POST', data=login_data)
    print(f"Login Status: {status}")
    print(f"Login Response: {resp}")
    if status != 200:
        print("Login failed!")
        return

    # 3. Create News
    print("\n[3] Testing Create News...")
    news_data = {
        "title": "Test News Title",
        "body": "This is a test news body content."
    }
    status, resp = make_request("/api/news", method='POST', data=news_data)
    print(f"Create News Status: {status}")
    print(f"Create News Response: {resp}")
    if status != 201:
        print("Create News failed!")
        return

    # 4. Get News
    print("\n[4] Testing Get News...")
    status, news_list = make_request("/api/news", method='GET')
    print(f"Get News Status: {status}")
    print(f"Get News Count: {len(news_list) if isinstance(news_list, list) else 'Error'}")
    
    if isinstance(news_list, list):
        found = False
        for item in news_list:
            if item['title'] == news_data['title']:
                found = True
                break
        
        if found:
            print("SUCCESS: Created news item found in feed.")
        else:
            print("FAILURE: Created news item NOT found in feed.")
    else:
        print("FAILURE: Could not fetch news list.")

if __name__ == "__main__":
    test_api()
