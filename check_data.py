import mysql.connector

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'port': 3306,
    'database': 'news_blog_db'
}

def check():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        
        print("--- Latest 5 News Items ---")
        cursor.execute("""
            SELECT news.news_id, news.title, news.created_at, users.username, news.image_url 
            FROM news 
            JOIN users ON news.user_id = users.user_id 
            ORDER BY news.created_at DESC 
            LIMIT 5
        """)
        for row in cursor.fetchall():
            print(row)
            
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check()
