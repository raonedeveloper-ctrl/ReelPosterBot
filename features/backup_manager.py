import os
import shutil
import json
from datetime import datetime
import zipfile

class BackupManager:
    """Backup and restore bot data"""
    
    def __init__(self):
        self.backup_dir = "backups/"
        os.makedirs(self.backup_dir, exist_ok=True)
    
    def create_backup(self):
        """Create complete backup"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"backup_{timestamp}"
        backup_path = os.path.join(self.backup_dir, backup_name)
        
        try:
            os.makedirs(backup_path, exist_ok=True)
            
            # Backup databases
            if os.path.exists("data/"):
                shutil.copytree("data/", os.path.join(backup_path, "data"))
            
            # Backup sessions
            if os.path.exists("sessions/"):
                shutil.copytree("sessions/", os.path.join(backup_path, "sessions"))
            
            # Backup config
            if os.path.exists("config.py"):
                shutil.copy2("config.py", backup_path)
            
            # Backup captions
            if os.path.exists("captions.json"):
                shutil.copy2("captions.json", backup_path)
            
            # Create backup info
            info = {
                'created': datetime.now().isoformat(),
                'version': '3.0.0-PRO',
                'files_backed_up': os.listdir(backup_path)
            }
            
            with open(os.path.join(backup_path, "backup_info.json"), 'w') as f:
                json.dump(info, f, indent=2)
            
            # Create ZIP archive
            zip_path = f"{backup_path}.zip"
            self._create_zip(backup_path, zip_path)
            
            # Remove unzipped folder
            shutil.rmtree(backup_path)
            
            return True, f"✅ Backup created: {backup_name}.zip"
            
        except Exception as e:
            return False, f"❌ Backup failed: {e}"
    
    def _create_zip(self, source_dir, zip_path):
        """Create ZIP archive"""
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(source_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, source_dir)
                    zipf.write(file_path, arcname)
    
    def restore_backup(self, backup_file):
        """Restore from backup"""
        try:
            # Extract ZIP
            extract_path = backup_file.replace('.zip', '')
            
            with zipfile.ZipFile(backup_file, 'r') as zipf:
                zipf.extractall(extract_path)
            
            # Restore data
            if os.path.exists(os.path.join(extract_path, "data")):
                if os.path.exists("data/"):
                    shutil.rmtree("data/")
                shutil.copytree(os.path.join(extract_path, "data"), "data")
            
            # Restore sessions
            if os.path.exists(os.path.join(extract_path, "sessions")):
                if os.path.exists("sessions/"):
                    shutil.rmtree("sessions/")
                shutil.copytree(os.path.join(extract_path, "sessions"), "sessions")
            
            # Restore config
            if os.path.exists(os.path.join(extract_path, "config.py")):
                shutil.copy2(os.path.join(extract_path, "config.py"), "config.py")
            
            # Restore captions
            if os.path.exists(os.path.join(extract_path, "captions.json")):
                shutil.copy2(os.path.join(extract_path, "captions.json"), "captions.json")
            
            # Clean up
            shutil.rmtree(extract_path)
            
            return True, "✅ Backup restored successfully! Please restart the bot."
            
        except Exception as e:
            return False, f"❌ Restore failed: {e}"
    
    def list_backups(self):
        """List all available backups"""
        backups = []
        
        for file in os.listdir(self.backup_dir):
            if file.endswith('.zip'):
                file_path = os.path.join(self.backup_dir, file)
                size = os.path.getsize(file_path) / (1024 * 1024)  # MB
                modified = datetime.fromtimestamp(os.path.getmtime(file_path))
                
                backups.append({
                    'name': file,
                    'path': file_path,
                    'size': f"{size:.2f} MB",
                    'date': modified.strftime("%Y-%m-%d %H:%M:%S")
                })
        
        return sorted(backups, key=lambda x: x['date'], reverse=True)
    
    def delete_backup(self, backup_file):
        """Delete backup file"""
        try:
            os.remove(backup_file)
            return True, "✅ Backup deleted"
        except Exception as e:
            return False, f"❌ Delete failed: {e}"

print("✅ Backup Manager Module loaded")

