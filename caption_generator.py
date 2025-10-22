import os
from config import USE_AI_CAPTIONS, OPENAI_API_KEY, DEFAULT_CAPTION_TEMPLATE

class CaptionGenerator:
    def __init__(self):
        self.use_ai = USE_AI_CAPTIONS
        self.api_key = OPENAI_API_KEY
    
    def generate_caption(self, video_filename, custom_keywords=""):
        """Caption generate karo - AI ya template se"""
        
        if self.use_ai and self.api_key:
            return self._generate_ai_caption(video_filename, custom_keywords)
        else:
            return self._generate_template_caption(video_filename, custom_keywords)
    
    def _generate_ai_caption(self, video_filename, custom_keywords):
        """OpenAI se caption generate karo (optional)"""
        try:
            import openai
            openai.api_key = self.api_key
            
            prompt = f"""
            Generate an engaging Instagram caption for a video named: {video_filename}
            Keywords: {custom_keywords}
            
            Requirements:
            - Keep it under 150 characters
            - Add 5-10 relevant hashtags
            - Make it engaging and trendy
            - Use emojis appropriately
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an Instagram caption expert."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150
            )
            
            caption = response.choices[0].message.content.strip()
            return caption
            
        except Exception as e:
            print(f"AI caption generation failed: {e}")
            return self._generate_template_caption(video_filename, custom_keywords)
    
    def _generate_template_caption(self, video_filename, custom_keywords=""):
        """Simple template se caption generate karo"""
        video_name = os.path.splitext(video_filename)[0].replace('_', ' ').title()
        
        caption = DEFAULT_CAPTION_TEMPLATE.format(video_name=video_name)
        
        if custom_keywords:
            caption += f"\n{custom_keywords}"
        
        return caption
