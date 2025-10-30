"""
Audio Emotion Recognition Module
Detects emotions from voice/audio using speech features
"""
import numpy as np
import librosa
import sounddevice as sd
from scipy.io.wavfile import write
import os

class AudioEmotionDetector:
    def __init__(self, sample_rate=22050, duration=5):
        self.sample_rate = sample_rate
        self.duration = duration
        self.emotion_labels = ['angry', 'happy', 'neutral', 'sad']
        
    def record_audio(self, duration=None):
        """Record audio from microphone"""
        if duration is None:
            duration = self.duration
            
        print(f"🎤 Recording for {duration} seconds...")
        audio = sd.rec(int(duration * self.sample_rate), 
                      samplerate=self.sample_rate, 
                      channels=1)
        sd.wait()
        print("✅ Recording complete")
        return audio.flatten()
        
    def extract_features(self, audio_data):
        """Extract MFCC and other audio features"""
        # MFCCs (Mel-Frequency Cepstral Coefficients)
        mfccs = librosa.feature.mfcc(y=audio_data, sr=self.sample_rate, n_mfcc=40)
        mfccs_mean = np.mean(mfccs.T, axis=0)
        
        # Zero Crossing Rate
        zcr = np.mean(librosa.feature.zero_crossing_rate(audio_data))
        
        # Spectral features
        spectral_centroid = np.mean(librosa.feature.spectral_centroid(y=audio_data, sr=self.sample_rate))
        spectral_rolloff = np.mean(librosa.feature.spectral_rolloff(y=audio_data, sr=self.sample_rate))
        
        # Chroma features
        chroma = np.mean(librosa.feature.chroma_stft(y=audio_data, sr=self.sample_rate))
        
        # Combine features
        features = np.concatenate([
            mfccs_mean,
            [zcr, spectral_centroid, spectral_rolloff, chroma]
        ])
        
        return features
        
    def predict_emotion_simple(self, audio_data):
        """Simple rule-based emotion prediction based on audio characteristics"""
        features = self.extract_features(audio_data)
        
        # Get energy and pitch characteristics
        energy = np.mean(np.abs(audio_data))
        zcr = np.mean(librosa.feature.zero_crossing_rate(audio_data))
        
        # Simple heuristic classification
        if energy > 0.02 and zcr > 0.1:
            emotion = 'angry'
            confidence = 0.75
        elif energy > 0.015:
            emotion = 'happy'
            confidence = 0.70
        elif energy < 0.008:
            emotion = 'sad'
            confidence = 0.65
        else:
            emotion = 'neutral'
            confidence = 0.60
            
        # Return probabilities
        probs = {e: 0.1 for e in self.emotion_labels}
        probs[emotion] = confidence
        
        # Normalize
        total = sum(probs.values())
        probs = {k: v/total for k, v in probs.items()}
        
        return probs
        
    def get_emotion_probabilities(self, audio_data=None):
        """Get emotion probabilities from audio"""
        if audio_data is None:
            audio_data = self.record_audio()
            
        return self.predict_emotion_simple(audio_data)
        
    def detect_from_microphone(self):
        """Detect emotion from microphone input"""
        audio = self.record_audio()
        probs = self.get_emotion_probabilities(audio)
        
        # Get dominant emotion
        emotion = max(probs, key=probs.get)
        confidence = probs[emotion]
        
        print(f"🎭 Detected emotion: {emotion} (confidence: {confidence:.2f})")
        return emotion, probs
