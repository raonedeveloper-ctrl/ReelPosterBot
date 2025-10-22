import os
import random
from config import (
    CAPTIONS_FILE, 
    TRENDING_HASHTAGS, 
    MAX_HASHTAGS_PER_POST,
    INSTAGRAM_USERNAME
)

class CaptionGenerator:
    def __init__(self):
        self.captions = self._load_captions()
        self.used_captions = set()
    
    def _load_captions(self):
        """TXT file se captions load karo"""
        if not os.path.exists(CAPTIONS_FILE):
            return []
        
        try:
            with open(CAPTIONS_FILE, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # --- se split karke captions list banao
            captions = [c.strip() for c in content.split('---') if c.strip()]
            return captions
        except Exception as e:
            print(f"❌ Error loading captions: {e}")
            return []
    
    def generate_caption(self, video_filename="", custom_keywords=""):
        """Caption + trending hashtags generate karo"""
        
        # Random caption select karo (jo already use nahi hua)
        available_captions = [c for c in self.captions if c not in self.used_captions]
        
        # Agar sab captions use ho gaye, reset karo
        if not available_captions:
            self.used_captions.clear()
            available_captions = self.captions
        
        if not available_captions:
            # Fallback agar file empty hai
            caption_text = f"💸 Rich Mindset 🔥\nFollow {INSTAGRAM_USERNAME} for daily motivation! 🚀"
        else:
            caption_text = random.choice(available_captions)
            self.used_captions.add(caption_text)
        
        # Trending hashtags add karo
        hashtags = self._generate_trending_hashtags(caption_text, custom_keywords)
        
        # Final caption
        final_caption = f"""{caption_text}

👉 Follow {INSTAGRAM_USERNAME} for more! 🚀

{hashtags}"""
        
        return final_caption
    
    def _generate_trending_hashtags(self, caption_text, custom_keywords):
        """Caption ke context se related trending hashtags"""
        
        # Caption me keywords detect karo
        caption_lower = caption_text.lower()
        
        # Priority hashtags (caption me agar yeh words hai)
        priority_tags = []
        
        keyword_map = {
            'money': ['money', 'millionaire', 'financialfreedom', 'wealth'],
            'business': ['business', 'entrepreneur', 'hustle', 'success'],
            'luxury': ['luxury', 'rich', 'lifestyle', 'millionaire'],
            'investment': ['investment', 'investing', 'wealth', 'financialfreedom'],
            'mindset': ['mindset', 'motivation', 'success', 'entrepreneur']
        }
        
        # Caption ke keywords se related tags find karo
        for keyword, tags in keyword_map.items():
            if keyword in caption_lower:
                priority_tags.extend(tags[:3])
        
        # Priority tags + random trending tags
        selected_tags = list(set(priority_tags))  # Duplicates remove
        
        # Remaining slots fill karo
        remaining = MAX_HASHTAGS_PER_POST - len(selected_tags)
        if remaining > 0:
            random_tags = random.sample(
                [t for t in TRENDING_HASHTAGS if t not in selected_tags],
                min(remaining, len(TRENDING_HASHTAGS))
            )
            selected_tags.extend(random_tags)
        
        # Limit to MAX_HASHTAGS
        selected_tags = selected_tags[:MAX_HASHTAGS_PER_POST]
        
        # Format hashtags
        hashtags = ' '.join([f'#{tag}' for tag in selected_tags])
        
        return hashtags
    
    def reload_captions(self):
        """Captions file reload karo (agar update kiya ho)"""
        self.captions = self._load_captions()
        self.used_captions.clear()
        return len(self.captions)
