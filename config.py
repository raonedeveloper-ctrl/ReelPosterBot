import os
from datetime import datetime

# ==================== CORE SETTINGS ====================
APP_VERSION = "3.0.0-PRO"
DEBUG_MODE = False

# ==================== INSTAGRAM SAFETY ====================
DELAY_BETWEEN_POSTS = (900, 1800)  # 15-30 minutes (industry standard)
MAX_POSTS_PER_DAY = 4
MAX_ACTIONS_PER_HOUR = 30  # Conservative limit to avoid blocks
SESSION_SAVE_PATH = "data/sessions/"
DATABASE_PATH = "data/videos_database.db"
ANALYTICS_DB_PATH = "data/analytics.db"

# ==================== CAPTION & HASHTAG SYSTEM ====================
USE_AI_CAPTIONS = False  # TXT file based (cost-effective)
CAPTIONS_FILE = "captions.txt"
INSTAGRAM_USERNAME = "@therichlegacy"

# Advanced Hashtag System with categorization
HASHTAG_CATEGORIES = {
    'high_engagement': [
        'money', 'wealth', 'success', 'motivation', 'entrepreneur',
        'business', 'luxury', 'millionaire', 'hustle', 'rich'
    ],
    'trending_2025': [
        'viral', 'trending', 'explore', 'reels', 'fyp',
        'explorepage', 'instagood', 'instadaily'
    ],
    'niche_specific': [
        'financialfreedom', 'investing', 'moneymindset', 'wealthbuilding',
        'sidehustle', 'passiveincome', 'entrepreneurlife', 'luxurylifestyle'
    ],
    'engagement_boosters': [
        'follow', 'like', 'comment', 'share', 'savepost'
    ]
}

# Hashtag optimization settings
MIN_HASHTAGS_PER_POST = 10
MAX_HASHTAGS_PER_POST = 15
HASHTAG_ROTATION_ENABLED = True  # Avoid using same hashtags repeatedly

# ==================== INTELLIGENT SCHEDULING ====================
# AI will learn and optimize these times based on engagement data
INITIAL_POSTING_TIMES = ["10:00", "14:00", "18:00", "21:00"]  # Starting schedule
ENABLE_SMART_SCHEDULING = True  # AI will adjust based on performance
MIN_HOURS_BETWEEN_POSTS = 3
AVOID_POSTING_HOURS = [0, 1, 2, 3, 4, 5]  # Late night (low engagement)

# ==================== VIDEO MANAGEMENT ====================
AUTO_DELETE_AFTER_UPLOAD = True
SUPPORTED_VIDEO_FORMATS = ['.mp4', '.mov', '.avi']
VIDEO_FOLDER_PATH = "videos/"
VIDEO_QUEUE_PATH = "data/video_queue.json"

# Video quality settings
VIDEO_MAX_SIZE_MB = 30
PREFERRED_RESOLUTION = "1080p"
PREFERRED_FPS = 30

# ==================== ANALYTICS & TRACKING ====================
TRACK_ANALYTICS = True
FETCH_ANALYTICS_INTERVAL_HOURS = 6
CAPTION_AB_TEST_ENABLED = True
HASHTAG_PERFORMANCE_TRACKING = True
SHADOW_BAN_DETECTION_ENABLED = True

# Analytics thresholds
LOW_ENGAGEMENT_THRESHOLD = 2.0  # Below 2% engagement rate
SHADOW_BAN_DETECTION_THRESHOLD = 0.5  # 50% drop in reach
MIN_DATA_POINTS_FOR_PREDICTION = 10  # Minimum posts needed for AI predictions

# ==================== STORY SETTINGS ====================
AUTO_POST_TO_STORY = True
STORY_DURATION_HOURS = 24
STORY_MUSIC_ENABLED = False  # Future feature

# ==================== PERFORMANCE OPTIMIZATION ====================
ENABLE_QUEUE_SYSTEM = True
MAX_RETRY_ATTEMPTS = 3
ERROR_COOLDOWN_MINUTES = 30
SESSION_REFRESH_INTERVAL_HOURS = 24

# ==================== NOTIFICATIONS ====================
DESKTOP_NOTIFICATIONS = True
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR

# ==================== BACKUP & RECOVERY ====================
AUTO_BACKUP_ENABLED = True
BACKUP_INTERVAL_HOURS = 24
BACKUP_PATH = "backups/"
MAX_BACKUPS_TO_KEEP = 7

# ==================== DIRECTORY SETUP ====================
directories = [
    SESSION_SAVE_PATH,
    os.path.dirname(DATABASE_PATH),
    os.path.dirname(ANALYTICS_DB_PATH),
    os.path.dirname(VIDEO_QUEUE_PATH),
    VIDEO_FOLDER_PATH,
    BACKUP_PATH,
    "logs"
]

for directory in directories:
    os.makedirs(directory, exist_ok=True)

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
Luxury lifestyle ke liye mindset upgrade karo! ✨
Success karna hai to action lo! 💸
Dreams ko reality me convert karo! 🔥
---
Financial freedom > 9 to 5 job 🔥
Invest in yourself pehle! 💼
Rich logo ki mindset copy karo! 💰
---
""")

# Create initial video queue file
if not os.path.exists(VIDEO_QUEUE_PATH):
    import json
    with open(VIDEO_QUEUE_PATH, 'w') as f:
        json.dump({"queue": [], "history": []}, f)

print(f"✅ Configuration loaded - Version {APP_VERSION}")
 