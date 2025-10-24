import sqlite3
from datetime import datetime, timedelta
from collections import defaultdict
import json
from config import (
    ANALYTICS_DB_PATH,
    LOW_ENGAGEMENT_THRESHOLD,
    SHADOW_BAN_DETECTION_THRESHOLD,
    MIN_DATA_POINTS_FOR_PREDICTION
)

class AdvancedAnalytics:
    def __init__(self):
        self.db_path = ANALYTICS_DB_PATH
        self.init_advanced_tables()
    
    def init_advanced_tables(self):
        """Initialize advanced analytics tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Enhanced post analytics
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS post_analytics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                media_id TEXT UNIQUE,
                username TEXT,
                video_filename TEXT,
                caption_variant TEXT,
                upload_date TIMESTAMP,
                upload_hour INTEGER,
                upload_day_of_week INTEGER,
                likes INTEGER DEFAULT 0,
                comments INTEGER DEFAULT 0,
                views INTEGER DEFAULT 0,
                shares INTEGER DEFAULT 0,
                saves INTEGER DEFAULT 0,
                reach INTEGER DEFAULT 0,
                engagement_rate REAL DEFAULT 0,
                viral_score REAL DEFAULT 0,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Hashtag performance tracking
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS hashtag_performance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                hashtag TEXT,
                username TEXT,
                media_id TEXT,
                impressions INTEGER DEFAULT 0,
                engagement INTEGER DEFAULT 0,
                reach INTEGER DEFAULT 0,
                performance_score REAL DEFAULT 0,
                date_used TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (media_id) REFERENCES post_analytics(media_id)
            )
        ''')
        
        # Caption A/B testing
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS caption_variants (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                variant_id TEXT UNIQUE,
                caption_text TEXT,
                hashtags TEXT,
                times_used INTEGER DEFAULT 0,
                avg_engagement REAL DEFAULT 0,
                total_likes INTEGER DEFAULT 0,
                total_comments INTEGER DEFAULT 0,
                total_views INTEGER DEFAULT 0,
                performance_score REAL DEFAULT 0,
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Best time analytics
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS time_performance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                hour INTEGER,
                day_of_week INTEGER,
                avg_engagement REAL DEFAULT 0,
                avg_reach INTEGER DEFAULT 0,
                post_count INTEGER DEFAULT 0,
                success_rate REAL DEFAULT 0,
                UNIQUE(username, hour, day_of_week)
            )
        ''')
        
        # Shadow ban detection
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS shadow_ban_checks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                check_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                avg_reach_last_7days INTEGER,
                avg_reach_previous_7days INTEGER,
                reach_drop_percentage REAL,
                is_shadow_banned INTEGER DEFAULT 0,
                recovery_suggestions TEXT
            )
        ''')
        
        # Account growth tracking
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS account_growth (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                followers INTEGER,
                following INTEGER,
                total_posts INTEGER,
                avg_engagement_rate REAL,
                growth_rate REAL,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    # ==================== POST ANALYTICS ====================
    
    def save_post_analytics(self, media_id, username, video_filename, caption, 
                           likes, comments, views, shares=0, saves=0, reach=0):
        """Save comprehensive post analytics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        upload_time = datetime.now()
        upload_hour = upload_time.hour
        upload_day = upload_time.weekday()
        
        # Calculate metrics
        total_engagement = likes + comments + shares + saves
        engagement_rate = (total_engagement / max(views, 1)) * 100
        
        # Viral score calculation (proprietary algorithm)
        viral_score = self._calculate_viral_score(likes, comments, views, shares, saves, reach)
        
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO post_analytics 
                (media_id, username, video_filename, caption_variant, upload_date, 
                 upload_hour, upload_day_of_week, likes, comments, views, shares, 
                 saves, reach, engagement_rate, viral_score)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (media_id, username, video_filename, caption[:50], upload_time, 
                  upload_hour, upload_day, likes, comments, views, shares, 
                  saves, reach, engagement_rate, viral_score))
            
            conn.commit()
            return True
        except Exception as e:
            print(f"❌ Error saving analytics: {e}")
            return False
        finally:
            conn.close()
    
    def _calculate_viral_score(self, likes, comments, views, shares, saves, reach):
        """Calculate viral potential score (0-100)"""
        if views == 0:
            return 0
        
        # Weighted scoring system
        engagement_rate = ((likes + comments * 2 + shares * 3 + saves * 2) / views) * 100
        reach_rate = (reach / max(views, 1)) * 100
        
        viral_score = min(100, (engagement_rate * 0.7 + reach_rate * 0.3))
        return round(viral_score, 2)
    
    # ==================== HASHTAG PERFORMANCE ====================
    
    def track_hashtag_performance(self, hashtags, media_id, username, engagement, reach=0):
        """Track individual hashtag performance"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for hashtag in hashtags:
            hashtag = hashtag.strip('#').lower()
            
            # Performance score: engagement per impression
            performance_score = (engagement / max(reach, 1)) * 100
            
            cursor.execute('''
                INSERT INTO hashtag_performance 
                (hashtag, username, media_id, engagement, reach, performance_score)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (hashtag, username, media_id, engagement, reach, performance_score))
        
        conn.commit()
        conn.close()
    
    def get_best_performing_hashtags(self, username, limit=20):
        """Get top performing hashtags based on historical data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                hashtag,
                AVG(performance_score) as avg_score,
                COUNT(*) as usage_count,
                AVG(engagement) as avg_engagement
            FROM hashtag_performance
            WHERE username = ?
            GROUP BY hashtag
            HAVING usage_count >= 2
            ORDER BY avg_score DESC, avg_engagement DESC
            LIMIT ?
        ''', (username, limit))
        
        hashtags = cursor.fetchall()
        conn.close()
        
        return [{'hashtag': h[0], 'score': round(h[1], 2), 
                 'used': h[2], 'avg_engagement': h[3]} for h in hashtags]
    
    def get_underperforming_hashtags(self, username, limit=10):
        """Identify hashtags that should be replaced"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                hashtag,
                AVG(performance_score) as avg_score,
                COUNT(*) as usage_count
            FROM hashtag_performance
            WHERE username = ?
            GROUP BY hashtag
            HAVING usage_count >= 3
            ORDER BY avg_score ASC
            LIMIT ?
        ''', (username, limit))
        
        hashtags = cursor.fetchall()
        conn.close()
        
        return [h[0] for h in hashtags]
    
    # ==================== CAPTION A/B TESTING ====================
    
    def register_caption_variant(self, variant_id, caption_text, hashtags):
        """Register a new caption variant for testing"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT OR IGNORE INTO caption_variants 
                (variant_id, caption_text, hashtags)
                VALUES (?, ?, ?)
            ''', (variant_id, caption_text, hashtags))
            
            conn.commit()
            return True
        except Exception as e:
            print(f"Error registering caption: {e}")
            return False
        finally:
            conn.close()
    
    def update_caption_performance(self, variant_id, likes, comments, views):
        """Update caption variant performance metrics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        engagement_rate = ((likes + comments) / max(views, 1)) * 100
        
        cursor.execute('''
            UPDATE caption_variants
            SET times_used = times_used + 1,
                total_likes = total_likes + ?,
                total_comments = total_comments + ?,
                total_views = total_views + ?,
                avg_engagement = (total_likes + total_comments) / CAST(total_views AS REAL) * 100,
                performance_score = ?
            WHERE variant_id = ?
        ''', (likes, comments, views, engagement_rate, variant_id))
        
        conn.commit()
        conn.close()
    
    def get_best_caption_variants(self, limit=5):
        """Get top performing caption variants"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT caption_text, avg_engagement, times_used, performance_score
            FROM caption_variants
            WHERE times_used >= 2
            ORDER BY performance_score DESC, avg_engagement DESC
            LIMIT ?
        ''', (limit,))
        
        variants = cursor.fetchall()
        conn.close()
        
        return variants
    
    # ==================== BEST TIME PREDICTION ====================
    
    def update_time_performance(self, username, hour, day_of_week, engagement, reach):
        """Update posting time performance data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO time_performance (username, hour, day_of_week, avg_engagement, avg_reach, post_count)
            VALUES (?, ?, ?, ?, ?, 1)
            ON CONFLICT(username, hour, day_of_week) DO UPDATE SET
                avg_engagement = ((avg_engagement * post_count) + ?) / (post_count + 1),
                avg_reach = ((avg_reach * post_count) + ?) / (post_count + 1),
                post_count = post_count + 1
        ''', (username, hour, day_of_week, engagement, reach, engagement, reach))
        
        conn.commit()
        conn.close()
    
    def predict_best_posting_times(self, username, num_times=4):
        """AI-powered prediction of best posting times"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get data points
        cursor.execute('''
            SELECT COUNT(*) FROM time_performance WHERE username = ?
        ''', (username,))
        
        data_points = cursor.fetchone()[0]
        
        if data_points < MIN_DATA_POINTS_FOR_PREDICTION:
            conn.close()
            # Return default times if insufficient data
            return ["10:00", "14:00", "18:00", "21:00"]
        
        # Get best times based on engagement and reach
        cursor.execute('''
            SELECT 
                hour,
                AVG(avg_engagement) as overall_engagement,
                AVG(avg_reach) as overall_reach,
                SUM(post_count) as total_posts
            FROM time_performance
            WHERE username = ?
            GROUP BY hour
            HAVING total_posts >= 2
            ORDER BY overall_engagement DESC, overall_reach DESC
            LIMIT ?
        ''', (username, num_times))
        
        best_times = cursor.fetchall()
        conn.close()
        
        if not best_times:
            return ["10:00", "14:00", "18:00", "21:00"]
        
        # Format hours as HH:00
        return [f"{hour:02d}:00" for hour, _, _, _ in best_times]
    
    # ==================== SHADOW BAN DETECTION ====================
    
    def check_shadow_ban(self, username):
        """Advanced shadow ban detection algorithm"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get last 7 days reach
        cursor.execute('''
            SELECT AVG(reach) FROM post_analytics
            WHERE username = ? AND upload_date >= datetime('now', '-7 days')
        ''', (username,))
        
        avg_reach_last_7 = cursor.fetchone()[0] or 0
        
        # Get previous 7 days reach (8-14 days ago)
        cursor.execute('''
            SELECT AVG(reach) FROM post_analytics
            WHERE username = ? 
            AND upload_date >= datetime('now', '-14 days')
            AND upload_date < datetime('now', '-7 days')
        ''', (username,))
        
        avg_reach_previous_7 = cursor.fetchone()[0] or 0
        
        # Calculate drop percentage
        if avg_reach_previous_7 > 0:
            drop_percentage = ((avg_reach_previous_7 - avg_reach_last_7) / avg_reach_previous_7) * 100
        else:
            drop_percentage = 0
        
        # Shadow ban indicators
        is_shadow_banned = drop_percentage >= (SHADOW_BAN_DETECTION_THRESHOLD * 100)
        
        # Recovery suggestions
        suggestions = []
        if is_shadow_banned:
            suggestions.extend([
                "🚫 Possible shadow ban detected!",
                "📉 Reach dropped by {:.1f}%".format(drop_percentage),
                "💡 Recommendations:",
                "  • Stop all automation for 48 hours",
                "  • Remove spammy hashtags",
                "  • Post only high-quality content",
                "  • Engage manually with your community",
                "  • Check Instagram's Community Guidelines"
            ])
        else:
            suggestions.append("✅ No shadow ban detected. Keep up the good work!")
        
        suggestions_text = "\n".join(suggestions)
        
        # Save check results
        cursor.execute('''
            INSERT INTO shadow_ban_checks 
            (username, avg_reach_last_7days, avg_reach_previous_7days, 
             reach_drop_percentage, is_shadow_banned, recovery_suggestions)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (username, int(avg_reach_last_7), int(avg_reach_previous_7), 
              drop_percentage, int(is_shadow_banned), suggestions_text))
        
        conn.commit()
        conn.close()
        
        return {
            'is_shadow_banned': is_shadow_banned,
            'drop_percentage': round(drop_percentage, 2),
            'avg_reach_last_7': int(avg_reach_last_7),
            'avg_reach_previous_7': int(avg_reach_previous_7),
            'suggestions': suggestions_text
        }
    
    # ==================== ACCOUNT GROWTH ====================
    
    def save_account_growth(self, username, followers, following, total_posts):
        """Track account growth metrics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Calculate current avg engagement
        cursor.execute('''
            SELECT AVG(engagement_rate) FROM post_analytics
            WHERE username = ? AND upload_date >= datetime('now', '-7 days')
        ''', (username,))
        
        avg_engagement = cursor.fetchone()[0] or 0
        
        # Calculate growth rate
        cursor.execute('''
            SELECT followers FROM account_growth
            WHERE username = ?
            ORDER BY date DESC LIMIT 1
        ''', (username,))
        
        previous_followers = cursor.fetchone()
        growth_rate = 0
        
        if previous_followers:
            prev_count = previous_followers[0]
            if prev_count > 0:
                growth_rate = ((followers - prev_count) / prev_count) * 100
        
        cursor.execute('''
            INSERT INTO account_growth 
            (username, followers, following, total_posts, avg_engagement_rate, growth_rate)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (username, followers, following, total_posts, avg_engagement, growth_rate))
        
        conn.commit()
        conn.close()
    
    # ==================== DASHBOARD DATA ====================
    
    def get_dashboard_data(self, username, days=7):
        """Get comprehensive dashboard data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        date_limit = datetime.now() - timedelta(days=days)
        
        # Overall stats
        cursor.execute('''
            SELECT 
                COUNT(*) as total_posts,
                SUM(likes) as total_likes,
                SUM(comments) as total_comments,
                SUM(views) as total_views,
                AVG(engagement_rate) as avg_engagement,
                AVG(viral_score) as avg_viral_score
            FROM post_analytics
            WHERE username = ? AND upload_date >= ?
        ''', (username, date_limit))
        
        stats = cursor.fetchone()
        
        # Best performing post
        cursor.execute('''
            SELECT video_filename, engagement_rate, viral_score
            FROM post_analytics
            WHERE username = ? AND upload_date >= ?
            ORDER BY viral_score DESC
            LIMIT 1
        ''', (username, date_limit))
        
        best_post = cursor.fetchone()
        
        conn.close()
        
        return {
            'total_posts': stats[0] or 0,
            'total_likes': stats[1] or 0,
            'total_comments': stats[2] or 0,
            'total_views': stats[3] or 0,
            'avg_engagement': round(stats[4] or 0, 2),
            'avg_viral_score': round(stats[5] or 0, 2),
            'best_post': {
                'filename': best_post[0] if best_post else 'N/A',
                'engagement': round(best_post[1], 2) if best_post else 0,
                'viral_score': round(best_post[2], 2) if best_post else 0
            }
        }

# Initialize on import
print("✅ Advanced Analytics Engine loaded")
 