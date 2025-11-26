from flask import Flask, render_template, jsonify, request, redirect, url_for, session
from database import Database
from mysql.connector import Error
import threading
import urllib.request
import urllib.parse
import os
import time
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__, template_folder='templates')
app.secret_key = 'your_secret_key_here'

# --- CONFIGURATION ---
DB_CONFIG = {
    'host': 'localhost',
    'database': 'news_blog_db',
    'user': 'root',
    'password': '',
    'port': 3306
}

# --- FLASK LOGIN SETUP ---
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login_page'

class User(UserMixin):
    def __init__(self, user_id, username, email, role='user'):
        self.id = user_id
        self.username = username
        self.email = email
        self.role = role

@login_manager.user_loader
def load_user(user_id):
    db = Database(**DB_CONFIG)
    try:
        user_data = db.fetch_one("SELECT * FROM users WHERE user_id = %s", (user_id,))
        if user_data:
            return User(user_data['user_id'], user_data['username'], user_data['email'])
        return None
    except Exception as e:
        print(f"Error loading user: {e}")
        return None
    finally:
        db.close()

# --- BACKGROUND TASKS ---
def generate_news_image(news_id, title, body):
    print(f"[{news_id}] Starting background image generation...")
    try:
        prompt = f"{title} {body[:50]}".strip()
        encoded_prompt = urllib.parse.quote(prompt)
        image_url = f"https://pollinations.ai/p/{encoded_prompt}?width=800&height=400&seed={news_id}&model=flux"
        
        filename = f"news_{news_id}.jpg"
        static_dir = os.path.join(app.root_path, 'static', 'news_images')
        if not os.path.exists(static_dir):
            os.makedirs(static_dir)
            
        file_path = os.path.join(static_dir, filename)
        
        print(f"[{news_id}] Downloading from: {image_url}")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Referer': 'https://pollinations.ai/',
            'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8'
        }
        req = urllib.request.Request(image_url, headers=headers)
        
        with urllib.request.urlopen(req) as response, open(file_path, 'wb') as out_file:
            out_file.write(response.read())
            
        print(f"[{news_id}] Image saved to: {file_path}")
        
        db = Database(**DB_CONFIG)
        try:
            db_image_path = f"/static/news_images/{filename}"
            db.execute_query("UPDATE news SET image_url = %s WHERE news_id = %s", (db_image_path, news_id))
            print(f"[{news_id}] Database updated with image.")
        finally:
            db.close()
        
    except Exception as e:
        with open("debug_log.txt", "a") as f:
            f.write(f"[{news_id}] ERROR: {e}\n")
        print(f"[{news_id}] ERROR generating image: {e}")

# --- ROUTING (VIEW) ---
@app.route('/')
@login_required
def index():
    return render_template('index.html', current_user=current_user)

@app.route('/login')
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    return render_template('login.html')

# --- AUTH API ---
@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.json
    db = Database(**DB_CONFIG)
    try:
        existing_user = db.fetch_one("SELECT user_id FROM users WHERE username = %s OR email = %s", (data['username'], data['email']))
        if existing_user:
            return jsonify({'error': 'Username or Email already exists'}), 400

        hashed_password = generate_password_hash(data['password'])
        query = "INSERT INTO users (username, email, password_hash, age, contact_number) VALUES (%s, %s, %s, %s, %s)"
        user_id = db.execute_query(query, (data['username'], data['email'], hashed_password, data.get('age'), data.get('contact_number')))
        
        user = User(user_id, data['username'], data['email'])
        login_user(user)
        
        return jsonify({'message': 'Registered successfully', 'user': {'id': user_id, 'username': user.username}}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.json
    db = Database(**DB_CONFIG)
    try:
        user_data = db.fetch_one("SELECT * FROM users WHERE username = %s", (data['username'],))
        
        if user_data and user_data['password_hash'] and check_password_hash(user_data['password_hash'], data['password']):
            user = User(user_data['user_id'], user_data['username'], user_data['email'])
            login_user(user)
            return jsonify({'message': 'Logged in successfully', 'user': {'id': user.id, 'username': user.username}})
        
        return jsonify({'error': 'Invalid username or password'}), 401
    finally:
        db.close()

@app.route('/api/auth/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'})

@app.route('/api/auth/me', methods=['GET'])
def get_current_user():
    if current_user.is_authenticated:
        return jsonify({'authenticated': True, 'user': {'id': current_user.id, 'username': current_user.username}})
    return jsonify({'authenticated': False})

# --- API CONTROLLERS ---
@app.route('/api/users', methods=['GET', 'POST'])
@login_required
def handle_users():
    db = Database(**DB_CONFIG)
    try:
        if request.method == 'GET':
            users = db.fetch_query("SELECT user_id, username, email, age, contact_number FROM users ORDER BY user_id DESC")
            return jsonify(users)
       
        if request.method == 'POST':
            data = request.json
            query = "INSERT INTO users (username, email, age, contact_number) VALUES (%s, %s, %s, %s)"
            user_id = db.execute_query(query, (data['username'], data['email'], data['age'], data['contact_number']))
            return jsonify({'message': 'User created', 'id': user_id}), 201
           
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()

@app.route('/api/users/<int:user_id>', methods=['PUT', 'DELETE'])
@login_required
def handle_single_user(user_id):
    if current_user.id != user_id:
         return jsonify({'error': 'Unauthorized'}), 403

    db = Database(**DB_CONFIG)
    try:
        if request.method == 'PUT':
            data = request.json
            query = "UPDATE users SET username=%s, email=%s, age=%s, contact_number=%s WHERE user_id=%s"
            db.execute_query(query, (data['username'], data['email'], data['age'], data['contact_number'], user_id))
            return jsonify({'message': 'User updated'})

        if request.method == 'DELETE':
            db.execute_query("DELETE FROM users WHERE user_id = %s", (user_id,))
            logout_user()
            return jsonify({'message': 'User deleted'})
           
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()

@app.route('/api/news', methods=['GET', 'POST'])
@login_required
def handle_news():
    db = Database(**DB_CONFIG)
    try:
        if request.method == 'GET':
            query = """
                SELECT news.*, users.username
                FROM news
                JOIN users ON news.user_id = users.user_id
                ORDER BY created_at DESC
            """
            news = db.fetch_query(query)
            return jsonify(news)

        if request.method == 'POST':
            data = request.json
            user_id = current_user.id
            
            # Generate a random image URL (simulating AI generation)
            import random
            image_url = f"https://picsum.photos/seed/{random.randint(1, 10000)}/800/400"

            query = "INSERT INTO news (title, body, user_id, image_url) VALUES (%s, %s, %s, %s)"
            news_id = db.execute_query(query, (data['title'], data['body'], user_id, image_url))
            
            return jsonify({'message': 'News added'}), 201

    except Exception as e:
        print(f"ERROR in handle_news: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()

@app.route('/api/news/<int:news_id>', methods=['PUT', 'DELETE'])
@login_required
def handle_news_item(news_id):
    db = Database(**DB_CONFIG)
    try:
        news_item = db.fetch_one("SELECT user_id FROM news WHERE news_id = %s", (news_id,))
        if not news_item:
            return jsonify({'error': 'News not found'}), 404
            
        if news_item['user_id'] != current_user.id:
            return jsonify({'error': 'Unauthorized'}), 403

        if request.method == 'PUT':
            data = request.json
            query = "UPDATE news SET title=%s, body=%s WHERE news_id=%s"
            db.execute_query(query, (data['title'], data['body'], news_id))
           
        if request.method == 'DELETE':
            db.execute_query("DELETE FROM news WHERE news_id=%s", (news_id,))
           
        return jsonify({'message': 'Success'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()

@app.route('/api/users/<int:user_id>/news', methods=['GET'])
@login_required
def get_user_news(user_id):
    db = Database(**DB_CONFIG)
    try:
        news = db.fetch_query("SELECT * FROM news WHERE user_id = %s ORDER BY created_at DESC", (user_id,))
        return jsonify(news)
    finally:
        db.close()

if __name__ == '__main__':
    app.run(debug=True, use_debugger=False, port=5000)
