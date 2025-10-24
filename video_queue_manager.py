import json
import os
from datetime import datetime
from config import VIDEO_QUEUE_PATH, VIDEO_FOLDER_PATH, SUPPORTED_VIDEO_FORMATS

class VideoQueueManager:
    """Enterprise-level video queue management system"""
    
    def __init__(self):
        self.queue_file = VIDEO_QUEUE_PATH
        self.queue_data = self._load_queue()
    
    def _load_queue(self):
        """Load queue from persistent storage"""
        try:
            if os.path.exists(self.queue_file):
                with open(self.queue_file, 'r') as f:
                    return json.load(f)
            return {"queue": [], "history": [], "paused": False}
        except Exception as e:
            print(f"❌ Error loading queue: {e}")
            return {"queue": [], "history": [], "paused": False}
    
    def _save_queue(self):
        """Persist queue to disk"""
        try:
            with open(self.queue_file, 'w') as f:
                json.dump(self.queue_data, f, indent=2)
            return True
        except Exception as e:
            print(f"❌ Error saving queue: {e}")
            return False
    
    def add_video_to_queue(self, video_path, priority=5, scheduled_time=None, custom_caption=None):
        """
        Add video to queue with priority
        Priority: 1 (highest) to 10 (lowest), default: 5
        """
        if not os.path.exists(video_path):
            return False, "Video file not found!"
        
        video_item = {
            "id": self._generate_id(),
            "path": video_path,
            "filename": os.path.basename(video_path),
            "priority": priority,
            "scheduled_time": scheduled_time,
            "custom_caption": custom_caption,
            "added_date": datetime.now().isoformat(),
            "status": "queued"
        }
        
        self.queue_data["queue"].append(video_item)
        
        # Sort by priority (lower number = higher priority)
        self.queue_data["queue"].sort(key=lambda x: x["priority"])
        
        self._save_queue()
        return True, f"Video added to queue (Priority: {priority})"
    
    def get_next_video(self):
        """Get next video from queue (respects priority and schedule)"""
        if self.queue_data.get("paused", False):
            return None, "Queue is paused"
        
        if not self.queue_data["queue"]:
            return None, "Queue is empty"
        
        current_time = datetime.now()
        
        # Find first available video (considering schedule)
        for video in self.queue_data["queue"]:
            if video["status"] != "queued":
                continue
            
            # Check if scheduled
            if video.get("scheduled_time"):
                scheduled = datetime.fromisoformat(video["scheduled_time"])
                if current_time < scheduled:
                    continue  # Not yet time
            
            # This is our video
            return video, "Video retrieved from queue"
        
        return None, "No videos ready to post"
    
    def mark_video_completed(self, video_id, success=True):
        """Mark video as completed and move to history"""
        for i, video in enumerate(self.queue_data["queue"]):
            if video["id"] == video_id:
                video["status"] = "completed" if success else "failed"
                video["completed_date"] = datetime.now().isoformat()
                
                # Move to history
                self.queue_data["history"].append(video)
                self.queue_data["queue"].pop(i)
                
                self._save_queue()
                return True
        
        return False
    
    def remove_from_queue(self, video_id):
        """Remove specific video from queue"""
        for i, video in enumerate(self.queue_data["queue"]):
            if video["id"] == video_id:
                self.queue_data["queue"].pop(i)
                self._save_queue()
                return True, "Video removed from queue"
        
        return False, "Video not found in queue"
    
    def reorder_queue(self, video_id, new_priority):
        """Change video priority"""
        for video in self.queue_data["queue"]:
            if video["id"] == video_id:
                video["priority"] = new_priority
                
                # Re-sort queue
                self.queue_data["queue"].sort(key=lambda x: x["priority"])
                self._save_queue()
                return True, f"Priority updated to {new_priority}"
        
        return False, "Video not found"
    
    def pause_queue(self):
        """Pause queue processing"""
        self.queue_data["paused"] = True
        self._save_queue()
        return True, "Queue paused"
    
    def resume_queue(self):
        """Resume queue processing"""
        self.queue_data["paused"] = False
        self._save_queue()
        return True, "Queue resumed"
    
    def get_queue_status(self):
        """Get current queue statistics"""
        queued = [v for v in self.queue_data["queue"] if v["status"] == "queued"]
        
        return {
            "total_queued": len(queued),
            "total_history": len(self.queue_data["history"]),
            "is_paused": self.queue_data.get("paused", False),
            "next_video": queued[0]["filename"] if queued else None
        }
    
    def get_all_queued_videos(self):
        """Get list of all queued videos"""
        return [v for v in self.queue_data["queue"] if v["status"] == "queued"]
    
    def clear_queue(self):
        """Clear entire queue"""
        self.queue_data["queue"] = []
        self._save_queue()
        return True, "Queue cleared"
    
    def auto_populate_from_folder(self, folder_path=None):
        """Automatically add all videos from folder to queue"""
        if folder_path is None:
            folder_path = VIDEO_FOLDER_PATH
        
        if not os.path.isdir(folder_path):
            return False, "Invalid folder path"
        
        added_count = 0
        
        for file in os.listdir(folder_path):
            file_ext = os.path.splitext(file)[1].lower()
            if file_ext in SUPPORTED_VIDEO_FORMATS:
                full_path = os.path.join(folder_path, file)
                
                # Check if already in queue
                already_queued = any(v["path"] == full_path for v in self.queue_data["queue"])
                
                if not already_queued:
                    success, _ = self.add_video_to_queue(full_path)
                    if success:
                        added_count += 1
        
        return True, f"Added {added_count} videos to queue"
    
    def _generate_id(self):
        """Generate unique ID for video"""
        return f"vid_{int(datetime.now().timestamp())}_{len(self.queue_data['queue'])}"

print("✅ Video Queue Manager loaded")

