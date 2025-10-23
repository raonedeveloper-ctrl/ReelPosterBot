import time
import random
from datetime import datetime, timedelta

class EngagementAutomator:
    """Automate engagement activities safely"""
    
    def __init__(self, client):
        self.client = client
        self.actions_today = 0
        self.max_actions_per_day = 100
        self.min_delay = 20  # seconds
        self.max_delay = 60
    
    def auto_like_comments(self, media_id, max_likes=10):
        """Auto-like comments on your post"""
        if self.actions_today >= self.max_actions_per_day:
            return False, "⚠️ Daily action limit reached"
        
        try:
            comments = self.client.media_comments(media_id, amount=max_likes)
            
            liked_count = 0
            
            for comment in comments:
                try:
                    self.client.comment_like(comment.pk)
                    liked_count += 1
                    self.actions_today += 1
                    
                    # Random delay
                    time.sleep(random.randint(self.min_delay, self.max_delay))
                    
                    if liked_count >= max_likes:
                        break
                        
                except Exception as e:
                    print(f"Like error: {e}")
                    continue
            
            return True, f"✅ Liked {liked_count} comments"
            
        except Exception as e:
            return False, f"❌ Error: {e}"
    
    def auto_reply_comments(self, media_id, reply_templates, max_replies=5):
        """Auto-reply to comments"""
        if self.actions_today >= self.max_actions_per_day:
            return False, "⚠️ Daily action limit reached"
        
        try:
            comments = self.client.media_comments(media_id, amount=20)
            
            replied_count = 0
            replied_users = set()
            
            for comment in comments:
                # Skip if already replied to this user
                if comment.user.username in replied_users:
                    continue
                
                # Simple spam detection
                if len(comment.text) < 3 or comment.text.count('http') > 0:
                    continue
                
                try:
                    # Choose reply based on comment sentiment
                    reply = self._choose_reply(comment.text, reply_templates)
                    
                    if reply:
                        self.client.media_comment(media_id, f"@{comment.user.username} {reply}")
                        replied_count += 1
                        replied_users.add(comment.user.username)
                        self.actions_today += 1
                        
                        # Random delay
                        time.sleep(random.randint(self.min_delay, self.max_delay))
                        
                        if replied_count >= max_replies:
                            break
                    
                except Exception as e:
                    print(f"Reply error: {e}")
                    continue
            
            return True, f"✅ Replied to {replied_count} comments"
            
        except Exception as e:
            return False, f"❌ Error: {e}"
    
    def _choose_reply(self, comment_text, templates):
        """Choose appropriate reply template"""
        comment_lower = comment_text.lower()
        
        # Positive keywords
        if any(word in comment_lower for word in ['love', 'amazing', 'great', 'awesome', 'nice']):
            return random.choice(templates.get('positive', ["Thank you! ❤️"]))
        
        # Question keywords
        if '?' in comment_text:
            return random.choice(templates.get('question', ["Great question! Let me know if you need more info 😊"]))
        
        # Default
        return random.choice(templates.get('default', ["Thanks for your comment! 🙏"]))
    
    def engage_with_hashtag(self, hashtag, max_likes=20):
        """Like posts from specific hashtag"""
        if self.actions_today >= self.max_actions_per_day:
            return False, "⚠️ Daily action limit reached"
        
        try:
            medias = self.client.hashtag_medias_recent(hashtag, amount=max_likes * 2)
            
            liked_count = 0
            
            for media in medias:
                try:
                    # Skip if already liked
                    if media.has_liked:
                        continue
                    
                    self.client.media_like(media.pk)
                    liked_count += 1
                    self.actions_today += 1
                    
                    # Random delay
                    time.sleep(random.randint(self.min_delay, self.max_delay))
                    
                    if liked_count >= max_likes:
                        break
                        
                except Exception as e:
                    print(f"Like error: {e}")
                    continue
            
            return True, f"✅ Liked {liked_count} posts from #{hashtag}"
            
        except Exception as e:
            return False, f"❌ Error: {e}"
    
    def get_actions_remaining(self):
        """Get remaining actions for today"""
        return self.max_actions_per_day - self.actions_today

print("✅ Engagement Automator Module loaded")
