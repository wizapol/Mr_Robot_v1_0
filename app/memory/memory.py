import sqlite3
import os

class MemoryController:
    def __init__(self, db_path="./app/memory/memory.db"):
        self.db_path = db_path
        self.connection = sqlite3.connect(db_path, check_same_thread=False)
        self._initialize_database()

    def _initialize_database(self):
        cursor = self.connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS memory (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        """)
        self.connection.commit()

    def store_memory(self, key, value):
        cursor = self.connection.cursor()
        cursor.execute("INSERT OR REPLACE INTO memory (key, value) VALUES (?, ?)", (key, value))
        self.connection.commit()

    def retrieve_memory(self, key):
        cursor = self.connection.cursor()
        cursor.execute("SELECT value FROM memory WHERE key = ?", (key,))
        result = cursor.fetchone()
        return result[0] if result else None

    def delete_memory(self, key):
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM memory WHERE key = ?", (key,))
        self.connection.commit()
        print("Deleted memory with key: {}".format(key))
