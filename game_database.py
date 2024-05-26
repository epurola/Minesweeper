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
                mines_left INTEGER,
                turns INTEGER
            )
        """)
        self.connection.commit()

    def add_record(self, duration, outcome, mines_left, turns):
        now = datetime.now()
        date = now.strftime("%Y-%m-%d")
        time_of_day = now.strftime("%H:%M:%S")
        self.cursor.execute("""
            INSERT INTO game_records (date, time_of_day, duration, outcome, mines_left, turns)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (date,time_of_day, duration, outcome, mines_left, turns))
        self.connection.commit()
   

    def get_all_records(self):
        self.cursor.execute("SELECT * FROM game_records")
        return self.cursor.fetchall()
    
    def get_best_time(self):
        self.cursor.execute("SELECT MIN(duration) FROM game_records WHERE outcome = 'Win'")
        result = self.cursor.fetchone()
        return result[0] if result[0] is not None else "No wins yet"
    
    def get_win_amount(self):
        self.cursor.execute("SELECT COUNT(*) FROM game_records WHERE outcome = 'Win'")
        result = self.cursor.fetchone()
        return result[0] if result else 0
    
    def get_loss_amount(self):
        self.cursor.execute("SELECT COUNT(*) FROM game_records WHERE outcome = 'Loss'")
        result = self.cursor.fetchone()
        return result[0] if result else 0
    
    def get_matches_amount(self):
        self.cursor.execute("SELECT COUNT(*) FROM game_records WHERE outcome = 'Loss' OR outcome = 'Win'")
        result = self.cursor.fetchone()
        return result[0] if result else 0
    
    def get_time_wasted(self):
       self.cursor.execute("SELECT duration FROM game_records")
       records = self.cursor.fetchall()
       total_duration = 0

       for record in records:
         duration_str = record[0]  
         hours, minutes, seconds = map(int, duration_str.split(':'))
         total_seconds = hours * 3600 + minutes * 60 + seconds
         total_duration += total_seconds
         
       total_hours = total_duration // 3600
       total_minutes = (total_duration % 3600) // 60
       total_seconds = total_duration % 60
       return f"{total_hours:02d}:{total_minutes:02d}:{total_seconds:02d}"
        
    def get_win_rate(self):
       self.cursor.execute("SELECT COUNT(*) FROM game_records WHERE outcome = 'Win'")
       wins = self.cursor.fetchone()[0]
       self.cursor.execute("SELECT COUNT(*) FROM game_records")
       total_games = self.cursor.fetchone()[0]
       if total_games == 0:
        return 0  
       win_rate = (wins / total_games) * 100
       return round(win_rate, 2)

    def close(self):
        self.connection.close()