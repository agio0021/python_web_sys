# database/database_manager.py
import sqlite3
import logging
from pathlib import Path


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
    
    def initialize_database(self):
        """データベースの初期化"""
        if not Path(self.db_path).exists():
            self.logger.info(f"Database file {self.db_path} does not exist. Creating new database.")
            self.connect()

            # テーブル作成
            create_table_sql = """
            CREATE TABLE IF NOT EXISTS employees (
                employee_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                name_kana TEXT NOT NULL,
                department TEXT NOT NULL,
                position TEXT NOT NULL,
                hire_date TEXT NOT NULL,
                salary INTEGER NOT NULL,
                email TEXT NOT NULL UNIQUE,
                phone TEXT,
                postal_code TEXT,
                address TEXT,
                notes TEXT,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """

            self.cursor.execute(create_table_sql)

            # インデックス作成
            index_sqls = [
                "CREATE INDEX IF NOT EXISTS idx_employees_name ON employees(name)",
                "CREATE INDEX IF NOT EXISTS idx_employees_department ON employees(department)",
                "CREATE INDEX IF NOT EXISTS idx_employees_position ON employees(position)"
            ]

            for index_sql in index_sqls:
                self.cursor.execute(index_sql)

            self.connection.commit()
            self.connection.close()
            return True

        else:
            self.logger.info(f"Database file {self.db_path} already exists. Skipping initialization.")
            self.connect()
            return True

    def connect(self):
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.cursor = self.connection.cursor()
            self.logger.info(f"Connected to database at {self.db_path}")
        except sqlite3.Error as e:
            self.logger.error(f"Error connecting to database: {e}")
            raise

    def execute_query(self, query, params=None):
        if not self.connection:
            raise Exception("Database connection is not established.")

        try:
            if params is not None:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.connection.commit()
            self.logger.info("Query executed successfully.")
        except sqlite3.Error as e:
            self.logger.error(f"Error executing query: {e}")
            raise

    def fetch_all(self):
        if not self.cursor:
            raise Exception("Cursor is not available.")

        try:
            results = self.cursor.fetchall()
            self.logger.info("Fetched all results successfully.")
            return results
        except sqlite3.Error as e:
            self.logger.error(f"Error fetching results: {e}")
            raise

    def close(self):
        if self.connection:
            self.connection.close()
            self.logger.info("Database connection closed.")

# 動作確認用テストブロック
if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)
    from config import Config

    db_manager = DatabaseManager(Config.DATABASE_PATH)
    success = db_manager.initialize_database()

    if success:
        print("Database initialized successfully.")
        db_manager.connect()
        db_manager.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = db_manager.cursor.fetchall()
        table_exists = len(tables) > 0
        assert table_exists, "Employees table was not created successfully."
        print(f"テーブル一覧: {[t[0] for t in tables]}")
        db_manager.close()
    else:
        print("✗ データベース初期化失敗")
