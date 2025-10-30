"""
Quick script to analyze music library
Run this once to create music emotion database
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from src.music_analysis.music_emotion_recognition import MusicEmotionAnalyzer

def main():
    print("🎵 Music Library Analysis Tool")
    print("="*60)
    
    analyzer = MusicEmotionAnalyzer()
    
    # Check if database exists
    if analyzer.load_database():
        print("\n📊 Current Database Statistics:")
        print(f"   Total songs: {len(analyzer.music_database)}")
        
        # Count songs by emotion
        emotion_counts = {'angry': 0, 'happy': 0, 'neutral': 0, 'sad': 0}
        for song, data in analyzer.music_database.items():
            dominant = data.get('dominant_emotion', 'neutral')
            emotion_counts[dominant] = emotion_counts.get(dominant, 0) + 1
            
        print("\n   Songs by emotion:")
        for emotion, count in emotion_counts.items():
            print(f"   • {emotion:10s}: {count}")
        
        choice = input("\n🔄 Re-analyze music library? (y/N): ")
        if choice.lower() != 'y':
            print("✅ Using existing database")
            return
    
    # Analyze library
    print("\n🔬 Analyzing music library...")
    analyzer.analyze_music_library('songs')
    
    print("\n✅ Analysis complete!")
    print("\n💡 You can now run: python multimodal_player.py")

if __name__ == "__main__":
    main()
