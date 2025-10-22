from instagrapi import Client
from instagrapi.exceptions import LoginRequired, ChallengeRequired, PleaseWaitFewMinutes
import time
import random
import os
from database_manager import DatabaseManager
from caption_generator import CaptionGenerator
from config import (
    SESSION_SAVE_PATH, 
    DELAY_BETWEEN_POSTS, 
    MAX_POSTS_PER_DAY,
    SUPPORTED_VIDEO_FORMATS
)

class InstagramManager:
    def __init__(self):
        self.client = None
        self.current_username = None
        self.db = DatabaseManager()
        self.caption_gen = CaptionGenerator()
    
    def login(self, username, password):
        """Instagram me login karo with session management"""
        try:
            self.client = Client()
            
            # Device settings set karo (ban avoid karne ke liye)
            self.client.delay_range = [1, 3]
            
            session_file = os.path.join(SESSION_SAVE_PATH, f"{username}_session.json")
            
            # Pehle saved session se login try karo
            if os.path.exists(session_file):
                try:
                    self.client.load_settings(session_file)
                    self.client.login(username, password)
                    print(f"✅ Session se login successful: {username}")
                    self.current_username = username
                    return True, "Session se login ho gaya!"
                except Exception as e:
                    print(f"Session login failed, fresh login kar rahe hai...")
            
            # Fresh login
            self.client.login(username, password)
            
            # Session save karo future ke liye
            self.client.dump_settings(session_file)
            
            # Database me account save karo
            self.db.add_account(username, password, session_file)
            
            self.current_username = username
            print(f"✅ Fresh login successful: {username}")
            return True, "Login successful!"
            
        except ChallengeRequired:
            return False, "Instagram verification chahiye! Browser se manually login karo."
        except PleaseWaitFewMinutes:
            return False, "Instagram ne temporary block kiya! 30-60 min wait karo."
        except Exception as e:
            return False, f"Login error: {str(e)}"
    
    def upload_video(self, video_path, custom_caption=None):
        """Video upload karo with safety checks"""
        
        if not self.client or not self.current_username:
            return False, "Pehle login karo!"
        
        try:
            # Safety Check 1: Video already uploaded?
            video_filename = os.path.basename(video_path)
            if self.db.is_video_uploaded(video_filename, self.current_username):
                return False, f"⚠️ Video already uploaded: {video_filename}"
            
            # Safety Check 2: Daily limit check
            today_posts = self.db.get_today_post_count(self.current_username)
            if today_posts >= MAX_POSTS_PER_DAY:
                return False, f"⚠️ Daily limit reached! Max {MAX_POSTS_PER_DAY} posts/day allowed."
            
            # Safety Check 3: File validation
            if not os.path.exists(video_path):
                return False, "Video file nahi mili!"
            
            file_ext = os.path.splitext(video_path)[1].lower()
            if file_ext not in SUPPORTED_VIDEO_FORMATS:
                return False, f"Unsupported format: {file_ext}"
            
            # Caption generate karo
            if custom_caption:
                caption = custom_caption
            else:
                caption = self.caption_gen.generate_caption(video_filename)
            
            print(f"📤 Uploading: {video_filename}")
            print(f"📝 Caption: {caption[:50]}...")
            
            # Video upload karo
            media = self.client.video_upload(
                video_path,
                caption=caption,
                extra_data={
                    "custom_accessibility_caption": "",
                    "like_and_view_counts_disabled": False,
                    "disable_comments": False,
                }
            )
            
            if media:
                # Database me save karo
                self.db.add_uploaded_video(
                    video_filename, 
                    self.current_username, 
                    caption, 
                    video_path
                )
                self.db.update_account_post_count(self.current_username)
                
                print(f"✅ Upload successful! Media ID: {media.pk}")
                return True, f"✅ Video uploaded successfully!\n{video_filename}"
            else:
                return False, "Upload failed - Unknown error"
                
        except PleaseWaitFewMinutes:
            return False, "⚠️ Rate limit! Instagram ne block kiya. 1-2 ghante wait karo."
        except Exception as e:
            return False, f"❌ Error: {str(e)}"
    
    def upload_folder_videos(self, folder_path, callback=None):
        """Folder ke saare videos upload karo with delays"""
        
        if not os.path.isdir(folder_path):
            return False, "Invalid folder path!"
        
        # Supported videos find karo
        videos = []
        for file in os.listdir(folder_path):
            file_ext = os.path.splitext(file)[1].lower()
            if file_ext in SUPPORTED_VIDEO_FORMATS:
                full_path = os.path.join(folder_path, file)
                
                # Skip already uploaded
                if not self.db.is_video_uploaded(file, self.current_username):
                    videos.append((file, full_path))
        
        if not videos:
            return False, "Folder me naye videos nahi hai!"
        
        # Daily limit check
        today_posts = self.db.get_today_post_count(self.current_username)
        remaining_slots = MAX_POSTS_PER_DAY - today_posts
        
        if remaining_slots <= 0:
            return False, f"⚠️ Aaj ke liye limit complete! Kal try karo."
        
        videos_to_upload = videos[:remaining_slots]
        
        results = {
            'success': 0,
            'failed': 0,
            'skipped': len(videos) - len(videos_to_upload)
        }
        
        for idx, (filename, filepath) in enumerate(videos_to_upload, 1):
            # Upload karo
            success, message = self.upload_video(filepath)
            
            if success:
                results['success'] += 1
            else:
                results['failed'] += 1
            
            # Callback for progress update (GUI ke liye)
            if callback:
                callback(idx, len(videos_to_upload), filename, success, message)
            
            # Safety delay - Human-like behavior
            if idx < len(videos_to_upload):
                delay = random.randint(DELAY_BETWEEN_POSTS[0], DELAY_BETWEEN_POSTS[1])
                print(f"⏳ Safety delay: {delay//60} minutes...")
                
                if callback:
                    callback(idx, len(videos_to_upload), f"Waiting {delay//60} min...", None, None)
                
                time.sleep(delay)
        
        summary = f"""
        📊 Upload Summary:
        ✅ Successful: {results['success']}
        ❌ Failed: {results['failed']}
        ⏭️ Skipped (limit): {results['skipped']}
        """
        
        return True, summary
    
    def get_account_info(self):
        """Current account ki info"""
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
            print(f"Error getting account info: {e}")
            return None
    
    def logout(self):
        """Safely logout"""
        if self.client:
            self.client = None
            self.current_username = None
            print("👋 Logged out successfully")
