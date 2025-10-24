from instagrapi import Client
from instagrapi.exceptions import LoginRequired, ChallengeRequired, PleaseWaitFewMinutes
import time
import random
import os
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
            
            # Try session-based login first
            if os.path.exists(session_file):
                try:
                    self.client.load_settings(session_file)
                    self.client.login(username, password)
                    print(f"✅ Session login successful: {username}")
                    self.current_username = username
                    self.retry_count = 0
                    return True, "Session login successful!"
                except Exception as e:
                    print(f"Session expired, fresh login...")
            
            # Fresh login
            self.client.login(username, password)
            self.client.dump_settings(session_file)
            self.db.add_account(username, password, session_file)
            
            self.current_username = username
            self.retry_count = 0
            print(f"✅ Fresh login successful: {username}")
            return True, "Login successful!"
            
        except ChallengeRequired:
            return False, "⚠️ Instagram verification required! Login via browser first."
        except PleaseWaitFewMinutes:
            return False, "🚫 Temporary block! Wait 30-60 minutes."
        except Exception as e:
            return False, f"❌ Login error: {str(e)}"
    
    def upload_video(self, video_path, custom_caption=None):
        """
        Professional video upload with:
        - Retry mechanism
        - Analytics tracking
        - Story cross-posting
        - A/B testing
        - Hashtag optimization
        """
        
        if not self.client or not self.current_username:
            return False, "❌ Not logged in!"
        
        # Retry loop
        for attempt in range(1, MAX_RETRY_ATTEMPTS + 1):
            try:
                result = self._attempt_upload(video_path, custom_caption, attempt)
                if result[0]:  # Success
                    self.retry_count = 0
                    return result
                
                # If failed and retries remaining
                if attempt < MAX_RETRY_ATTEMPTS:
                    wait_time = ERROR_COOLDOWN_MINUTES * attempt
                    print(f"⏳ Retry {attempt}/{MAX_RETRY_ATTEMPTS} in {wait_time} minutes...")
                    time.sleep(wait_time * 60)
                
            except PleaseWaitFewMinutes:
                print(f"⚠️ Rate limited. Cooling down...")
                time.sleep(ERROR_COOLDOWN_MINUTES * 60)
            except Exception as e:
                print(f"❌ Attempt {attempt} failed: {e}")
                if attempt < MAX_RETRY_ATTEMPTS:
                    time.sleep(ERROR_COOLDOWN_MINUTES * 60)
        
        return False, f"❌ Upload failed after {MAX_RETRY_ATTEMPTS} attempts"
    
    def _attempt_upload(self, video_path, custom_caption, attempt_num):
        """Single upload attempt with full feature set"""
        
        # Pre-upload validations
        video_filename = os.path.basename(video_path)
        
        if self.db.is_video_uploaded(video_filename, self.current_username):
            return False, f"⚠️ Already uploaded: {video_filename}"
        
        today_posts = self.db.get_today_post_count(self.current_username)
        if today_posts >= MAX_POSTS_PER_DAY:
            return False, f"⚠️ Daily limit reached ({MAX_POSTS_PER_DAY} posts/day)"
        
        if not os.path.exists(video_path):
            return False, "❌ Video file not found!"
        
        file_ext = os.path.splitext(video_path)[1].lower()
        if file_ext not in SUPPORTED_VIDEO_FORMATS:
            return False, f"❌ Unsupported format: {file_ext}"
        
        # Generate optimized caption
        if custom_caption:
            caption = custom_caption
            variant_id = "custom_caption"
        else:
            caption, variant_id = self.caption_gen.generate_caption(video_filename)
        
        print(f"📤 Uploading: {video_filename} (Attempt {attempt_num})")
        print(f"📝 Caption preview: {caption[:80]}...")
        
        # Upload to Instagram
        media = self.client.video_upload(
            video_path,
            caption=caption,
            extra_data={
                "custom_accessibility_caption": "",
                "like_and_view_counts_disabled": False,
                "disable_comments": False,
            }
        )
        
        if not media:
            return False, "❌ Upload failed - No media returned"
        
        print(f"✅ Upload successful! Media ID: {media.pk}")
        
        # Save to database
        self.db.add_uploaded_video(
            video_filename, 
            self.current_username, 
            caption, 
            video_path
        )
        self.db.update_account_post_count(self.current_username)
        
        # FEATURE: Auto-post to Story
        if AUTO_POST_TO_STORY:
            self._post_to_story(video_path)
        
        # FEATURE: Analytics tracking
        if TRACK_ANALYTICS:
            self._track_post_analytics(media.pk, video_filename, caption, variant_id)
        
        return True, f"✅ Video uploaded successfully!\n{video_filename}"
    
    def _post_to_story(self, video_path):
        """Post video to Instagram Story"""
        try:
            print("📱 Cross-posting to story...")
            time.sleep(3)
            story = self.client.video_upload_to_story(video_path)
            if story:
                print("✅ Posted to story!")
        except Exception as e:
            print(f"⚠️ Story post failed: {e}")
    
    def _track_post_analytics(self, media_id, video_filename, caption, variant_id):
        """Fetch and save post analytics"""
        try:
            print("📊 Tracking analytics...")
            time.sleep(5)
            
            media_info = self.client.media_info(media_id)
            
            likes = media_info.like_count or 0
            comments = media_info.comment_count or 0
            views = media_info.view_count or 0
            
            # Save post analytics
            self.analytics.save_post_analytics(
                str(media_id),
                self.current_username,
                video_filename,
                caption,
                likes,
                comments,
                views
            )
            
            # Track hashtags
            hashtags = [tag.strip() for tag in caption.split() if tag.startswith('#')]
            if hashtags:
                total_engagement = likes + comments
                self.analytics.track_hashtag_performance(
                    hashtags,
                    str(media_id),
                    self.current_username,
                    total_engagement,
                    views
                )
            
            # Update time performance
            from datetime import datetime
            now = datetime.now()
            self.analytics.update_time_performance(
                self.current_username,
                now.hour,
                now.weekday(),
                (likes + comments) / max(views, 1) * 100,
                views
            )
            
            print(f"📊 Analytics tracked: {likes}❤️ {comments}💬 {views}👁️")
            
        except Exception as e:
            print(f"⚠️ Analytics error: {e}")
    
    def update_account_analytics(self):
        """Update account-level analytics"""
        try:
            user_info = self.client.user_info_by_username(self.current_username)
            
            self.analytics.save_account_growth(
                self.current_username,
                user_info.follower_count,
                user_info.following_count,
                user_info.media_count
            )
            
            print(f"📈 Account analytics: {user_info.follower_count} followers")
            return True
        except Exception as e:
            print(f"❌ Account analytics error: {e}")
            return False
    
    def get_performance_dashboard(self, days=7):
        """Get comprehensive performance data with safe error handling"""
        try:
            # Try to get dashboard data
            dashboard = self.analytics.get_dashboard_data(self.current_username, days)
            
            # If no data, return empty structure
            if not dashboard:
                dashboard = {
                    'total_posts': 0,
                    'total_likes': 0,
                    'total_comments': 0,
                    'total_views': 0,
                    'avg_engagement': 0,
                    'avg_viral_score': 0,
                    'best_post': {
                        'filename': 'No posts yet',
                        'engagement': 0,
                        'viral_score': 0
                    }
                }
            
            # Add shadow ban check (with error handling)
            try:
                shadow_ban = self.analytics.check_shadow_ban(self.current_username)
                dashboard['shadow_ban'] = shadow_ban
            except Exception as e:
                print(f"Shadow ban check error: {e}")
                dashboard['shadow_ban'] = {
                    'is_shadow_banned': False,
                    'drop_percentage': 0,
                    'avg_reach_last_7': 0,
                    'avg_reach_previous_7': 0,
                    'suggestions': 'Not enough data yet'
                }
            
            # Add best times (with error handling)
            try:
                best_times = self.analytics.predict_best_posting_times(self.current_username)
                dashboard['recommended_times'] = best_times
            except Exception as e:
                print(f"Best times prediction error: {e}")
                dashboard['recommended_times'] = ["10:00", "14:00", "18:00", "21:00"]
            
            # Add top hashtags (with error handling)
            try:
                top_hashtags = self.analytics.get_best_performing_hashtags(self.current_username, 10)
                dashboard['top_hashtags'] = top_hashtags if top_hashtags else []
            except Exception as e:
                print(f"Hashtags fetch error: {e}")
                dashboard['top_hashtags'] = []
            
            return dashboard
            
        except Exception as e:
            print(f"❌ Dashboard error: {e}")
            # Return safe empty structure instead of None
            return {
                'total_posts': 0,
                'total_likes': 0,
                'total_comments': 0,
                'total_views': 0,
                'avg_engagement': 0,
                'avg_viral_score': 0,
                'best_post': {
                    'filename': 'No posts yet',
                    'engagement': 0,
                    'viral_score': 0
                },
                'shadow_ban': {
                    'is_shadow_banned': False,
                    'drop_percentage': 0,
                    'avg_reach_last_7': 0,
                    'avg_reach_previous_7': 0,
                    'suggestions': 'Not enough data'
                },
                'recommended_times': ["10:00", "14:00", "18:00", "21:00"],
                'top_hashtags': []
            }
    
    def upload_folder_videos(self, folder_path, callback=None):
        """Batch upload with progress tracking"""
        
        if not os.path.isdir(folder_path):
            return False, "❌ Invalid folder path!"
        
        videos = []
        for file in os.listdir(folder_path):
            file_ext = os.path.splitext(file)[1].lower()
            if file_ext in SUPPORTED_VIDEO_FORMATS:
                full_path = os.path.join(folder_path, file)
                if not self.db.is_video_uploaded(file, self.current_username):
                    videos.append((file, full_path))
        
        if not videos:
            return False, "⚠️ No new videos found!"
        
        today_posts = self.db.get_today_post_count(self.current_username)
        remaining_slots = MAX_POSTS_PER_DAY - today_posts
        
        if remaining_slots <= 0:
            return False, f"⚠️ Daily limit reached! Try tomorrow."
        
        videos_to_upload = videos[:remaining_slots]
        
        results = {'success': 0, 'failed': 0, 'skipped': len(videos) - len(videos_to_upload)}
        
        for idx, (filename, filepath) in enumerate(videos_to_upload, 1):
            success, message = self.upload_video(filepath)
            
            if success:
                results['success'] += 1
            else:
                results['failed'] += 1
            
            if callback:
                callback(idx, len(videos_to_upload), filename, success, message)
            
            # Human-like delay
            if idx < len(videos_to_upload):
                delay = random.randint(DELAY_BETWEEN_POSTS[0], DELAY_BETWEEN_POSTS[1])
                print(f"⏳ Cooling down: {delay//60} minutes...")
                
                if callback:
                    callback(idx, len(videos_to_upload), f"⏳ Waiting {delay//60}min", None, None)
                
                time.sleep(delay)
        
        summary = f"""
📊 Upload Summary:
✅ Successful: {results['success']}
❌ Failed: {results['failed']}
⏭️ Skipped: {results['skipped']}
        """
        
        return True, summary
    
    def get_account_info(self):
        """Get current account information"""
        if not self.client or not self.current_username:
            return None
        
        try:
            user_info = self.client.user_info_by_username(self.current_username)
            return {
                'username': user_info.username,
                'full_name': user_info.full_name,
                'followers': user_info.follower_count,
                'following': user_info.following_count,
                'posts': user_info.media_count
            }
        except Exception as e:
            print(f"❌ Account info error: {e}")
            return None
    
    def logout(self):
        """Safe logout"""
        if self.client:
            self.client = None
            self.current_username = None
            print("👋 Logged out successfully")

print("✅ Professional Instagram Manager loaded")

