import sqlite3
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseConnection:
    """Manages SQLite database connection."""
    def __init__(self, db_name: str = 'yks_bot.db'):
        self.db_name = db_name
        self.conn = None

    def connect(self):
        """Establishes connection to SQLite database."""
        try:
            self.conn = sqlite3.connect(self.db_name)
            logger.info(f"Connected to database: {self.db_name}")
            return self.conn
        except sqlite3.Error as e:
            logger.error(f"Database connection error: {e}")
            raise

    def close(self):
        """Closes database connection."""
        if self.conn:
            self.conn.close()
            logger.info("Database connection closed")