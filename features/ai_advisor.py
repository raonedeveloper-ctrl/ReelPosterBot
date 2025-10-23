import cv2
import numpy as np
from collections import Counter
import re

class AIContentAdvisor:
    """AI-powered content analysis and recommendations"""
    
    def __init__(self):
        self.quality_threshold = 70
    
    def analyze_video(self, video_path):
        """Comprehensive video analysis"""
        analysis = {
            'technical_score': 0,
            'content_score': 0,
            'engagement_prediction': 0,
            'recommendations': [],
            'should_post': False
        }
        
        # Technical analysis
        tech_score = self._analyze_technical_quality(video_path)
        analysis['technical_score'] = tech_score
        
        # Content analysis
        content_score = self._analyze_content_quality(video_path)
        analysis['content_score'] = content_score
        
        # Overall score
        overall = (tech_score + content_score) / 2
        analysis['overall_score'] = round(overall, 1)
        
        # Engagement prediction (ML-based would be better)
        analysis['engagement_prediction'] = self._predict_engagement(overall)
        
        # Recommendations
        analysis['recommendations'] = self._generate_recommendations(tech_score, content_score)
        
        # Post decision
        analysis['should_post'] = overall >= self.quality_threshold
        
        return analysis
    
    def _analyze_technical_quality(self, video_path):
        """Analyze technical aspects"""
        score = 0
        
        try:
            cap = cv2.VideoCapture(video_path)
            
            # Get video properties
            fps = cap.get(cv2.CAP_PROP_FPS)
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            duration = frame_count / fps if fps > 0 else 0
            
            # Resolution score (40 points)
            if width >= 1080 and height >= 1920:
                score += 40
            elif width >= 720 and height >= 1280:
                score += 30
            else:
                score += 20
            
            # FPS score (20 points)
            if fps >= 60:
                score += 20
            elif fps >= 30:
                score += 15
            else:
                score += 10
            
            # Duration score (20 points) - 15-60s ideal
            if 15 <= duration <= 60:
                score += 20
            elif 10 <= duration <= 90:
                score += 15
            else:
                score += 10
            
            # Frame quality analysis (20 points)
            frame_quality = self._analyze_frame_quality(cap)
            score += frame_quality
            
            cap.release()
            
        except Exception as e:
            print(f"Technical analysis error: {e}")
            score = 50  # Default score
        
        return min(score, 100)
    
    def _analyze_frame_quality(self, cap):
        """Analyze frame brightness and sharpness"""
        score = 0
        sample_frames = []
        
        # Sample 10 frames
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        sample_indices = np.linspace(0, total_frames - 1, 10, dtype=int)
        
        for idx in sample_indices:
            cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
            ret, frame = cap.read()
            
            if ret:
                sample_frames.append(frame)
        
        if sample_frames:
            # Brightness check
            avg_brightness = np.mean([np.mean(cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)) 
                                     for f in sample_frames])
            
            if 50 <= avg_brightness <= 200:  # Good brightness range
                score += 10
            else:
                score += 5
            
            # Sharpness check (Laplacian variance)
            sharpness_scores = []
            for frame in sample_frames:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
                sharpness_scores.append(laplacian_var)
            
            avg_sharpness = np.mean(sharpness_scores)
            
            if avg_sharpness > 100:  # Sharp
                score += 10
            elif avg_sharpness > 50:  # Acceptable
                score += 7
            else:
                score += 3
        
        return score
    
    def _analyze_content_quality(self, video_path):
        """Analyze content-related factors"""
        score = 50  # Base score
        
        # In a real implementation, you would:
        # 1. Analyze scene changes (more = engaging)
        # 2. Detect faces (human content = better)
        # 3. Check color vibrancy
        # 4. Analyze motion (dynamic = better)
        
        # Simplified version
        try:
            cap = cv2.VideoCapture(video_path)
            
            # Scene change detection
            scene_changes = self._detect_scene_changes(cap)
            
            if scene_changes > 3:
                score += 20
            elif scene_changes > 1:
                score += 10
            
            # Motion analysis
            motion_score = self._analyze_motion(cap)
            score += motion_score
            
            cap.release()
            
        except Exception as e:
            print(f"Content analysis error: {e}")
        
        return min(score, 100)
    
    def _detect_scene_changes(self, cap):
        """Detect number of scene changes"""
        prev_frame = None
        changes = 0
        frame_count = 0
        
        while frame_count < 100:  # Sample first 100 frames
            ret, frame = cap.read()
            if not ret:
                break
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            if prev_frame is not None:
                diff = cv2.absdiff(prev_frame, gray)
                if np.mean(diff) > 30:  # Threshold for scene change
                    changes += 1
            
            prev_frame = gray
            frame_count += 1
        
        return changes
    
    def _analyze_motion(self, cap):
        """Analyze video motion/dynamics"""
        # Simplified motion score
        return 15  # Placeholder
    
    def _predict_engagement(self, quality_score):
        """Predict engagement based on quality"""
        # Simple linear prediction
        # In reality, use ML model trained on historical data
        
        base_engagement = quality_score * 0.05  # 0-5% engagement
        
        # Random factor for variability
        import random
        variation = random.uniform(-0.5, 0.5)
        
        return round(max(0, base_engagement + variation), 2)
    
    def _generate_recommendations(self, tech_score, content_score):
        """Generate improvement recommendations"""
        recommendations = []
        
        if tech_score < 70:
            if tech_score < 50:
                recommendations.append("🔴 Improve video resolution (1080x1920 minimum)")
            recommendations.append("⚠️ Consider increasing frame rate to 30+ FPS")
            recommendations.append("💡 Check video duration (15-60 seconds ideal)")
        
        if content_score < 70:
            recommendations.append("🎨 Add more visual variety and scene changes")
            recommendations.append("⚡ Increase motion/dynamics in video")
            recommendations.append("✨ Improve lighting and color vibrancy")
        
        if tech_score >= 70 and content_score >= 70:
            recommendations.append("✅ Great quality! Ready to post")
            recommendations.append("💡 Consider posting at optimal time")
            recommendations.append("📝 Use trending hashtags for reach")
        
        return recommendations
    
    def generate_smart_caption(self, video_analysis, trending_topics=None):
        """Generate AI-powered caption"""
        score = video_analysis.get('overall_score', 50)
        
        # Caption templates based on score
        if score >= 80:
            openings = [
                "🔥 This is incredible! ",
                "✨ Pure magic! ",
                "💯 Perfection! ",
            ]
        elif score >= 60:
            openings = [
                "Check this out! ",
                "Here's something cool: ",
                "You'll love this: ",
            ]
        else:
            openings = [
                "New post! ",
                "Here we go: ",
                "Latest update: ",
            ]
        
        import random
        caption = random.choice(openings)
        
        # Add context
        caption += "Drop a ❤️ if you enjoyed!\n\n"
        
        # Add hashtags
        caption += "#reels #viral #trending #instagram #explore"
        
        return caption

print("✅ AI Content Advisor Module loaded")

