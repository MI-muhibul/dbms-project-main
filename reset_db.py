import mysql.connector

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'port': 3306,
    'database': 'news_blog_db'
}

def reset():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        print("Dropping tables...")
        cursor.execute("DROP TABLE IF EXISTS news")
        cursor.execute("DROP TABLE IF EXISTS users")
        
        conn.commit()
        cursor.close()
        conn.close()
        print("Tables dropped.")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    reset()
