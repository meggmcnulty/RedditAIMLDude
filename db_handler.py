import sqlite3
from datetime import datetime, timedelta
import config

class DatabaseHandler:
    def __init__(self):
        self.conn = sqlite3.connect(config.DB_FILE)
        self.create_tables()
    
    def create_tables(self):
        cursor = self.conn.cursor()
        
        # Table for tracking comments
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            post_id TEXT NOT NULL,
            comment_id TEXT NOT NULL,
            subreddit TEXT NOT NULL,
            timestamp DATETIME NOT NULL,
            UNIQUE(post_id, comment_id)
        )
        ''')
        
        # Table for tracking daily comment count
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS daily_stats (
            date DATE PRIMARY KEY,
            comment_count INTEGER DEFAULT 0
        )
        ''')
        
        self.conn.commit()
    
    def has_commented_on_post(self, post_id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT 1 FROM comments WHERE post_id = ?', (post_id,))
        return cursor.fetchone() is not None
    
    def add_comment(self, post_id, comment_id, subreddit):
        cursor = self.conn.cursor()
        now = datetime.now()
        
        # Add comment record
        cursor.execute('''
        INSERT INTO comments (post_id, comment_id, subreddit, timestamp)
        VALUES (?, ?, ?, ?)
        ''', (post_id, comment_id, subreddit, now))
        
        # Update daily stats
        today = now.date()
        cursor.execute('''
        INSERT INTO daily_stats (date, comment_count)
        VALUES (?, 1)
        ON CONFLICT(date) DO UPDATE SET
        comment_count = comment_count + 1
        ''', (today,))
        
        self.conn.commit()
    
    def get_today_comment_count(self):
        cursor = self.conn.cursor()
        today = datetime.now().date()
        cursor.execute('SELECT comment_count FROM daily_stats WHERE date = ?', (today,))
        result = cursor.fetchone()
        return result[0] if result else 0
    
    def can_post_today(self):
        return self.get_today_comment_count() < config.MAX_COMMENTS_PER_DAY
    
    def get_last_comment_time(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT MAX(timestamp) FROM comments')
        result = cursor.fetchone()
        if result and result[0]:
            return datetime.fromisoformat(result[0])
        return None
    
    def can_post_now(self):
        last_comment = self.get_last_comment_time()
        if not last_comment:
            return True
        
        time_since_last = datetime.now() - last_comment
        return time_since_last >= timedelta(hours=config.COMMENT_INTERVAL_HOURS)
    
    def close(self):
        self.conn.close() 