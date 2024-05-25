import sqlite3
from datetime import datetime

class GameDatabase:
    def __init__(self, db_name="minesweeper.db"):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS game_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                time_of_day TEXT,
                duration REAL,
                outcome TEXT,
                mines_left INTEGER
            )
        """)
        self.connection.commit()

    def add_record(self, duration, outcome, mines_left):
        now = datetime.now()
        date = now.strftime("%Y-%m-%d")
        time_of_day = now.strftime("%H:%M:%S")
        self.cursor.execute("""
            INSERT INTO game_records (date, time_of_day, duration, outcome, mines_left)
            VALUES (?, ?, ?, ?, ?)
        """, (date, time_of_day, duration, outcome, mines_left))
        self.connection.commit()

    def get_all_records(self):
        self.cursor.execute("SELECT * FROM game_records")
        return self.cursor.fetchall()

    def close(self):
        self.connection.close()