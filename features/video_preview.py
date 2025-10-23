import cv2
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os

class VideoPreview:
    """Video preview with thumbnail and metadata"""
    
    def __init__(self):
        self.preview_window = None
        self.video_info = {}
    
    def show_preview(self, video_path, callback=None):
        """Show video preview window"""
        if not os.path.exists(video_path):
            return False
        
        # Extract video info
        self._extract_video_info(video_path)
        
        # Create preview window
        self.preview_window = tk.Toplevel()
        self.preview_window.title("Video Preview")
        self.preview_window.geometry("600x700")
        
        # Video thumbnail
        thumb_frame = tk.Frame(self.preview_window)
        thumb_frame.pack(pady=10)
        
        thumbnail = self._get_thumbnail(video_path)
        if thumbnail:
            photo = ImageTk.PhotoImage(thumbnail)
            label = tk.Label(thumb_frame, image=photo)
            label.image = photo  # Keep reference
            label.pack()
        
        # Video info
        info_frame = tk.LabelFrame(
            self.preview_window,
            text="📊 Video Information",
            font=("Arial", 12, "bold"),
            padx=20,
            pady=10
        )
        info_frame.pack(fill=tk.X, padx=10, pady=10)
        
        info_items = [
            ("📁 Filename", os.path.basename(video_path)),
            ("⏱️ Duration", self.video_info.get('duration', 'N/A')),
            ("📐 Resolution", self.video_info.get('resolution', 'N/A')),
            ("💾 File Size", self.video_info.get('size', 'N/A')),
            ("🎞️ FPS", self.video_info.get('fps', 'N/A')),
            ("📊 Quality Score", self._calculate_quality_score())
        ]
        
        for label_text, value in info_items:
            row = tk.Frame(info_frame)
            row.pack(fill=tk.X, pady=3)
            
            tk.Label(
                row,
                text=label_text,
                font=("Arial", 10, "bold"),
                width=20,
                anchor="w"
            ).pack(side=tk.LEFT)
            
            tk.Label(
                row,
                text=value,
                font=("Arial", 10)
            ).pack(side=tk.LEFT)
        
        # Action buttons
        btn_frame = tk.Frame(self.preview_window)
        btn_frame.pack(pady=20)
        
        tk.Button(
            btn_frame,
            text="✅ Upload This Video",
            font=("Arial", 11, "bold"),
            bg="#4CAF50",
            fg="white",
            width=20,
            height=2,
            command=lambda: self._confirm_upload(video_path, callback)
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            btn_frame,
            text="❌ Cancel",
            font=("Arial", 11, "bold"),
            bg="#f44336",
            fg="white",
            width=20,
            height=2,
            command=self.preview_window.destroy
        ).pack(side=tk.LEFT, padx=5)
        
        return True
    
    def _extract_video_info(self, video_path):
        """Extract video metadata"""
        try:
            cap = cv2.VideoCapture(video_path)
            
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            duration = frame_count / fps if fps > 0 else 0
            
            file_size = os.path.getsize(video_path) / (1024 * 1024)  # MB
            
            self.video_info = {
                'duration': f"{int(duration)}s",
                'resolution': f"{width}x{height}",
                'size': f"{file_size:.2f} MB",
                'fps': f"{int(fps)} fps",
                'width': width,
                'height': height,
                'frame_count': frame_count
            }
            
            cap.release()
        except Exception as e:
            print(f"Error extracting video info: {e}")
    
    def _get_thumbnail(self, video_path):
        """Extract first frame as thumbnail"""
        try:
            cap = cv2.VideoCapture(video_path)
            ret, frame = cap.read()
            cap.release()
            
            if ret:
                # Convert BGR to RGB
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # Resize to fit preview
                frame = cv2.resize(frame, (500, 400))
                # Convert to PIL Image
                return Image.fromarray(frame)
            
        except Exception as e:
            print(f"Error getting thumbnail: {e}")
        
        return None
    
    def _calculate_quality_score(self):
        """Calculate video quality score"""
        score = 0
        
        # Resolution score
        width = self.video_info.get('width', 0)
        height = self.video_info.get('height', 0)
        
        if width >= 1080 and height >= 1920:  # Full HD vertical
            score += 40
        elif width >= 720 and height >= 1280:  # HD vertical
            score += 30
        else:
            score += 20
        
        # FPS score
        fps_str = self.video_info.get('fps', '0 fps')
        fps = int(fps_str.split()[0]) if fps_str != 'N/A' else 0
        
        if fps >= 60:
            score += 30
        elif fps >= 30:
            score += 25
        else:
            score += 15
        
        # Duration score (15-60s ideal for reels)
        duration_str = self.video_info.get('duration', '0s')
        duration = int(duration_str.replace('s', '')) if duration_str != 'N/A' else 0
        
        if 15 <= duration <= 60:
            score += 30
        elif 10 <= duration <= 90:
            score += 20
        else:
            score += 10
        
        return f"{score}/100 {'🟢' if score >= 70 else '🟡' if score >= 50 else '🔴'}"
    
    def _confirm_upload(self, video_path, callback):
        """Confirm and upload"""
        self.preview_window.destroy()
        if callback:
            callback(video_path)

print("✅ Video Preview Module loaded")
