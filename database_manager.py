import sqlite3
from datetime import datetime
import os
from config import DATABASE_PATH

class DatabaseManager:
    def __init__(self):
        self.db_path = DATABASE_PATH
        self.init_database()
    
    def init_database(self):
        """Database tables create karo"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Uploaded videos tracking table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS uploaded_videos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                video_filename TEXT NOT NULL,
                account_username TEXT NOT NULL,
                upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                caption_used TEXT,
                video_path TEXT,
                status TEXT DEFAULT 'success',
                UNIQUE(video_filename, account_username)
            )
        ''')
        
        # Accounts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                session_file TEXT,
                added_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_post_date TIMESTAMP,
                total_posts INTEGER DEFAULT 0,
                is_active INTEGER DEFAULT 1
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def is_video_uploaded(self, video_filename, username):
        """Check karo ki video already uploaded hai ya nahi"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id FROM uploaded_videos 
            WHERE video_filename = ? AND account_username = ?
        ''', (video_filename, username))
        
        result = cursor.fetchone()
        conn.close()
        
        return result is not None
    
    def add_uploaded_video(self, video_filename, username, caption, video_path):
        """Uploaded video ko database me save karo"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO uploaded_videos 
                (video_filename, account_username, caption_used, video_path)
                VALUES (?, ?, ?, ?)
            ''', (video_filename, username, caption, video_path))
            
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()
    
    def add_account(self, username, password, session_file):
        """Naya account database me add karo"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO accounts (username, password, session_file)
                VALUES (?, ?, ?)
            ''', (username, password, session_file))
            
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()
    
    def get_all_accounts(self):
        """Saare accounts retrieve karo"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT username, is_active FROM accounts')
        accounts = cursor.fetchall()
        conn.close()
        
        return accounts
    
    def get_account_credentials(self, username):
        """Specific account ki credentials get karo"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT password, session_file FROM accounts 
            WHERE username = ?
        ''', (username,))
        
        result = cursor.fetchone()
        conn.close()
        
        return result
    
    def update_account_post_count(self, username):
        """Account ka post count update karo"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE accounts 
            SET total_posts = total_posts + 1, 
                last_post_date = CURRENT_TIMESTAMP
            WHERE username = ?
        ''', (username,))
        
        conn.commit()
        conn.close()
    
    def get_today_post_count(self, username):
        """Aaj kitne posts kiye, count karo"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT COUNT(*) FROM uploaded_videos 
            WHERE account_username = ? 
            AND DATE(upload_date) = DATE('now')
        ''', (username,))
        
        count = cursor.fetchone()[0]
        conn.close()
        
        return count
    
    def get_uploaded_videos_list(self, username):
        """Account ke uploaded videos list"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT video_filename, upload_date FROM uploaded_videos 
            WHERE account_username = ?
            ORDER BY upload_date DESC
            LIMIT 50
        ''', (username,))
        
        videos = cursor.fetchall()
        conn.close()
        
        return videos
    
    def delete_account(self, username):
        """Account delete karo"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM accounts WHERE username = ?', (username,))
        conn.commit()
        conn.close()

