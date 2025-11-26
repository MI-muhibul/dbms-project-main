import mysql.connector
import random
from werkzeug.security import generate_password_hash
import datetime

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

        # 4. Seeding Data
        cursor.execute("SELECT COUNT(*) FROM users")
        if cursor.fetchone()[0] == 0:
            print("[*] Seeding data (5 Users, 20 News items)...")
           
            # Create Specific Users
            users = [
                ("Journalist", "journalist@news.com"),
                ("Abir", "abir@example.com"),
                ("Alice Smith", "alice@example.com"),
                ("Bob Jones", "bob@example.com"),
                ("Charlie Brown", "charlie@example.com"),
                ("Diana Prince", "diana@example.com"),
                ("Eve Wilson", "eve@example.com"),
                ("Frank Miller", "frank@example.com"),
                ("Grace Lee", "grace@example.com"),
                ("Hank Green", "hank@example.com")
            ]
            
            common_password_hash = generate_password_hash("12345678")
            
            users_data = []
            for username, email in users:
                users_data.append((username, email, common_password_hash, random.randint(25, 45), f"555-{random.randint(1000,9999)}"))
           
            cursor.executemany("INSERT INTO users (username, email, password_hash, age, contact_number) VALUES (%s, %s, %s, %s, %s)", users_data)
            conn.commit()

            # Get User IDs
            cursor.execute("SELECT user_id, username FROM users")
            user_map = {row[1]: row[0] for row in cursor.fetchall()}

            # Sample news content (3 per user)
            news_items = [
                # Journalist
                ("Journalist", "Global Climate Summit Results", "World leaders agree on ambitious new carbon reduction targets for 2030. The summit concluded with a historic agreement signed by 195 nations.", "https://picsum.photos/seed/climate1/800/400"),
                ("Journalist", "Diplomatic Tensions in Eastern Europe", "Peace talks stall as border disputes continue to escalate. International observers have reported increased military activity.", "https://picsum.photos/seed/eu1/800/400"),
                ("Journalist", "Tech Giants Face New Regulations", "The EU announces strict new privacy laws affecting major tech companies. The Digital Markets Act aims to curb the dominance of big tech firms.", "https://picsum.photos/seed/tech1/800/400"),

                # Abir
                ("Abir", "My First Tech Review", "Testing the latest smartphone camera capabilities in low light. The results were surprising. The night mode captured details that were invisible to the naked eye.", "https://picsum.photos/seed/phone1/800/400"),
                ("Abir", "Coding Bootcamp Experience", "Reflecting on 12 weeks of intensive Python learning. It was a challenging journey, but the skills I gained are invaluable.", "https://picsum.photos/seed/code1/800/400"),
                ("Abir", "Travel Diary: Japan", "Exploring the streets of Tokyo and the temples of Kyoto. The blend of ultra-modern technology and ancient tradition is fascinating.", "https://picsum.photos/seed/japan1/800/400"),

                # Alice Smith
                ("Alice Smith", "AI Breakthrough in Healthcare", "New artificial intelligence models are predicting diseases with 99% accuracy, revolutionizing early diagnosis.", "https://picsum.photos/seed/ai1/800/400"),
                ("Alice Smith", "The Future of Remote Work", "Studies show that 70% of companies plan to keep hybrid work models permanently. Employees report higher satisfaction.", "https://picsum.photos/seed/work1/800/400"),
                ("Alice Smith", "Sustainable Fashion Trends", "How the fashion industry is pivoting towards eco-friendly materials and ethical labor practices.", "https://picsum.photos/seed/fashion1/800/400"),

                # Bob Jones
                ("Bob Jones", "Local Sports Team Wins Championship", "The city celebrates as the Tigers take home the trophy after a 20-year drought. The parade is scheduled for this Friday.", "https://picsum.photos/seed/sport1/800/400"),
                ("Bob Jones", "New Park Opens Downtown", "A green oasis in the middle of the city, featuring playgrounds and walking trails. The park was designed by renowned landscape architects.", "https://picsum.photos/seed/park1/800/400"),
                ("Bob Jones", "Traffic Updates for the Weekend", "Major road closures expected due to the marathon. Plan your commute accordingly. The downtown area will be closed.", "https://picsum.photos/seed/traffic1/800/400"),

                # Charlie Brown
                ("Charlie Brown", "Best Coffee Shops in Town", "A guide to the coziest spots for your morning brew. We rated them based on bean quality, atmosphere, and pastry selection.", "https://picsum.photos/seed/coffee1/800/400"),
                ("Charlie Brown", "Review: The New Sci-Fi Blockbuster", "Visually stunning but lacks narrative depth. A mixed bag for genre fans. The special effects are groundbreaking.", "https://picsum.photos/seed/movie1/800/400"),
                ("Charlie Brown", "Top 10 Books of 2025", "Our curated list of must-read novels and non-fiction from the past year. Includes the Pulitzer Prize winner.", "https://picsum.photos/seed/book1/800/400"),

                # Diana Prince
                ("Diana Prince", "Museum Exhibition Opens", "Ancient artifacts from Egypt are now on display at the National Museum. The collection includes the golden mask of a pharaoh.", "https://picsum.photos/seed/museum1/800/400"),
                ("Diana Prince", "Charity Gala Raises Millions", "Local philanthropists gather to support education initiatives. The event featured a silent auction and a performance.", "https://picsum.photos/seed/gala1/800/400"),
                ("Diana Prince", "The Art of Pottery", "A workshop on traditional ceramic techniques attracts artists from all over. Participants learned how to throw clay.", "https://picsum.photos/seed/pottery1/800/400"),
                
                # Eve Wilson
                ("Eve Wilson", "Gardening Tips for Spring", "How to prepare your soil for the upcoming planting season. Adding compost and mulch now will ensure a bountiful harvest.", "https://picsum.photos/seed/garden1/800/400"),
                ("Eve Wilson", "Homemade Pasta Recipe", "A simple guide to making fresh pasta from scratch. All you need is flour, eggs, and a little patience.", "https://picsum.photos/seed/pasta1/800/400"),
                ("Eve Wilson", "Yoga for Beginners", "Five essential poses to improve flexibility and reduce stress. Remember to focus on your breath and listen to your body.", "https://picsum.photos/seed/yoga1/800/400"),

                # Frank Miller
                ("Frank Miller", "Investment Strategies 101", "Understanding the basics of stocks, bonds, and mutual funds. Diversification is the golden rule of investing.", "https://picsum.photos/seed/money1/800/400"),
                ("Frank Miller", "Real Estate Market Trends", "Housing prices continue to rise despite higher interest rates. Inventory remains low in popular neighborhoods.", "https://picsum.photos/seed/house1/800/400"),
                ("Frank Miller", "Cryptocurrency Update", "Bitcoin rallies as institutional adoption grows. Major banks are now offering crypto custody services.", "https://picsum.photos/seed/crypto1/800/400"),

                # Grace Lee
                ("Grace Lee", "Music Festival Preview", "The lineup for this year's Summer Sound fest is incredible. Headliners include The Weeknd and Dua Lipa.", "https://picsum.photos/seed/music1/800/400"),
                ("Grace Lee", "Indie Game Spotlight", "Reviewing 'Stardew Valley', a farming simulator with heart. The pixel art is charming, and the gameplay loop is addictive.", "https://picsum.photos/seed/game1/800/400"),
                ("Grace Lee", "Photography Basics", "Understanding the exposure triangle: Aperture, Shutter Speed, and ISO. Mastering these three settings will give you full creative control.", "https://picsum.photos/seed/photo1/800/400"),

                # Hank Green
                ("Hank Green", "Science News: Mars Mission", "NASA announces new timeline for the first human landing on Mars. The Artemis program will serve as a stepping stone.", "https://picsum.photos/seed/mars1/800/400"),
                ("Hank Green", "The Power of Curiosity", "Why asking questions is the key to learning and innovation. Curiosity drives us to explore the unknown.", "https://picsum.photos/seed/science1/800/400"),
                ("Hank Green", "Renewable Energy Tech", "New solar panel efficiency records set by researchers. Perovskite solar cells are showing great promise.", "https://picsum.photos/seed/solar1/800/400")
            ]

            news_data = []
            for username, title, body, image_url in news_items:
                if username in user_map:
                    news_data.append((title, body, user_map[username], image_url))
            
            cursor.executemany("INSERT INTO news (title, body, user_id, image_url) VALUES (%s, %s, %s, %s)", news_data)
            conn.commit()
            print("[+] Data seeding complete.")
        else:
            print("[-] Data already exists. Skipping seed.")

        cursor.close()
        conn.close()
        print("--- Initialization Success ---")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

if __name__ == "__main__":
    init_db()
