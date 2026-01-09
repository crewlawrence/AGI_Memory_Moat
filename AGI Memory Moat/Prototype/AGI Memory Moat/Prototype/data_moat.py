import sqlite3
import json

class DataMoat:
    def __init__(self):
db_path='moat.db'):
        self.conn =
sqlite3.connect(db_path)
        self.conn.execute('''CREATE TABLE IF NOT EXISTS proprietary_data
                          (id INTEGER PRIMARY KEY, key TEXT UNIQUE, value TEXT)''')

 def add_data(self, key, value):
        """Accumulate data from AGI loops (e.g., user insights)."""
        self.conn.execute("INSERT OR REPLACE INTO proprietary_data (key, value) VALUES (?, ?)", (key, json.dumps(value)))
        self.conn.commit()

    def get_data(self, key):
        cur = self.conn.execute("SELECT value FROM proprietary_data WHERE key=?", (key,))
        row = cur.fetchone()
        return json.loads(row[0]) if row else None

    def query(self, query_str):
        """Simple search; expand to vector later."""
        cur = self.conn.execute("SELECT key, value FROM proprietary_data WHERE key LIKE ?", (f"%{query_str}%",))
        return [json.loads(row[1]) for row in cur.fetchall()]