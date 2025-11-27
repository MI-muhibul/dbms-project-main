import mysql.connector

# Configuration for XAMPP
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'port': 3306
}

def init_db():
    print("--- Starting Database Initialization ---")
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # 1. Create Database
        cursor.execute("CREATE DATABASE IF NOT EXISTS news_blog_db")
        cursor.execute("USE news_blog_db")
        print("[+] Database selected.")

        # 2. Create Users Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL,
            password_hash VARCHAR(255),
            age INT,
            contact_number VARCHAR(20)
        )
        """)
        print("[+] Users table ready.")

        # 3. Create News Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS news (
            news_id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            body TEXT NOT NULL,
            image_url VARCHAR(255),
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            user_id INT,
            FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
        )
        """)
        print("[+] News table ready.")

        cursor.close()
        conn.close()
        print("--- Initialization Success ---")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

if __name__ == "__main__":
    init_db()
