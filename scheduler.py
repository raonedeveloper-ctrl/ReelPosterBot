from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import os
import random
from instagram_manager import InstagramManager
from database_manager import DatabaseManager
from config import AUTO_POSTING_TIMES, VIDEO_FOLDER_PATH, SUPPORTED_VIDEO_FORMATS, AUTO_DELETE_AFTER_UPLOAD
import time

class AutoPoster:
    def __init__(self, username, password):
        self.scheduler = BackgroundScheduler()
        self.insta_manager = InstagramManager()
        self.db = DatabaseManager()
        self.username = username
        self.password = password
        self.is_running = False
        
    def start_scheduler(self):
        """Scheduler start karo"""
        
        # Pehle login karo
        success, message = self.insta_manager.login(self.username, self.password)
        if not success:
            print(f"❌ Login failed: {message}")
            return False, message
        
        print(f"✅ Logged in as: {self.username}")
        
        # Har scheduled time ke liye job add karo
        for post_time in AUTO_POSTING_TIMES:
            hour, minute = post_time.split(":")
            
            self.scheduler.add_job(
                self.auto_post_video,
                trigger=CronTrigger(hour=int(hour), minute=int(minute)),
                id=f"post_at_{post_time}",
                replace_existing=True
            )
            
            print(f"⏰ Scheduled: Daily posting at {post_time}")
        
        self.scheduler.start()
        self.is_running = True
        print("🚀 Auto-poster started! Videos will post automatically.")
        
        return True, "Scheduler started successfully!"
    
    def auto_post_video(self):
        """Automatic video upload karo"""
        print("\n⏰ Auto-posting triggered!")
        
        try:
            # Random video select karo
            video_path = self._get_random_unposted_video()
            
            if not video_path:
                print("⚠️ No new videos found in folder!")
                return
            
            video_filename = os.path.basename(video_path)
            print(f"📹 Selected video: {video_filename}")
            
            # Video upload karo
            success, message = self.insta_manager.upload_video(video_path)
            
            if success:
                print(f"✅ {message}")
                
                # Auto delete video if enabled
                if AUTO_DELETE_AFTER_UPLOAD:
                    try:
                        os.remove(video_path)
                        print(f"🗑️ Video deleted: {video_filename}")
                    except Exception as e:
                        print(f"⚠️ Could not delete video: {e}")
            else:
                print(f"❌ Upload failed: {message}")
                
        except Exception as e:
            print(f"❌ Auto-post error: {e}")
    
    def _get_random_unposted_video(self):
        """Random unposted video select karo"""
        
        if not os.path.isdir(VIDEO_FOLDER_PATH):
            return None
        
        # Saare videos get karo
        all_videos = []
        for file in os.listdir(VIDEO_FOLDER_PATH):
            file_ext = os.path.splitext(file)[1].lower()
            if file_ext in SUPPORTED_VIDEO_FORMATS:
                full_path = os.path.join(VIDEO_FOLDER_PATH, file)
                
                # Check ki already uploaded nahi hai
                if not self.db.is_video_uploaded(file, self.username):
                    all_videos.append(full_path)
        
        # Random video return karo
        if all_videos:
            return random.choice(all_videos)
        
        return None
    
    def stop_scheduler(self):
        """Scheduler stop karo"""
        if self.is_running:
            self.scheduler.shutdown()
            self.is_running = False
            print("⏹️ Auto-poster stopped!")
    
    def get_next_post_time(self):
        """Next post time dikhao"""
        jobs = self.scheduler.get_jobs()
        if jobs:
            next_job = min(jobs, key=lambda x: x.next_run_time)
            return next_job.next_run_time
        return None
