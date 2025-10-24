import ast
import inspect
import sys
import os
from datetime import datetime

print("=" * 80)
print("🔍 INSTAGRAM BOT - AUTOMATIC DIAGNOSTIC REPORT")
print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 80)
print()

# ==================== CHECK 1: FILE EXISTENCE ====================
print("📂 CHECK 1: Verifying file existence...")
required_files = [
    'main.py',
    'instagram_manager.py',
    'config.py',
    'advanced_analytics.py',
    'database_manager.py',
    'scheduler.py',
    'video_queue_manager.py',
    'caption_generator.py'
]

missing_files = []
for file in required_files:
    if not os.path.exists(file):
        missing_files.append(file)
        print(f"   ❌ MISSING: {file}")
    else:
        size = os.path.getsize(file)
        print(f"   ✅ FOUND: {file} ({size} bytes)")

if missing_files:
    print(f"\n⚠️ ERROR: {len(missing_files)} files are missing!")
else:
    print(f"\n✅ All required files present")

print()

# ==================== CHECK 2: INSTAGRAM_MANAGER METHODS ====================
print("🔍 CHECK 2: Analyzing instagram_manager.py methods...")

try:
    with open('instagram_manager.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Parse the file
    tree = ast.parse(content)
    
    # Find InstagramManager class
    instagram_manager_class = None
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == 'InstagramManager':
            instagram_manager_class = node
            break
    
    if not instagram_manager_class:
        print("   ❌ ERROR: InstagramManager class not found!")
    else:
        print(f"   ✅ InstagramManager class found")
        
        # List all methods
        methods = []
        for item in instagram_manager_class.body:
            if isinstance(item, ast.FunctionDef):
                methods.append(item.name)
        
        print(f"\n   📋 Methods found in InstagramManager class:")
        for method in methods:
            print(f"      • {method}()")
        
        # Check for required methods
        required_methods = [
            '__init__',
            'login',
            'logout',
            'upload_video',
            'get_realtime_account_stats',
            'get_user_posts_in_range',
            'refresh_account_insights'
        ]
        
        print(f"\n   🔎 Checking required methods:")
        missing_methods = []
        for method in required_methods:
            if method in methods:
                print(f"      ✅ {method}() - PRESENT")
            else:
                print(f"      ❌ {method}() - MISSING")
                missing_methods.append(method)
        
        if missing_methods:
            print(f"\n   ⚠️ ERROR: {len(missing_methods)} required methods are missing!")
            print(f"   Missing: {', '.join(missing_methods)}")
        
        # Check login method signature
        if 'login' in methods:
            for item in instagram_manager_class.body:
                if isinstance(item, ast.FunctionDef) and item.name == 'login':
                    # Check if it returns a tuple
                    returns_tuple = False
                    for node in ast.walk(item):
                        if isinstance(node, ast.Return) and node.value:
                            if isinstance(node.value, ast.Tuple):
                                returns_tuple = True
                    
                    if returns_tuple:
                        print(f"\n   ✅ login() method returns tuple (success, message)")
                    else:
                        print(f"\n   ⚠️ WARNING: login() method may not return tuple")
                        print(f"      Expected: return True, 'message'")
                        print(f"      This could cause: 'cannot unpack non-iterable bool object' error")

except FileNotFoundError:
    print("   ❌ ERROR: instagram_manager.py file not found!")
except Exception as e:
    print(f"   ❌ ERROR parsing file: {e}")

print()

# ==================== CHECK 3: MAIN.PY LOGIN HANDLER ====================
print("🔍 CHECK 3: Analyzing main.py login handler...")

try:
    with open('main.py', 'r', encoding='utf-8') as f:
        main_content = f.read()
    
    # Check if do_login expects tuple
    if 'success, message = self.insta_manager.login' in main_content:
        print("   ✅ main.py expects tuple: (success, message)")
        print("   ✅ Login handler correctly unpacks tuple")
    elif 'success = self.insta_manager.login' in main_content:
        print("   ⚠️ main.py expects boolean only")
        print("   ⚠️ This is incompatible with tuple return")
    else:
        print("   ⚠️ Could not determine login handler pattern")
    
    # Check for show_dashboard method
    if 'def show_dashboard(self):' in main_content:
        print("   ✅ show_dashboard() method exists in main.py")
        
        # Check indentation
        lines = main_content.split('\n')
        for i, line in enumerate(lines):
            if 'def show_dashboard(self):' in line:
                spaces = len(line) - len(line.lstrip())
                if spaces == 4:
                    print(f"   ✅ show_dashboard() has correct indentation (4 spaces)")
                elif spaces == 0:
                    print(f"   ❌ ERROR: show_dashboard() has NO indentation (line {i+1})")
                    print(f"      This method is NOT part of the class!")
                    print(f"      Fix: Add 4 spaces before 'def show_dashboard(self):'")
                else:
                    print(f"   ⚠️ WARNING: show_dashboard() has {spaces} spaces (line {i+1})")
                break
    else:
        print("   ❌ ERROR: show_dashboard() method not found in main.py")
    
    # Check for export_analytics_report method
    if 'def export_analytics_report(self, insights, days):' in main_content:
        print("   ✅ export_analytics_report() method exists")
    else:
        print("   ⚠️ WARNING: export_analytics_report() method not found")

except FileNotFoundError:
    print("   ❌ ERROR: main.py file not found!")
except Exception as e:
    print(f"   ❌ ERROR: {e}")

print()

# ==================== CHECK 4: IMPORT ISSUES ====================
print("🔍 CHECK 4: Testing imports...")

try:
    sys.path.insert(0, os.getcwd())
    
    print("   Testing: from instagram_manager import InstagramManager")
    from instagram_manager import InstagramManager
    print("   ✅ Import successful")
    
    # Check if InstagramManager has login method
    if hasattr(InstagramManager, 'login'):
        print("   ✅ InstagramManager.login exists in runtime")
        
        # Check method signature
        sig = inspect.signature(InstagramManager.login)
        print(f"   ✅ login() signature: {sig}")
    else:
        print("   ❌ ERROR: InstagramManager.login does NOT exist in runtime!")
        print("   ⚠️ This is the ROOT CAUSE of your error!")
        print("   ⚠️ File has the method, but Python doesn't see it")
        print("   ⚠️ Possible causes:")
        print("      1. Method has syntax error")
        print("      2. Method is not indented (not part of class)")
        print("      3. Method is defined after __init__ is called")
    
    # List all methods
    methods = [m for m in dir(InstagramManager) if not m.startswith('_')]
    print(f"\n   📋 InstagramManager runtime methods:")
    for method in methods:
        print(f"      • {method}")

except ImportError as e:
    print(f"   ❌ IMPORT ERROR: {e}")
except Exception as e:
    print(f"   ❌ ERROR: {e}")

print()

# ==================== CHECK 5: SYNTAX ERRORS ====================
print("🔍 CHECK 5: Checking for syntax errors...")

try:
    print("   Checking instagram_manager.py syntax...")
    with open('instagram_manager.py', 'r', encoding='utf-8') as f:
        code = f.read()
    
    try:
        compile(code, 'instagram_manager.py', 'exec')
        print("   ✅ instagram_manager.py has no syntax errors")
    except SyntaxError as e:
        print(f"   ❌ SYNTAX ERROR in instagram_manager.py:")
        print(f"      Line {e.lineno}: {e.msg}")
        print(f"      {e.text}")
        
except Exception as e:
    print(f"   ❌ ERROR: {e}")

print()

# ==================== DIAGNOSTIC SUMMARY ====================
print("=" * 80)
print("📊 DIAGNOSTIC SUMMARY")
print("=" * 80)
print()
print("If you see errors above, here's what to do:")
print()
print("1️⃣ If 'login() - MISSING': instagram_manager.py needs login method")
print("2️⃣ If 'login exists but runtime missing': Check method indentation")
print("3️⃣ If 'show_dashboard has NO indentation': Add 4 spaces before def")
print("4️⃣ If 'login does not return tuple': Fix return statements")
print("5️⃣ If 'SYNTAX ERROR': Fix the syntax error at reported line")
print()
print("💡 NEXT STEPS:")
print("   1. Review all ❌ ERROR messages above")
print("   2. Copy this entire report")
print("   3. Share with developer for exact fix")
print()
print("=" * 80)
print("Report completed. Save this output for reference.")
print("=" * 80)
