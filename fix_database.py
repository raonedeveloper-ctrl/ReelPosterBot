import sqlite3
import os

DB_PATH = "data/analytics.db"

def fix_database():
    """Fix existing database"""
    if not os.path.exists(DB_PATH):
        print("✅ Database doesn't exist yet, no fix needed")
        return
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Check if columns exist
    cursor.execute("PRAGMA table_info(post_analytics)")
    columns = [col[1] for col in cursor.fetchall()]
    
    fixes_applied = 0
    
    # Add missing columns
    if 'viral_score' not in columns:
        try:
            cursor.execute("ALTER TABLE post_analytics ADD COLUMN viral_score REAL DEFAULT 0")
            print("✅ Added viral_score column")
            fixes_applied += 1
        except Exception as e:
            print(f"⚠️ Could not add viral_score: {e}")
    
    if 'upload_hour' not in columns:
        try:
            cursor.execute("ALTER TABLE post_analytics ADD COLUMN upload_hour INTEGER DEFAULT 0")
            print("✅ Added upload_hour column")
            fixes_applied += 1
        except Exception as e:
            print(f"⚠️ Could not add upload_hour: {e}")
    
    if 'upload_day_of_week' not in columns:
        try:
            cursor.execute("ALTER TABLE post_analytics ADD COLUMN upload_day_of_week INTEGER DEFAULT 0")
            print("✅ Added upload_day_of_week column")
            fixes_applied += 1
        except Exception as e:
            print(f"⚠️ Could not add upload_day_of_week: {e}")
    
    conn.commit()
    conn.close()
    
    if fixes_applied > 0:
        print(f"\n✅ Database fixed! Applied {fixes_applied} fixes.")
    else:
        print("\n✅ Database is already up to date!")

if __name__ == "__main__":
    print("🔧 Fixing database...")
    fix_database()
    print("\n🚀 Now run: python main.py")
