"""
Music Recommendation Engine
Intelligent music selection based on detected emotions
"""
import random
import pandas as pd
import os

class MusicRecommendationEngine:
    def __init__(self, music_analyzer=None):
        self.music_analyzer = music_analyzer
        self.emotion_mapping = {
            'angry': '1',
            'happy': '2',
            'neutral': '3',
            'sad': '3'
        }
        self.emotion_folders = {
            '1': 'Angry.csv',
            '2': 'Happy.csv',
            '3': 'NeutralOrSad.csv'
        }
        self.strategy = 'mood_matching'  # or 'mood_regulation'
        
    def set_strategy(self, strategy):
        """Set recommendation strategy: 'mood_matching' or 'mood_regulation'"""
        self.strategy = strategy
        
    def mood_regulation_mapping(self, emotion):
        """Map emotions for mood regulation (e.g., sad -> uplifting)"""
        regulation_map = {
            'angry': 'neutral',  # Calm down angry
            'sad': 'happy',      # Uplift sad
            'happy': 'happy',    # Enhance happy
            'neutral': 'happy'   # Energize neutral
        }
        return regulation_map.get(emotion, emotion)
        
    def get_song_from_csv(self, emotion):
        """Get random song from emotion CSV file"""
        emotion_code = self.emotion_mapping.get(emotion, '3')
        csv_file = self.emotion_folders.get(emotion_code, 'NeutralOrSad.csv')
        csv_path = os.path.join('emotions_file', csv_file)
        
        if not os.path.exists(csv_path):
            print(f"⚠️  CSV file not found: {csv_path}")
            return None
            
        try:
            df = pd.read_csv(csv_path)
            df_top = df.columns[0]
            count = df[df_top].count()
            
            if count == 0:
                return None
                
            random_index = random.randrange(0, count)
            song_name = df[df_top][random_index]
            return song_name
        except Exception as e:
            print(f"⚠️  Error reading CSV: {e}")
            return None
            
    def get_songs_from_analyzer(self, emotion, top_n=5):
        """Get songs from music analyzer database"""
        if self.music_analyzer and self.music_analyzer.music_database:
            return self.music_analyzer.find_songs_by_emotion(emotion, top_n)
        return []
        
    def recommend_song(self, detected_emotion, use_analyzer=False):
        """Recommend a song based on detected emotion"""
        target_emotion = detected_emotion
        
        # Apply strategy
        if self.strategy == 'mood_regulation':
            target_emotion = self.mood_regulation_mapping(detected_emotion)
            print(f"🎯 Mood Regulation: {detected_emotion} → {target_emotion}")
        else:
            print(f"🎯 Mood Matching: {target_emotion}")
            
        # Try music analyzer first if available
        if use_analyzer:
            songs = self.get_songs_from_analyzer(target_emotion, top_n=5)
            if songs:
                song = random.choice(songs)
                print(f"🎵 Selected from analyzer: {song}")
                return song
                
        # Fallback to CSV-based selection
        song = self.get_song_from_csv(target_emotion)
        if song:
            print(f"🎵 Selected from CSV: {song}")
        return song
        
    def generate_playlist(self, detected_emotion, num_songs=5, use_analyzer=False):
        """Generate a playlist based on emotion"""
        playlist = []
        target_emotion = detected_emotion
        
        if self.strategy == 'mood_regulation':
            target_emotion = self.mood_regulation_mapping(detected_emotion)
            
        # Get songs from analyzer
        if use_analyzer and self.music_analyzer:
            songs = self.get_songs_from_analyzer(target_emotion, top_n=num_songs)
            playlist.extend(songs)
            
        # Fill remaining with CSV songs
        while len(playlist) < num_songs:
            song = self.get_song_from_csv(target_emotion)
            if song and song not in playlist:
                playlist.append(song)
            else:
                break
                
        return playlist
        
    def get_recommendation_explanation(self, detected_emotion):
        """Get explanation for recommendation"""
        if self.strategy == 'mood_regulation':
            target = self.mood_regulation_mapping(detected_emotion)
            explanations = {
                ('angry', 'neutral'): "You seem angry. Let's calm you down with peaceful music.",
                ('sad', 'happy'): "You seem sad. Let's lift your spirits with uplifting music!",
                ('happy', 'happy'): "You're happy! Let's keep that energy going!",
                ('neutral', 'happy'): "Let's add some energy to your day!"
            }
            return explanations.get((detected_emotion, target), f"Playing {target} music for you.")
        else:
            return f"You seem {detected_emotion}. Playing music that matches your mood."
