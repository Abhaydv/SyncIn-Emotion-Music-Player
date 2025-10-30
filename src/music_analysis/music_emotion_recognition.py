"""
Music Emotion Recognition Module
Analyzes emotions in music tracks
"""
import librosa
import numpy as np
import json
import os

class MusicEmotionAnalyzer:
    def __init__(self):
        self.emotion_labels = ['angry', 'happy', 'neutral', 'sad']
        self.music_database = {}
        
    def extract_music_features(self, audio_path):
        """Extract audio features from music file"""
        try:
            y, sr = librosa.load(audio_path, duration=30)  # Load first 30 seconds
            
            # Tempo and beat
            tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
            
            # Spectral features
            spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
            spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)[0]
            
            # Zero crossing rate
            zcr = librosa.feature.zero_crossing_rate(y)[0]
            
            # MFCCs
            mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
            
            # Chroma features (harmony)
            chroma = librosa.feature.chroma_stft(y=y, sr=sr)
            
            # Energy/RMS
            rms = librosa.feature.rms(y=y)[0]
            
            features = {
                'tempo': float(tempo),
                'spectral_centroid_mean': float(np.mean(spectral_centroids)),
                'spectral_rolloff_mean': float(np.mean(spectral_rolloff)),
                'zcr_mean': float(np.mean(zcr)),
                'mfcc_mean': float(np.mean(mfccs)),
                'chroma_mean': float(np.mean(chroma)),
                'energy_mean': float(np.mean(rms))
            }
            
            return features
        except Exception as e:
            print(f"⚠️  Error extracting features from {audio_path}: {e}")
            return None
            
    def predict_music_emotion(self, features):
        """Predict emotion of music based on features"""
        if not features:
            return {'neutral': 1.0}
            
        tempo = features['tempo']
        energy = features['energy_mean']
        valence = features['chroma_mean']  # Proxy for positivity
        
        # Rule-based classification
        probs = {}
        
        # Happy: fast tempo, high energy, positive valence
        if tempo > 120 and energy > 0.15 and valence > 0.5:
            probs['happy'] = 0.7
            probs['angry'] = 0.1
            probs['sad'] = 0.05
            probs['neutral'] = 0.15
            
        # Angry: fast tempo, very high energy
        elif tempo > 110 and energy > 0.2:
            probs['angry'] = 0.6
            probs['happy'] = 0.2
            probs['sad'] = 0.1
            probs['neutral'] = 0.1
            
        # Sad: slow tempo, low energy
        elif tempo < 80 and energy < 0.12:
            probs['sad'] = 0.7
            probs['neutral'] = 0.2
            probs['happy'] = 0.05
            probs['angry'] = 0.05
            
        # Neutral: moderate everything
        else:
            probs['neutral'] = 0.6
            probs['happy'] = 0.2
            probs['sad'] = 0.15
            probs['angry'] = 0.05
            
        return probs
        
    def analyze_song(self, audio_path):
        """Analyze a single song and return emotion"""
        features = self.extract_music_features(audio_path)
        if features:
            emotion_probs = self.predict_music_emotion(features)
            dominant_emotion = max(emotion_probs, key=emotion_probs.get)
            return {
                'features': features,
                'emotions': emotion_probs,
                'dominant_emotion': dominant_emotion
            }
        return None
        
    def analyze_music_library(self, songs_folder='songs'):
        """Analyze all songs in library and save to database"""
        print("🎵 Analyzing music library...")
        
        if not os.path.exists(songs_folder):
            print(f"⚠️  Folder {songs_folder} not found")
            return
            
        for filename in os.listdir(songs_folder):
            if filename.endswith('.mp3'):
                song_path = os.path.join(songs_folder, filename)
                song_name = filename[:-4]  # Remove .mp3
                
                print(f"   Analyzing: {song_name}")
                analysis = self.analyze_song(song_path)
                
                if analysis:
                    self.music_database[song_name] = analysis
                    
        print(f"✅ Analyzed {len(self.music_database)} songs")
        self.save_database()
        
    def save_database(self, filepath='data/music_emotion_db.json'):
        """Save music emotion database"""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(self.music_database, f, indent=2)
        print(f"💾 Database saved to {filepath}")
        
    def load_database(self, filepath='data/music_emotion_db.json'):
        """Load music emotion database"""
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                self.music_database = json.load(f)
            print(f"📂 Loaded {len(self.music_database)} songs from database")
            return True
        return False
        
    def find_songs_by_emotion(self, target_emotion, top_n=5):
        """Find songs matching target emotion"""
        if not self.music_database:
            self.load_database()
            
        if not self.music_database:
            return []
            
        # Score each song based on target emotion
        song_scores = []
        for song_name, data in self.music_database.items():
            emotion_prob = data['emotions'].get(target_emotion, 0)
            song_scores.append((song_name, emotion_prob))
            
        # Sort by score
        song_scores.sort(key=lambda x: x[1], reverse=True)
        
        return [song for song, score in song_scores[:top_n]]
