import os
import random
import hashlib
from config import (
    CAPTIONS_FILE, 
    HASHTAG_CATEGORIES,
    MIN_HASHTAGS_PER_POST,
    MAX_HASHTAGS_PER_POST,
    HASHTAG_ROTATION_ENABLED,
    INSTAGRAM_USERNAME,
    CAPTION_AB_TEST_ENABLED
)

class CaptionGenerator:
    """Advanced caption generation with A/B testing and smart hashtags"""
    
    def __init__(self, analytics_manager=None):
        self.captions = self._load_captions()
        self.used_captions = set()
        self.analytics = analytics_manager
        self.hashtag_history = []
    
    def _load_captions(self):
        """Load captions from file"""
        if not os.path.exists(CAPTIONS_FILE):
            return []
        
        try:
            with open(CAPTIONS_FILE, 'r', encoding='utf-8') as f:
                content = f.read()
            
            captions = [c.strip() for c in content.split('---') if c.strip()]
            return captions
        except Exception as e:
            print(f"❌ Error loading captions: {e}")
            return []
    
    def generate_caption(self, video_filename="", custom_keywords=""):
        """Generate optimized caption with smart hashtags"""
        
        # Select caption
        caption_text = self._select_caption()
        
        # Generate optimized hashtags
        hashtags = self._generate_smart_hashtags(caption_text, custom_keywords)
        
        # Create variant ID for A/B testing
        variant_id = self._create_variant_id(caption_text, hashtags)
        
        # Register for A/B testing
        if CAPTION_AB_TEST_ENABLED and self.analytics:
            self.analytics.register_caption_variant(variant_id, caption_text, hashtags)
        
        # Build final caption
        final_caption = f"""{caption_text}

👉 Follow {INSTAGRAM_USERNAME} for more! 🚀

{hashtags}"""
        
        return final_caption, variant_id
    
    def _select_caption(self):
        """Smart caption selection with rotation"""
        
        # Get best performing captions if we have analytics data
        if CAPTION_AB_TEST_ENABLED and self.analytics:
            try:
                best_variants = self.analytics.get_best_caption_variants(limit=3)
                if best_variants and random.random() < 0.7:  # 70% use best performers
                    return random.choice(best_variants)[0]
            except:
                pass
        
        # Fallback to file-based captions
        available_captions = [c for c in self.captions if c not in self.used_captions]
        
        if not available_captions:
            self.used_captions.clear()
            available_captions = self.captions
        
        if not available_captions:
            return f"💸 Rich Mindset 🔥\nFollow {INSTAGRAM_USERNAME} for daily motivation! 🚀"
        
        caption = random.choice(available_captions)
        self.used_captions.add(caption)
        
        return caption
    
    def _generate_smart_hashtags(self, caption_text, custom_keywords=""):
        """Generate optimized hashtags based on performance data"""
        
        selected_tags = []
        
        # Get best performing hashtags from analytics
        if self.analytics:
            try:
                best_hashtags = self.analytics.get_best_performing_hashtags(
                    INSTAGRAM_USERNAME, 
                    limit=8
                )
                if best_hashtags:
                    selected_tags.extend([h['hashtag'] for h in best_hashtags[:5]])
            except:
                pass
        
        # Add context-based hashtags
        caption_lower = caption_text.lower()
        
        keyword_map = {
            'money': ['money', 'wealth', 'financialfreedom'],
            'paisa': ['money', 'wealth', 'rich'],
            'business': ['business', 'entrepreneur', 'hustle'],
            'luxury': ['luxury', 'rich', 'millionaire'],
            'success': ['success', 'motivation', 'entrepreneur'],
            'invest': ['investing', 'investment', 'wealth']
        }
        
        for keyword, tags in keyword_map.items():
            if keyword in caption_lower:
                selected_tags.extend(tags[:2])
        
        # Remove duplicates
        selected_tags = list(dict.fromkeys(selected_tags))
        
        # Add category hashtags to reach target count
        remaining = MAX_HASHTAGS_PER_POST - len(selected_tags)
        
        if remaining > 0:
            # Prioritize high engagement category
            pool = (HASHTAG_CATEGORIES['high_engagement'] + 
                   HASHTAG_CATEGORIES['trending_2025'] + 
                   HASHTAG_CATEGORIES['niche_specific'])
            
            # Avoid recently used if rotation enabled
            if HASHTAG_ROTATION_ENABLED:
                pool = [h for h in pool if h not in self.hashtag_history[-30:]]
            
            additional = random.sample(pool, min(remaining, len(pool)))
            selected_tags.extend(additional)
        
        # Limit to max hashtags
        selected_tags = selected_tags[:MAX_HASHTAGS_PER_POST]
        
        # Ensure minimum hashtags
        if len(selected_tags) < MIN_HASHTAGS_PER_POST:
            needed = MIN_HASHTAGS_PER_POST - len(selected_tags)
            pool = HASHTAG_CATEGORIES['high_engagement']
            selected_tags.extend(random.sample(pool, min(needed, len(pool))))
        
        # Update history
        self.hashtag_history.extend(selected_tags)
        self.hashtag_history = self.hashtag_history[-100:]  # Keep last 100
        
        # Format hashtags
        hashtags = ' '.join([f'#{tag}' for tag in selected_tags])
        
        return hashtags
    
    def _create_variant_id(self, caption, hashtags):
        """Create unique ID for caption variant"""
        content = f"{caption[:50]}{hashtags[:50]}"
        return hashlib.md5(content.encode()).hexdigest()[:12]
    
    def reload_captions(self):
        """Reload captions from file"""
        self.captions = self._load_captions()
        self.used_captions.clear()
        return len(self.captions)

print("✅ Smart Caption Generator loaded")
