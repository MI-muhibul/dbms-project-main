import mysql.connector
from mysql.connector import Error

class Database:
    def __init__(self, host, user, password, database, port=3306):
        self.conn = None
        self.cursor = None
        try:
            self.conn = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database,
                port=port
            )
            self.cursor = self.conn.cursor(dictionary=True)
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            raise e

    def execute_query(self, query, params=None):
        if not self.conn or not self.conn.is_connected():
            return None
        try:
            self.cursor.execute(query, params or ())
            self.conn.commit()
            return self.cursor.lastrowid
        except Error as e:
            print(f"Error executing query: {e}")
            raise e

    def fetch_query(self, query, params=None):
        if not self.conn or not self.conn.is_connected():
            return None
        try:
            self.cursor.execute(query, params or ())
            return self.cursor.fetchall()
        except Error as e:
            print(f"Error fetching data: {e}")
            raise e

    def fetch_one(self, query, params=None):
        if not self.conn or not self.conn.is_connected():
            return None
        try:
            self.cursor.execute(query, params or ())
            return self.cursor.fetchone()
        except Error as e:
            print(f"Error fetching data: {e}")
            raise e

    def close(self):
        if self.conn and self.conn.is_connected():
            self.cursor.close()
            self.conn.close()
