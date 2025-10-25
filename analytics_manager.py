import sqlite3
from datetime import datetime, timedelta
from config import ANALYTICS_DB_PATH

class AnalyticsManager:
    def __init__(self):
        self.db_path = ANALYTICS_DB_PATH
        self.init_database()
    
    def init_database(self):
        """Analytics database setup"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Post analytics table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS post_analytics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                media_id TEXT UNIQUE,
                username TEXT,
                video_filename TEXT,
                upload_date TIMESTAMP,
                likes INTEGER DEFAULT 0,
                comments INTEGER DEFAULT 0,
                views INTEGER DEFAULT 0,
                shares INTEGER DEFAULT 0,
                saves INTEGER DEFAULT 0,
                engagement_rate REAL DEFAULT 0,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Account growth table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS account_growth (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                followers INTEGER,
                following INTEGER,
                total_posts INTEGER,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Best posting times
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS best_times (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                hour INTEGER,
                avg_engagement REAL,
                post_count INTEGER,
                UNIQUE(username, hour)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_post_analytics(self, media_id, username, video_filename, likes, comments, views, shares=0, saves=0):
        """Post ka analytics save karo"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Engagement rate calculate
        total_engagement = likes + comments + shares + saves
        engagement_rate = (total_engagement / max(views, 1)) * 100 if views > 0 else 0
        
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO post_analytics 
                (media_id, username, video_filename, upload_date, likes, comments, views, shares, saves, engagement_rate)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (media_id, username, video_filename, datetime.now(), likes, comments, views, shares, saves, engagement_rate))
            
            conn.commit()
        except Exception as e:
            print(f"Error saving analytics: {e}")
        finally:
            conn.close()
    
    def save_account_growth(self, username, followers, following, total_posts):
        """Account growth track karo"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO account_growth (username, followers, following, total_posts)
            VALUES (?, ?, ?, ?)
        ''', (username, followers, following, total_posts))
        
        conn.commit()
        conn.close()
    
    def get_total_engagement(self, username, days=7):
        """Last X days ka total engagement"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        date_limit = datetime.now() - timedelta(days=days)
        
        cursor.execute('''
            SELECT 
                SUM(likes) as total_likes,
                SUM(comments) as total_comments,
                SUM(views) as total_views,
                AVG(engagement_rate) as avg_engagement
            FROM post_analytics
            WHERE username = ? AND upload_date >= ?
        ''', (username, date_limit))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                'total_likes': result[0] or 0,
                'total_comments': result[1] or 0,
                'total_views': result[2] or 0,
                'avg_engagement': round(result[3] or 0, 2)
            }
        return None
    
    def get_best_performing_posts(self, username, limit=5):
        """Top performing videos"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT video_filename, likes, comments, views, engagement_rate
            FROM post_analytics
            WHERE username = ?
            ORDER BY engagement_rate DESC
            LIMIT ?
        ''', (username, limit))
        
        posts = cursor.fetchall()
        conn.close()
        
        return posts
    
    def get_follower_growth(self, username, days=30):
        """Follower growth track karo"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        date_limit = datetime.now() - timedelta(days=days)
        
        cursor.execute('''
            SELECT date, followers
            FROM account_growth
            WHERE username = ? AND date >= ?
            ORDER BY date ASC
        ''', (username, date_limit))
        
        growth = cursor.fetchall()
        conn.close()
        
        return growth
    
        def fix_missing_columns(self):
            """Fix missing columns in existing database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Add viral_score column if missing
            cursor.execute('''
                ALTER TABLE post_analytics 
                ADD COLUMN viral_score REAL DEFAULT 0
            ''')
            print("✅ Added viral_score column")
        except:
            pass  # Column already exists
        
        try:
            # Add upload_hour column if missing
            cursor.execute('''
                ALTER TABLE post_analytics 
                ADD COLUMN upload_hour INTEGER DEFAULT 0
            ''')
            print("✅ Added upload_hour column")
        except:
            pass
        
        try:
            # Add upload_day_of_week column if missing
            cursor.execute('''
                ALTER TABLE post_analytics 
                ADD COLUMN upload_day_of_week INTEGER DEFAULT 0
            ''')
            print("✅ Added upload_day_of_week column")
        except:
            pass

    def analyze_best_posting_time(self, username):
        """Best posting time analyze karo based on engagement"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                CAST(strftime('%H', upload_date) AS INTEGER) as hour,
                AVG(engagement_rate) as avg_engagement,
                COUNT(*) as post_count
            FROM post_analytics
            WHERE username = ?
            GROUP BY hour
            HAVING post_count >= 2
            ORDER BY avg_engagement DESC
            LIMIT 5
        ''', (username,))
        
        
        best_times = cursor.fetchall()
        conn.close()
        
        return best_times
