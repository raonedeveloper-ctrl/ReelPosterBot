from core.instagram_manager import InstagramManager
from database_manager import DatabaseManager
import threading

class MultiAccountManager:
    """Manage multiple Instagram accounts"""
    
    def __init__(self):
        self.accounts = {}  # {username: InstagramManager}
        self.current_account = None
        self.db = DatabaseManager()
    
    def add_account(self, username, password):
        """Add new account"""
        manager = InstagramManager()
        success, message = manager.login(username, password)
        
        if success:
            self.accounts[username] = manager
            if not self.current_account:
                self.current_account = username
            return True, f"✅ Account added: {username}"
        
        return False, message
    
    def switch_account(self, username):
        """Switch to different account"""
        if username in self.accounts:
            self.current_account = username
            return True, f"✅ Switched to: {username}"
        
        return False, "❌ Account not found"
    
    def get_current_manager(self):
        """Get current active account manager"""
        if self.current_account and self.current_account in self.accounts:
            return self.accounts[self.current_account]
        return None
    
    def get_all_accounts(self):
        """List all logged-in accounts"""
        return list(self.accounts.keys())
    
    def cross_post(self, video_path, target_accounts, caption=None):
        """Post to multiple accounts"""
        results = {'success': [], 'failed': []}
        
        for username in target_accounts:
            if username in self.accounts:
                manager = self.accounts[username]
                success, message = manager.upload_video(video_path, caption)
                
                if success:
                    results['success'].append(username)
                else:
                    results['failed'].append((username, message))
        
        return results
    
    def get_combined_stats(self, days=7):
        """Get combined stats from all accounts"""
        combined = {
            'total_posts': 0,
            'total_likes': 0,
            'total_comments': 0,
            'total_views': 0,
            'total_followers': 0
        }
        
        for username, manager in self.accounts.items():
            try:
                dashboard = manager.get_performance_dashboard(days)
                combined['total_posts'] += dashboard.get('total_posts', 0)
                combined['total_likes'] += dashboard.get('total_likes', 0)
                combined['total_comments'] += dashboard.get('total_comments', 0)
                combined['total_views'] += dashboard.get('total_views', 0)
                
                account_info = manager.get_account_info()
                if account_info:
                    combined['total_followers'] += account_info['followers']
            except:
                continue
        
        return combined
    
    def remove_account(self, username):
        """Remove account"""
        if username in self.accounts:
            self.accounts[username].logout()
            del self.accounts[username]
            
            if self.current_account == username:
                self.current_account = list(self.accounts.keys())[0] if self.accounts else None
            
            return True, f"✅ Account removed: {username}"
        
        return False, "❌ Account not found"

print("✅ Multi-Account Manager loaded")
