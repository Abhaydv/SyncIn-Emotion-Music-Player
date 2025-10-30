#!/usr/bin/env python3
"""
Quick Start Guide for Multimodal Music Player
Run this to test your installation
"""
import sys
import os

def check_imports():
    """Check if all required packages are installed"""
    print("🔍 Checking dependencies...\n")
    
    packages = {
        'opencv-python': 'cv2',
        'tensorflow': 'tensorflow',
        'numpy': 'numpy',
        'pandas': 'pandas',
        'librosa': 'librosa',
        'sounddevice': 'sounddevice',
        'transformers': 'transformers',
        'torch': 'torch',
        'pygame': 'pygame',
        'scipy': 'scipy',
        'sklearn': 'sklearn'
    }
    
    missing = []
    for package_name, import_name in packages.items():
        try:
            __import__(import_name)
            print(f"✅ {package_name}")
        except ImportError:
            print(f"❌ {package_name} - MISSING")
            missing.append(package_name)
    
    if missing:
        print(f"\n⚠️  Missing packages: {', '.join(missing)}")
        print("\n💡 Install with: pip install " + " ".join(missing))
        return False
    
    print("\n✅ All dependencies installed!")
    return True

def check_files():
    """Check if required files exist"""
    print("\n🔍 Checking required files...\n")
    
    required = {
        'Model file': 'retrained_graph.pb',
        'Labels file': 'retrained_labels.txt',
        'Cascade file': 'haarcascade_frontalface_alt.xml',
        'Songs folder': 'songs/',
        'Emotions CSV folder': 'emotions_file/'
    }
    
    all_present = True
    for name, path in required.items():
        if os.path.exists(path):
            print(f"✅ {name}: {path}")
        else:
            print(f"❌ {name}: {path} - NOT FOUND")
            all_present = False
    
    if not all_present:
        print("\n⚠️  Some files are missing!")
        return False
        
    print("\n✅ All required files present!")
    return True

def print_usage():
    """Print usage instructions"""
    print("\n" + "="*70)
    print("🎵 MULTIMODAL MUSIC PLAYER - QUICK START")
    print("="*70)
    
    print("\n📋 STEP 1: Analyze Music Library (First time only)")
    print("-"*70)
    print("   python analyze_music.py")
    print("   ")
    print("   This will:")
    print("   • Extract audio features from all songs")
    print("   • Classify emotion of each song")
    print("   • Create music_emotion_db.json database")
    print("   • Takes ~5-10 minutes for 30 songs")
    
    print("\n📋 STEP 2: Run Multimodal Player")
    print("-"*70)
    print("   python multimodal_player.py")
    print("   ")
    print("   This will:")
    print("   • Detect emotion from your face (webcam)")
    print("   • Detect emotion from your voice (microphone)")
    print("   • Analyze emotion from your text input (optional)")
    print("   • Fuse all emotions intelligently")
    print("   • Recommend and play matching music")
    
    print("\n📋 STEP 3: Control Music Playback")
    print("-"*70)
    print("   P - Pause")
    print("   R - Resume")
    print("   S - Stop")
    print("   Q - Quit")
    
    print("\n💡 TIPS:")
    print("-"*70)
    print("   • Good lighting helps facial detection")
    print("   • Speak clearly for 5 seconds for audio detection")
    print("   • Text input is optional (press Enter to skip)")
    print("   • Try both mood matching and mood regulation strategies")
    
    print("\n🔧 CUSTOMIZATION:")
    print("-"*70)
    print("   Edit multimodal_player.py to:")
    print("   • Change fusion weights (facial/audio/text)")
    print("   • Switch fusion method (weighted vs attention)")
    print("   • Change recommendation strategy (matching vs regulation)")
    print("   • Adjust number of facial predictions")
    
    print("\n📊 TESTING INDIVIDUAL COMPONENTS:")
    print("-"*70)
    print("   # Test facial emotion")
    print("   python -c \"from src.emotion_detection.facial_emotion import *")
    print("   detector = FacialEmotionDetector()")
    print("   emotion = detector.detect_from_webcam()\"")
    print("   ")
    print("   # Test audio emotion")
    print("   python -c \"from src.emotion_detection.audio_emotion import *")
    print("   detector = AudioEmotionDetector()")
    print("   emotion, probs = detector.detect_from_microphone()\"")
    print("   ")
    print("   # Test text emotion")
    print("   python -c \"from src.emotion_detection.text_emotion import *")
    print("   detector = TextEmotionDetector()")
    print("   emotion, probs = detector.detect_from_input('I am so happy!')\"")
    
    print("\n" + "="*70)
    print("🚀 Ready to experience multimodal emotion recognition!")
    print("="*70 + "\n")

def main():
    print("\n" + "="*70)
    print("🎵 MULTIMODAL MUSIC PLAYER - INSTALLATION CHECK")
    print("="*70 + "\n")
    
    deps_ok = check_imports()
    files_ok = check_files()
    
    if deps_ok and files_ok:
        print("\n✅ ✅ ✅ SYSTEM READY! ✅ ✅ ✅")
        print_usage()
    else:
        print("\n⚠️  Please fix the issues above before running the player.")
        sys.exit(1)

if __name__ == "__main__":
    main()
