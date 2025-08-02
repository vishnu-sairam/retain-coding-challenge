"""Database connection and management utilities"""

import sqlite3
import threading
from contextlib import contextmanager
from config import Config


class DatabaseManager:
    """Thread-safe database connection manager"""
    
    def __init__(self, db_path=None):
        self.db_path = db_path or Config.DATABASE_PATH
        self._local = threading.local()
    
    def get_connection(self):
        """Get a thread-local database connection"""
        if not hasattr(self._local, 'connection'):
            self._local.connection = sqlite3.connect(
                self.db_path,
                check_same_thread=True  # Secure: each thread gets its own connection
            )
            self._local.connection.row_factory = sqlite3.Row  # Enable dict-like access
        return self._local.connection
    
    @contextmanager
    def get_cursor(self):
        """Context manager for database operations with automatic commit/rollback"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            yield cursor
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
    
    def close_connection(self):
        """Close the thread-local connection"""
        if hasattr(self._local, 'connection'):
            self._local.connection.close()
            delattr(self._local, 'connection')


# Global database manager instance
db_manager = DatabaseManager()
