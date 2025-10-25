import sqlite3
import os

print("🔧 Fixing database...")

DB_PATH = "data/analytics.db"

if not os.path.exists(DB_PATH):
    print("✅ No database found, will create fresh on next run")
else:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute("ALTER TABLE post_analytics ADD COLUMN viral_score REAL DEFAULT 0")
        print("✅ Added viral_score column")
    except:
        print("ℹ️ viral_score already exists")
    
    try:
        cursor.execute("ALTER TABLE post_analytics ADD COLUMN upload_hour INTEGER DEFAULT 0")
        print("✅ Added upload_hour column")
    except:
        print("ℹ️ upload_hour already exists")
    
    try:
        cursor.execute("ALTER TABLE post_analytics ADD COLUMN upload_day_of_week INTEGER DEFAULT 0")
        print("✅ Added upload_day_of_week column")
    except:
        print("ℹ️ upload_day_of_week already exists")
    
    conn.commit()
    conn.close()
    print("\n✅ Database fixed successfully!")

print("\n🚀 Now run: python main.py")
