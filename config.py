import os

# Instagram Safety Settings
DELAY_BETWEEN_POSTS = (900, 1800)  # 15-30 minutes
MAX_POSTS_PER_DAY = 4
SESSION_SAVE_PATH = "data/sessions/"
DATABASE_PATH = "data/videos_database.db"
ANALYTICS_DB_PATH = "data/analytics.db"

# Caption Settings - TXT FILE BASED (NO AI COST!)
USE_AI_CAPTIONS = False  # AI OFF, TXT file se lenge
CAPTIONS_FILE = "captions.txt"  # Caption file path
INSTAGRAM_USERNAME = "@therichlegacy"

# Trending Hashtags for Money/Wealth Niche (Auto-updated)
TRENDING_HASHTAGS = [
    # High Engagement (Money/Wealth/Success)
    "money", "business", "success", "entrepreneur", "motivation",
    "wealth", "luxury", "millionaire", "hustle", "financialfreedom",
    "rich", "lifestyle", "investment", "investing", "mindset",
    
    # Trending 2025
    "viral", "trending", "explore", "reels", "instagram"
]

MAX_HASHTAGS_PER_POST = 15  # Instagram best practice

# Automatic Posting Schedule
AUTO_POSTING_TIMES = ["13:00", "15:00", "16:00", "19:00"]
AUTO_DELETE_AFTER_UPLOAD = True

# Video Settings
SUPPORTED_VIDEO_FORMATS = ['.mp4', '.mov', '.avi']
VIDEO_FOLDER_PATH = "videos/"

# Analytics Settings
TRACK_ANALYTICS = True
FETCH_ANALYTICS_EVERY_HOURS = 6  # Har 6 ghante me analytics update

# Story Settings
AUTO_POST_TO_STORY = True  # Reel ko story me bhi post karo
STORY_DURATION_HOURS = 24  # Stories 24 hours ke liye

# Create directories
os.makedirs(SESSION_SAVE_PATH, exist_ok=True)
os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
os.makedirs(os.path.dirname(ANALYTICS_DB_PATH), exist_ok=True)
os.makedirs(VIDEO_FOLDER_PATH, exist_ok=True)
os.makedirs("logs", exist_ok=True)

# Create default captions file if not exists
if not os.path.exists(CAPTIONS_FILE):
    with open(CAPTIONS_FILE, 'w', encoding='utf-8') as f:
        f.write("""💸 Paisa kamaana mushkil nahi, seekhna zaroori hai! 💪
Rich banna luck nahi, decision hai! 🔥
Agar tu bhi next level jaana chahta hai, follow kar! 🚀
---
9 to 5 se nahi, mindset se hota hai paisa! ✨
Smart work > Hard work 😎
Luxury tab aati hai jab paisa aapke liye kaam kare! 💼
---
Business karne wale risk lete hai, excuses nahi! 💪
Rich mindset > Rich parents
Ab waqt hai smart work ka! 🚀
---
""")
