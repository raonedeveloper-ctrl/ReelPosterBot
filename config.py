import os

# Instagram Safety Settings
DELAY_BETWEEN_POSTS = (900, 1800)  # 15-30 minutes random delay (seconds)
MAX_POSTS_PER_DAY = 3  # Maximum 3 posts per day per account
SESSION_SAVE_PATH = "data/sessions/"
DATABASE_PATH = "data/videos_database.db"

# AI Caption Settings (Optional - Manual caption bhi dal sakte ho)
USE_AI_CAPTIONS = False  # True karo agar OpenAI use karna hai
OPENAI_API_KEY = ""  # Yaha apni API key dalo (optional)

# Default Caption Template (Agar AI nahi use kar rahe)
DEFAULT_CAPTION_TEMPLATE = """
✨ {video_name}

#viral #trending #explore #reels #instagram #love
"""

# Video Settings
SUPPORTED_VIDEO_FORMATS = ['.mp4', '.mov', '.avi']
VIDEO_FOLDER_PATH = "videos/"  # Default folder

# Create necessary directories
os.makedirs(SESSION_SAVE_PATH, exist_ok=True)
os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
os.makedirs(VIDEO_FOLDER_PATH, exist_ok=True)
os.makedirs("logs", exist_ok=True)
