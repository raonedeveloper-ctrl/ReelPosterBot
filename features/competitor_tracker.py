from instagrapi import Client
import time
from datetime import datetime, timedelta
import sqlite3

class CompetitorTracker:
    """Track and analyze competitor accounts"""
    
    def __init__(self, client):
        self.client = client
        self.db_path = "data/competitors.db"
        self._init_database()
    
    def _init_database(self):
        """Initialize competitor database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS competitors (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE,
                added_date TEXT,
                last_checked TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS competitor_posts (
                id INTEGER PRIMARY KEY,
                competitor_username TEXT,
                media_id TEXT UNIQUE,
                caption TEXT,
                likes INTEGER,
                comments INTEGER,
                views INTEGER,
                posted_date TEXT,
                hashtags TEXT,
                FOREIGN KEY (competitor_username) REFERENCES competitors(username)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_competitor(self, username):
        """Add competitor to track"""
        try:
            # Verify account exists
            user_info = self.client.user_info_by_username(username)
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR IGNORE INTO competitors (username, added_date, last_checked)
                VALUES (?, ?, ?)
            ''', (username, datetime.now().isoformat(), datetime.now().isoformat()))
            
            conn.commit()
            conn.close()
            
            return True, f"✅ Tracking: {username}"
        except Exception as e:
            return False, f"❌ Error: {e}"
    
    def track_competitor(self, username):
        """Fetch latest posts from competitor"""
        try:
            user_info = self.client.user_info_by_username(username)
            medias = self.client.user_medias(user_info.pk, amount=20)
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            new_posts = 0
            
            for media in medias:
                # Extract hashtags
                hashtags = ' '.join([tag for tag in media.caption_text.split() if tag.startswith('#')]) if media.caption_text else ''
                
                cursor.execute('''
                    INSERT OR IGNORE INTO competitor_posts
                    (competitor_username, media_id, caption, likes, comments, views, posted_date, hashtags)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    username,
                    str(media.pk),
                    media.caption_text[:500] if media.caption_text else '',
                    media.like_count or 0,
                    media.comment_count or 0,
                    media.view_count or 0,
                    media.taken_at.isoformat(),
                    hashtags
                ))
                
                new_posts += 1
                time.sleep(1)
            
            # Update last checked
            cursor.execute('''
                UPDATE competitors SET last_checked = ? WHERE username = ?
            ''', (datetime.now().isoformat(), username))
            
            conn.commit()
            conn.close()
            
            return True, f"✅ Tracked {new_posts} posts from {username}"
            
        except Exception as e:
            return False, f"❌ Tracking error: {e}"
    
    def get_competitor_stats(self, username, days=30):
        """Get competitor performance stats"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
        
        cursor.execute('''
            SELECT 
                COUNT(*) as total_posts,
                AVG(likes) as avg_likes,
                AVG(comments) as avg_comments,
                AVG(views) as avg_views,
                MAX(likes) as best_likes,
                GROUP_CONCAT(hashtags, ' ') as all_hashtags
            FROM competitor_posts
            WHERE competitor_username = ? AND posted_date >= ?
        ''', (username, cutoff_date))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            # Parse top hashtags
            all_tags = result[5].split() if result[5] else []
            from collections import Counter
            top_hashtags = Counter(all_tags).most_common(10)
            
            return {
                'total_posts': result[0],
                'avg_likes': round(result[1] or 0, 1),
                'avg_comments': round(result[2] or 0, 1),
                'avg_views': round(result[3] or 0, 1),
                'best_likes': result[4] or 0,
                'top_hashtags': [tag[0] for tag in top_hashtags]
            }
        
        return None
    
    def compare_with_me(self, my_stats, competitor_username):
        """Compare your stats vs competitor"""
        comp_stats = self.get_competitor_stats(competitor_username)
        
        if not comp_stats:
            return None
        
        comparison = {
            'posts': {
                'mine': my_stats.get('total_posts', 0),
                'theirs': comp_stats['total_posts'],
                'diff': my_stats.get('total_posts', 0) - comp_stats['total_posts']
            },
            'engagement': {
                'mine': my_stats.get('avg_engagement', 0),
                'theirs': comp_stats['avg_likes'] + comp_stats['avg_comments'],
                'diff': my_stats.get('avg_engagement', 0) - (comp_stats['avg_likes'] + comp_stats['avg_comments'])
            }
        }
        
        return comparison
    
    def get_all_competitors(self):
        """List all tracked competitors"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT username, added_date, last_checked FROM competitors')
        results = cursor.fetchall()
        conn.close()
        
        return results

print("✅ Competitor Tracker Module loaded")
