#database/database_manager.py
import sqlite3 
import logging
from pathlib import Path

# Ensure the logs directory exists
class DatabaseManager:
    """データベース管理クラス"""

def __init__(self, db_path):
    """
    コンストラクタ

    Args:
        db_path (str): データベースファイルパス
    """
    self.db_path = db_path
    self.connection = None
    self.cursor = None
    self.logger = logging.getLogger(__name__)

    def connect(self):
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.cursor = self.connection.cursor()
            logging.info(f"Connected to database at {self.db_path}")
        except sqlite3.Error as e:
            logging.error(f"Error connecting to database: {e}")
            raise

    def execute_query(self, query, params=None):
        if not self.connection:
            raise Exception("Database connection is not established.")
        
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.connection.commit()
            logging.info("Query executed successfully.")
        except sqlite3.Error as e:
            logging.error(f"Error executing query: {e}")
            raise

    def fetch_all(self):
        if not self.cursor:
            raise Exception("Cursor is not available.")
        
        try:
            results = self.cursor.fetchall()
            logging.info("Fetched all results successfully.")
            return results
        except sqlite3.Error as e:
            logging.error(f"Error fetching results: {e}")
            raise

    def close(self):
        if self.connection:
            self.connection.close()
            logging.info("Database connection closed.")
