"""
Text Emotion Recognition Module
Analyzes emotions from text using NLP
"""
from transformers import pipeline
import numpy as np

class TextEmotionDetector:
    def __init__(self):
        try:
            # Use emotion classification model
            self.classifier = pipeline("text-classification", 
                                      model="j-hartmann/emotion-english-distilroberta-base",
                                      return_all_scores=True)
            self.model_loaded = True
        except Exception as e:
            print(f"⚠️  Could not load transformer model: {e}")
            print("💡 Using rule-based text analysis instead")
            self.model_loaded = False
            
        # Emotion keywords for rule-based fallback
        self.emotion_keywords = {
            'angry': ['angry', 'furious', 'mad', 'irritated', 'annoyed', 'hate', 'rage'],
            'happy': ['happy', 'joy', 'excited', 'great', 'awesome', 'love', 'wonderful'],
            'sad': ['sad', 'depressed', 'unhappy', 'miserable', 'crying', 'hurt'],
            'neutral': ['okay', 'fine', 'normal', 'alright']
        }
        
    def analyze_text_simple(self, text):
        """Simple keyword-based emotion analysis"""
        text_lower = text.lower()
        scores = {emotion: 0 for emotion in self.emotion_keywords}
        
        for emotion, keywords in self.emotion_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    scores[emotion] += 1
                    
        # Normalize scores
        total = sum(scores.values())
        if total == 0:
            return {'neutral': 0.8, 'happy': 0.1, 'sad': 0.05, 'angry': 0.05}
        
        probs = {k: v/total for k, v in scores.items()}
        return probs
        
    def get_emotion_probabilities(self, text):
        """Get emotion probabilities from text"""
        if not text or len(text.strip()) == 0:
            return {'neutral': 0.8, 'happy': 0.1, 'sad': 0.05, 'angry': 0.05}
            
        if self.model_loaded:
            try:
                results = self.classifier(text)[0]
                # Convert to our emotion format
                probs = {}
                for item in results:
                    label = item['label'].lower()
                    score = item['score']
                    
                    # Map model labels to our emotions
                    if label in ['joy', 'happy']:
                        probs['happy'] = score
                    elif label in ['anger', 'angry']:
                        probs['angry'] = score
                    elif label in ['sadness', 'sad']:
                        probs['sad'] = score
                    elif label in ['neutral']:
                        probs['neutral'] = score
                    elif label in ['fear', 'surprise', 'disgust']:
                        # Distribute these to existing emotions
                        probs['neutral'] = probs.get('neutral', 0) + score/3
                        
                # Ensure all emotions have values
                for emotion in ['angry', 'happy', 'sad', 'neutral']:
                    if emotion not in probs:
                        probs[emotion] = 0.01
                        
                # Normalize
                total = sum(probs.values())
                probs = {k: v/total for k, v in probs.items()}
                return probs
            except Exception as e:
                print(f"⚠️  Model prediction failed: {e}")
                return self.analyze_text_simple(text)
        else:
            return self.analyze_text_simple(text)
            
    def detect_from_input(self, text=None):
        """Detect emotion from text input"""
        if text is None:
            text = input("💬 Enter your text: ")
            
        probs = self.get_emotion_probabilities(text)
        emotion = max(probs, key=probs.get)
        confidence = probs[emotion]
        
        print(f"🎭 Detected emotion: {emotion} (confidence: {confidence:.2f})")
        return emotion, probs
