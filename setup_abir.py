import urllib.request
import urllib.parse
import json
import time

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

def run_scenario():
    print("--- Starting Abir Scenario (urllib) ---")
    
    # 1. Register
    print("[1] Registering 'abir'...")
    reg_data = {
        "username": "abir",
        "email": "abir@test.com",
        "password": "12345678",
        "age": 25,
        "contact_number": "123456"
    }
    status, resp = make_request("/api/auth/register", method='POST', data=reg_data)
    print(f"Register Status: {status}")
    print(f"Register Response: {resp}")

    # 2. Login
    print("\n[2] Logging in...")
    login_data = {
        "username": "abir",
        "password": "12345678"
    }
    status, resp = make_request("/api/auth/login", method='POST', data=login_data)
    print(f"Login Status: {status}")
    
    if status != 200:
        print("Login failed, cannot post news.")
        return

    # 3. Post News
    print("\n[3] Posting News...")
    news_data = {
        "title": "My Friend",
        "body": "This is a news post about my best friend."
    }
    status, resp = make_request("/api/news", method='POST', data=news_data)
    print(f"Post News Status: {status}")
    print(f"Post News Response: {resp}")
    
    if status == 201:
        print("\nSUCCESS: User 'abir' registered and news posted.")
    else:
        print("\nFAILURE: Could not post news.")

if __name__ == "__main__":
    run_scenario()
