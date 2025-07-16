import sqlite3
import asyncio
from datetime import datetime
from contextlib import contextmanager


class Database:
    def __init__(self, db_path="complaints.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with self._get_sync_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS complaints (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    text TEXT NOT NULL,
                    status TEXT DEFAULT 'open',
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    sentiment TEXT DEFAULT 'unknown',
                    category TEXT DEFAULT 'другое'
                )
            """)

    @contextmanager
    def _get_sync_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Для доступа к колонкам по имени
        try:
            yield conn
        finally:
            conn.close()

    async def _run_db_query(self, query, params=None, fetch=False):
        def sync_query():
            with self._get_sync_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params or ())
                if fetch:
                    return cursor.fetchall()
                conn.commit()
                return cursor.lastrowid

        return await asyncio.get_event_loop().run_in_executor(None, sync_query)

    async def insert_complaint(self, text: str) -> int:
        return await self._run_db_query(
            "INSERT INTO complaints (text) VALUES (?)",
            (text,)
        )

    async def update_sentiment(self, complaint_id: int, sentiment: str):
        await self._run_db_query(
            "UPDATE complaints SET sentiment = ? WHERE id = ?",
            (sentiment, complaint_id)
        )

    async def update_category(self, complaint_id: int, category: str):
        await self._run_db_query(
            "UPDATE complaints SET category = ? WHERE id = ?",
            (category, complaint_id)
        )

    async def get_complaint(self, complaint_id: int) -> dict:
        result = await self._run_db_query(
            "SELECT id, text, status, timestamp, sentiment, category FROM complaints WHERE id = ?",
            (complaint_id,),
            fetch=True
        )
        return dict(result[0]) if result else None