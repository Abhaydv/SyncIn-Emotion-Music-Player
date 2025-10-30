"""
Multimodal Fusion Module
Combines emotions from facial, audio, and text modalities
"""
import numpy as np

class MultimodalFusion:
    def __init__(self, fusion_method='weighted_average'):
        self.fusion_method = fusion_method
        # Default weights for each modality
        self.weights = {
            'facial': 0.4,
            'audio': 0.35,
            'text': 0.25
        }
        self.emotion_labels = ['angry', 'happy', 'neutral', 'sad']
        
    def set_weights(self, facial=0.4, audio=0.35, text=0.25):
        """Set custom weights for modalities"""
        total = facial + audio + text
        self.weights = {
            'facial': facial / total,
            'audio': audio / total,
            'text': text / total
        }
        
    def normalize_emotions(self, emotion_dict):
        """Normalize emotion probabilities to standard format"""
        # Convert to standard emotions
        normalized = {emotion: 0.0 for emotion in self.emotion_labels}
        
        for emotion, prob in emotion_dict.items():
            emotion_lower = emotion.lower()
            if 'angry' in emotion_lower or 'anger' in emotion_lower:
                normalized['angry'] += prob
            elif 'happy' in emotion_lower or 'joy' in emotion_lower:
                normalized['happy'] += prob
            elif 'sad' in emotion_lower:
                normalized['sad'] += prob
            elif 'neutral' in emotion_lower:
                normalized['neutral'] += prob
            else:
                # Distribute unknown emotions
                normalized['neutral'] += prob / 2
                normalized['sad'] += prob / 2
                
        # Normalize to sum to 1
        total = sum(normalized.values())
        if total > 0:
            normalized = {k: v/total for k, v in normalized.items()}
        else:
            normalized = {emotion: 0.25 for emotion in self.emotion_labels}
            
        return normalized
        
    def weighted_average_fusion(self, facial_probs, audio_probs, text_probs):
        """Combine emotions using weighted average"""
        # Normalize all inputs
        facial = self.normalize_emotions(facial_probs) if facial_probs else {e: 0.25 for e in self.emotion_labels}
        audio = self.normalize_emotions(audio_probs) if audio_probs else {e: 0.25 for e in self.emotion_labels}
        text = self.normalize_emotions(text_probs) if text_probs else {e: 0.25 for e in self.emotion_labels}
        
        # Compute weighted average
        fused_probs = {}
        for emotion in self.emotion_labels:
            fused_probs[emotion] = (
                self.weights['facial'] * facial.get(emotion, 0) +
                self.weights['audio'] * audio.get(emotion, 0) +
                self.weights['text'] * text.get(emotion, 0)
            )
            
        # Normalize
        total = sum(fused_probs.values())
        if total > 0:
            fused_probs = {k: v/total for k, v in fused_probs.items()}
            
        return fused_probs
        
    def attention_fusion(self, facial_probs, audio_probs, text_probs, 
                        facial_confidence=1.0, audio_confidence=1.0, text_confidence=1.0):
        """
        Attention-based fusion that weights modalities by their confidence
        """
        confidences = [facial_confidence, audio_confidence, text_confidence]
        total_confidence = sum(confidences)
        
        if total_confidence == 0:
            return self.weighted_average_fusion(facial_probs, audio_probs, text_probs)
            
        # Normalize confidences to get attention weights
        attention_weights = [c / total_confidence for c in confidences]
        
        # Temporarily adjust weights based on confidence
        old_weights = self.weights.copy()
        self.weights = {
            'facial': attention_weights[0],
            'audio': attention_weights[1],
            'text': attention_weights[2]
        }
        
        result = self.weighted_average_fusion(facial_probs, audio_probs, text_probs)
        
        # Restore original weights
        self.weights = old_weights
        
        return result
        
    def fuse_emotions(self, facial_probs=None, audio_probs=None, text_probs=None,
                     facial_conf=1.0, audio_conf=1.0, text_conf=1.0):
        """
        Main fusion method
        Returns fused emotion probabilities
        """
        if self.fusion_method == 'weighted_average':
            return self.weighted_average_fusion(facial_probs, audio_probs, text_probs)
        elif self.fusion_method == 'attention':
            return self.attention_fusion(facial_probs, audio_probs, text_probs,
                                        facial_conf, audio_conf, text_conf)
        else:
            return self.weighted_average_fusion(facial_probs, audio_probs, text_probs)
            
    def get_dominant_emotion(self, fused_probs):
        """Get the dominant emotion and its confidence"""
        emotion = max(fused_probs, key=fused_probs.get)
        confidence = fused_probs[emotion]
        return emotion, confidence
        
    def print_fusion_results(self, fused_probs):
        """Pretty print fusion results"""
        print("\n🧠 Multimodal Fusion Results:")
        print("="*50)
        sorted_emotions = sorted(fused_probs.items(), key=lambda x: x[1], reverse=True)
        for emotion, prob in sorted_emotions:
            bar = "█" * int(prob * 30)
            print(f"{emotion:10s} {prob:5.2%} {bar}")
        print("="*50)
        
        dominant_emotion, confidence = self.get_dominant_emotion(fused_probs)
        print(f"\n✨ Final Emotion: {dominant_emotion.upper()} (confidence: {confidence:.2%})")
        return dominant_emotion
