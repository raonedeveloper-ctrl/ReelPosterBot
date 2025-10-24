from instagrapi import Client
from instagrapi.exceptions import LoginRequired, ChallengeRequired, PleaseWaitFewMinutes
import time
import random
import os
from datetime import datetime, timedelta

from database_manager import DatabaseManager
from caption_generator import CaptionGenerator
from advanced_analytics import AdvancedAnalytics

from config import (
    SESSION_SAVE_PATH,
    DELAY_BETWEEN_POSTS,
    MAX_POSTS_PER_DAY,
    SUPPORTED_VIDEO_FORMATS,
    AUTO_POST_TO_STORY,
    TRACK_ANALYTICS,
    MAX_RETRY_ATTEMPTS,
    ERROR_COOLDOWN_MINUTES
)


class InstagramManager:
    """Enterprise-grade Instagram automation manager"""
    
    def __init__(self):
        self.client = None
        self.current_username = None
        self.db = DatabaseManager()
        self.analytics = AdvancedAnalytics()
        self.caption_gen = CaptionGenerator(analytics_manager=self.analytics)
        self.retry_count = 0
    
def login(self, username, password):
    """Secure login with session management"""
    try:
        self.client = Client()
        self.client.delay_range = [1, 3]
        
        session_file = os.path.join(SESSION_SAVE_PATH, f"{username}_session.json")
        
        # Try loading existing session
        if os.path.exists(session_file):
            try:
                self.client.load_settings(session_file)
                self.client.login(username, password)
                self.current_username = username
                print(f"✅ Logged in using saved session: {username}")
                return True, "Logged in successfully using saved session"
            except Exception as e:
                print(f"⚠️ Session expired, logging in fresh: {e}")
        
        # Fresh login
        self.client.login(username, password)
        self.current_username = username
        
        # Save session
        os.makedirs(SESSION_SAVE_PATH, exist_ok=True)
        self.client.dump_settings(session_file)
        
        print(f"✅ Successfully logged in: {username}")
        return True, f"Successfully logged in as {username}"
        
    except ChallengeRequired as e:
        error_msg = f"Challenge required (2FA/Verification): {e}"
        print(f"⚠️ {error_msg}")
        return False, error_msg
    except LoginRequired as e:
        error_msg = f"Login failed: {e}"
        print(f"❌ {error_msg}")
        return False, error_msg
    except PleaseWaitFewMinutes as e:
        error_msg = f"Rate limited. Please wait: {e}"
        print(f"⏳ {error_msg}")
        return False, error_msg
    except Exception as e:
        error_msg = f"Unexpected login error: {e}"
        print(f"❌ {error_msg}")
        return False, error_msg
    
    def logout(self):
        """Safely logout and cleanup"""
        if self.client:
            try:
                self.client.logout()
                self.current_username = None
                print("✅ Logged out successfully")
                return True
            except Exception as e:
                print(f"⚠️ Logout warning: {e}")
                return False
        return True
    
    def upload_video(self, video_path, caption="", hashtags=None, attempt=1):
        """
        Upload video to Instagram Reels with advanced error handling
        """
        if not self.client or not self.current_username:
            print("❌ Not logged in. Please login first.")
            return False
        
        # Validate video file
        if not os.path.exists(video_path):
            print(f"❌ Video file not found: {video_path}")
            return False
        
        video_ext = os.path.splitext(video_path)[1].lower()
        if video_ext not in SUPPORTED_VIDEO_FORMATS:
            print(f"❌ Unsupported format: {video_ext}")
            return False
        
        # Check daily post limit
        if not self._check_daily_limit():
            print(f"⚠️ Daily post limit reached ({MAX_POSTS_PER_DAY})")
            return False
        
        # Check for duplicates
        video_filename = os.path.basename(video_path)
        if self.db.is_video_uploaded(video_filename, self.current_username):
            print(f"⚠️ Video already uploaded: {video_filename}")
            return False
        
        # Generate caption if not provided
        if not caption:
            caption = self.caption_gen.generate_caption(video_filename)
        
        # Add hashtags if provided
        if hashtags:
            caption = f"{caption}\n\n{' '.join(hashtags)}"
        
        print(f"📤 Uploading video (Attempt {attempt}/{MAX_RETRY_ATTEMPTS}): {video_filename}")
        print(f"📝 Caption: {caption[:100]}...")
        
        try:
            # Upload to Instagram
            media = self.client.clip_upload(
                video_path,
                caption=caption
            )
            
            media_id = str(media.pk)
            print(f"✅ Upload successful! Media ID: {media_id}")
            
            # Save to database
            self.db.add_uploaded_video(
                video_filename=video_filename,
                account_username=self.current_username,
                caption_used=caption,
                video_path=video_path,
                status='success'
            )
            
            # Track analytics if enabled
            if TRACK_ANALYTICS:
                self.analytics.save_post_analytics(
                    media_id=media_id,
                    username=self.current_username,
                    video_filename=video_filename,
                    caption=caption,
                    likes=0,
                    comments=0,
                    views=0
                )
            
            # Auto-post to story if enabled
            if AUTO_POST_TO_STORY:
                try:
                    print("📸 Posting to story...")
                    self.client.video_upload_to_story(video_path)
                    print("✅ Posted to story!")
                except Exception as e:
                    print(f"⚠️ Story upload failed: {e}")
            
            # Human-like delay
            delay = random.randint(*DELAY_BETWEEN_POSTS)
            print(f"⏳ Waiting {delay} seconds before next action...")
            time.sleep(delay)
            
            self.retry_count = 0  # Reset retry counter
            return True
            
        except Exception as e:
            print(f"❌ Upload failed: {e}")
            
            # Retry logic
            if attempt < MAX_RETRY_ATTEMPTS:
                cooldown = ERROR_COOLDOWN_MINUTES * 60
                print(f"⏳ Retrying in {ERROR_COOLDOWN_MINUTES} minutes...")
                time.sleep(cooldown)
                return self.upload_video(video_path, caption, hashtags, attempt + 1)
            else:
                print(f"❌ Max retries reached. Upload failed permanently.")
                
                # Log failed upload
                self.db.add_uploaded_video(
                    video_filename=video_filename,
                    account_username=self.current_username,
                    caption_used=caption,
                    video_path=video_path,
                    status='failed'
                )
                return False
    
    def _check_daily_limit(self):
        """Check if daily post limit has been reached"""
        posts_today = self.db.get_posts_today(self.current_username)
        return posts_today < MAX_POSTS_PER_DAY
    
    def get_account_info(self):
        """Get basic account information"""
        if not self.client or not self.current_username:
            return None
        
        try:
            user_info = self.client.user_info_by_username(self.current_username)
            return {
                'username': user_info.username,
                'full_name': user_info.full_name,
                'followers': user_info.follower_count,
                'following': user_info.following_count,
                'media_count': user_info.media_count,
                'biography': user_info.biography
            }
        except Exception as e:
            print(f"❌ Error fetching account info: {e}")
            return None
    
    # ==================== REAL-TIME STATS (NEW) ====================
    
    def get_realtime_account_stats(self):
        """
        Fetch real-time account statistics from Instagram API
        Returns comprehensive account metrics
        """
        if not self.client or not self.current_username:
            return None
        
        try:
            print("📊 Fetching real-time account stats...")
            
            # Get user info
            user_info = self.client.user_info_by_username(self.current_username)
            
            # Get user's media (recent posts)
            user_id = user_info.pk
            medias = self.client.user_medias(user_id, amount=50)  # Last 50 posts
            
            # Calculate metrics
            total_likes = sum(media.like_count or 0 for media in medias)
            total_comments = sum(media.comment_count or 0 for media in medias)
            total_views = sum(media.view_count or 0 for media in medias if hasattr(media, 'view_count'))
            
            media_count = len(medias)
            avg_likes = total_likes / media_count if media_count > 0 else 0
            avg_comments = total_comments / media_count if media_count > 0 else 0
            avg_views = total_views / media_count if media_count > 0 else 0
            
            # Calculate engagement rate
            total_engagement = total_likes + total_comments
            engagement_rate = (total_engagement / (user_info.follower_count * media_count)) * 100 if user_info.follower_count > 0 and media_count > 0 else 0
            
            stats = {
                'username': user_info.username,
                'full_name': user_info.full_name,
                'followers': user_info.follower_count,
                'following': user_info.following_count,
                'media_count': user_info.media_count,
                'biography': user_info.biography,
                'total_likes': total_likes,
                'total_comments': total_comments,
                'total_views': total_views,
                'avg_likes': round(avg_likes, 2),
                'avg_comments': round(avg_comments, 2),
                'avg_views': round(avg_views, 2),
                'engagement_rate': round(engagement_rate, 2),
                'recent_posts_count': media_count,
                'fetched_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            print(f"✅ Stats fetched: {stats['followers']} followers, {stats['engagement_rate']}% engagement")
            return stats
            
        except Exception as e:
            print(f"❌ Error fetching real-time stats: {e}")
            return None
    
    def get_user_posts_in_range(self, days=7):
        """
        Fetch user's posts within specified time range
        Returns list of posts with engagement metrics
        """
        if not self.client or not self.current_username:
            return []
        
        try:
            print(f"📥 Fetching posts from last {days} days...")
            
            user_info = self.client.user_info_by_username(self.current_username)
            user_id = user_info.pk
            
            # Fetch posts (increased amount to ensure we get posts within range)
            medias = self.client.user_medias(user_id, amount=100)
            
            # Filter by date range
            cutoff_date = datetime.now() - timedelta(days=days)
            filtered_posts = []
            
            for media in medias:
                if media.taken_at.replace(tzinfo=None) >= cutoff_date:
                    post_data = {
                        'media_id': str(media.pk),
                        'caption': media.caption_text[:100] if media.caption_text else "No caption",
                        'likes': media.like_count or 0,
                        'comments': media.comment_count or 0,
                        'views': media.view_count or 0 if hasattr(media, 'view_count') else 0,
                        'taken_at': media.taken_at.strftime("%Y-%m-%d %H:%M:%S"),
                        'media_type': str(media.media_type),
                        'thumbnail_url': media.thumbnail_url if hasattr(media, 'thumbnail_url') else None
                    }
                    
                    # Calculate engagement for this post
                    post_engagement = post_data['likes'] + post_data['comments']
                    post_data['engagement'] = post_engagement
                    post_data['engagement_rate'] = round((post_engagement / user_info.follower_count * 100), 2) if user_info.follower_count > 0 else 0
                    
                    filtered_posts.append(post_data)
            
            # Sort by engagement (highest first)
            filtered_posts.sort(key=lambda x: x['engagement'], reverse=True)
            
            print(f"✅ Found {len(filtered_posts)} posts in last {days} days")
            return filtered_posts
            
        except Exception as e:
            print(f"❌ Error fetching posts: {e}")
            return []
    
    def get_top_performing_posts(self, days=7, limit=10):
        """
        Get top N performing posts within time range
        """
        posts = self.get_user_posts_in_range(days)
        return posts[:limit] if posts else []
    
    def refresh_account_insights(self, days=7):
        """
        Comprehensive account insights refresh
        Combines real-time stats + recent posts analysis
        """
        if not self.client or not self.current_username:
            return None
        
        try:
            print("🔄 Refreshing complete account insights...")
            
            # Get real-time account stats
            account_stats = self.get_realtime_account_stats()
            if not account_stats:
                return None
            
            # Get posts in time range
            posts = self.get_user_posts_in_range(days)
            
            # Calculate period-specific metrics
            period_likes = sum(p['likes'] for p in posts)
            period_comments = sum(p['comments'] for p in posts)
            period_views = sum(p['views'] for p in posts)
            period_posts = len(posts)
            
            insights = {
                'account': account_stats,
                'period_stats': {
                    'days': days,
                    'total_posts': period_posts,
                    'total_likes': period_likes,
                    'total_comments': period_comments,
                    'total_views': period_views,
                    'avg_likes_per_post': round(period_likes / period_posts, 2) if period_posts > 0 else 0,
                    'avg_comments_per_post': round(period_comments / period_posts, 2) if period_posts > 0 else 0,
                    'avg_views_per_post': round(period_views / period_posts, 2) if period_posts > 0 else 0,
                    'engagement_rate': round(((period_likes + period_comments) / (account_stats['followers'] * period_posts) * 100), 2) if account_stats['followers'] > 0 and period_posts > 0 else 0
                },
                'top_posts': posts[:10],
                'last_updated': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # Save to analytics database
            self.analytics.save_realtime_snapshot(
                self.current_username,
                account_stats['followers'],
                account_stats['following'],
                account_stats['media_count'],
                account_stats['engagement_rate']
            )
            
            print("✅ Insights refreshed successfully!")
            return insights
            
        except Exception as e:
            print(f"❌ Error refreshing insights: {e}")
            return None
    
    def post_to_story(self, video_path):
        """Upload video to Instagram Story"""
        if not self.client or not self.current_username:
            print("❌ Not logged in")
            return False
        
        try:
            print("📸 Posting to story...")
            self.client.video_upload_to_story(video_path)
            print("✅ Story posted successfully!")
            return True
        except Exception as e:
            print(f"❌ Story upload failed: {e}")
            return False
    
    def get_upload_history(self, limit=10):
        """Get recent upload history"""
        return self.db.get_upload_history(self.current_username, limit)
    
    def delete_post(self, media_id):
        """Delete a post from Instagram"""
        if not self.client:
            return False
        
        try:
            self.client.media_delete(media_id)
            print(f"✅ Post deleted: {media_id}")
            return True
        except Exception as e:
            print(f"❌ Delete failed: {e}")
            return False


# Initialize on import
print("✅ Instagram Manager initialized")
