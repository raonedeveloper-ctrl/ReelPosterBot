from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import os
import random
from instagram_manager import InstagramManager
from database_manager import DatabaseManager
from video_queue_manager import VideoQueueManager
from advanced_analytics import AdvancedAnalytics
from config import (
    VIDEO_FOLDER_PATH, 
    SUPPORTED_VIDEO_FORMATS, 
    AUTO_DELETE_AFTER_UPLOAD,
    ENABLE_SMART_SCHEDULING,
    INITIAL_POSTING_TIMES,
    ENABLE_QUEUE_SYSTEM
)
import time

class AutoPoster:
    """Intelligent auto-posting scheduler with AI optimization"""
    
    def __init__(self, username, password):
        self.scheduler = BackgroundScheduler()
        self.insta_manager = InstagramManager()
        self.db = DatabaseManager()
        self.analytics = AdvancedAnalytics()
        self.queue_manager = VideoQueueManager()
        self.username = username
        self.password = password
        self.is_running = False
        self.posting_times = INITIAL_POSTING_TIMES.copy()
    
    def start_scheduler(self):
        """Start intelligent scheduler with AI-optimized times"""
        
        # Login
        success, message = self.insta_manager.login(self.username, self.password)
        if not success:
            print(f"❌ Login failed: {message}")
            return False, message
        
        print(f"✅ Logged in as: {self.username}")
        
        # Get AI-predicted best times if enabled
        if ENABLE_SMART_SCHEDULING:
            try:
                predicted_times = self.analytics.predict_best_posting_times(
                    self.username, 
                    num_times=4
                )
                if predicted_times:
                    self.posting_times = predicted_times
                    print(f"🤖 AI-optimized posting times: {', '.join(self.posting_times)}")
                else:
                    print(f"📅 Using default schedule: {', '.join(self.posting_times)}")
            except Exception as e:
                print(f"⚠️ AI prediction failed, using default times: {e}")
        
        # Auto-populate queue if enabled
        if ENABLE_QUEUE_SYSTEM:
            self.queue_manager.auto_populate_from_folder()
            queue_status = self.queue_manager.get_queue_status()
            print(f"📦 Queue loaded: {queue_status['total_queued']} videos")
        
        # Schedule jobs for each posting time
        for post_time in self.posting_times:
            hour, minute = post_time.split(":")
            
            self.scheduler.add_job(
                self.auto_post_video,
                trigger=CronTrigger(hour=int(hour), minute=int(minute)),
                id=f"post_at_{post_time}",
                replace_existing=True
            )
            
            print(f"⏰ Scheduled: Daily posting at {post_time}")
        
        # Schedule periodic analytics update (every 6 hours)
        self.scheduler.add_job(
            self._update_analytics,
            trigger=CronTrigger(hour="*/6"),
            id="analytics_update",
            replace_existing=True
        )
        
        # Schedule shadow ban check (daily at 9 AM)
        self.scheduler.add_job(
            self._check_shadow_ban,
            trigger=CronTrigger(hour=9, minute=0),
            id="shadow_ban_check",
            replace_existing=True
        )
        
        self.scheduler.start()
        self.is_running = True
        print("🚀 Intelligent auto-poster activated!")
        
        return True, "Scheduler started successfully!"
    
    def auto_post_video(self):
        """Intelligent video posting with queue management"""
        print("\n⏰ Auto-posting triggered!")
        
        try:
            # Get video from queue or random selection
            if ENABLE_QUEUE_SYSTEM:
                video_data, msg = self.queue_manager.get_next_video()
                if not video_data:
                    print(f"⚠️ {msg}")
                    return
                
                video_path = video_data["path"]
                video_id = video_data["id"]
                custom_caption = video_data.get("custom_caption")
            else:
                video_path = self._get_random_unposted_video()
                video_id = None
                custom_caption = None
            
            if not video_path:
                print("⚠️ No videos available to post!")
                return
            
            video_filename = os.path.basename(video_path)
            print(f"📹 Selected video: {video_filename}")
            
            # Upload video
            success, message = self.insta_manager.upload_video(
                video_path, 
                custom_caption=custom_caption
            )
            
            if success:
                print(f"✅ {message}")
                
                # Mark as completed in queue
                if ENABLE_QUEUE_SYSTEM and video_id:
                    self.queue_manager.mark_video_completed(video_id, success=True)
                
                # Auto-delete if enabled
                if AUTO_DELETE_AFTER_UPLOAD:
                    try:
                        os.remove(video_path)
                        print(f"🗑️ Video deleted: {video_filename}")
                    except Exception as e:
                        print(f"⚠️ Could not delete video: {e}")
            else:
                print(f"❌ Upload failed: {message}")
                
                # Mark as failed in queue
                if ENABLE_QUEUE_SYSTEM and video_id:
                    self.queue_manager.mark_video_completed(video_id, success=False)
                
        except Exception as e:
            print(f"❌ Auto-post error: {e}")
    
    def _get_random_unposted_video(self):
        """Get random unposted video (fallback if queue disabled)"""
        if not os.path.isdir(VIDEO_FOLDER_PATH):
            return None
        
        all_videos = []
        for file in os.listdir(VIDEO_FOLDER_PATH):
            file_ext = os.path.splitext(file)[1].lower()
            if file_ext in SUPPORTED_VIDEO_FORMATS:
                full_path = os.path.join(VIDEO_FOLDER_PATH, file)
                
                if not self.db.is_video_uploaded(file, self.username):
                    all_videos.append(full_path)
        
        if all_videos:
            return random.choice(all_videos)
        
        return None
    
    def _update_analytics(self):
        """Periodic analytics update"""
        try:
            print("📊 Updating analytics...")
            self.insta_manager.update_account_analytics()
            
            # Re-optimize posting times if enough data
            if ENABLE_SMART_SCHEDULING:
                new_times = self.analytics.predict_best_posting_times(self.username)
                if new_times != self.posting_times:
                    print(f"🔄 Optimizing schedule: {' → '.join(new_times)}")
                    self.posting_times = new_times
                    # Reschedule jobs (implementation in production version)
        except Exception as e:
            print(f"⚠️ Analytics update error: {e}")
    
    def _check_shadow_ban(self):
        """Daily shadow ban check"""
        try:
            print("🔍 Running shadow ban check...")
            result = self.analytics.check_shadow_ban(self.username)
            
            if result['is_shadow_banned']:
                print(f"🚫 ALERT: Possible shadow ban detected!")
                print(result['suggestions'])
            else:
                print("✅ No shadow ban detected")
        except Exception as e:
            print(f"⚠️ Shadow ban check error: {e}")
    
    def stop_scheduler(self):
        """Stop scheduler"""
        if self.is_running:
            self.scheduler.shutdown()
            self.is_running = False
            print("⏹️ Auto-poster stopped!")
    
    def get_next_post_time(self):
        """Get next scheduled post time"""
        jobs = self.scheduler.get_jobs()
        if jobs:
            next_job = min(jobs, key=lambda x: x.next_run_time)
            return next_job.next_run_time
        return None

print("✅ Intelligent Scheduler loaded")
