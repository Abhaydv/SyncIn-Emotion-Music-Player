# 🎵 SyncIn - Emotion-Based Music Player

[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.20-orange.svg)](https://tensorflow.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

**SyncIn** is an intelligent music player that uses **Computer Vision** and **Emotion Recognition** to automatically play music based on your mood! Simply look at your webcam, let the AI detect your emotion, and enjoy songs that match your feelings.

## 🎯 Features

- **Real-time Emotion Detection**: Uses your webcam to detect facial expressions
- **AI-Powered Recognition**: Built with TensorFlow for accurate emotion classification
- **Automatic Music Selection**: Plays songs matching your detected mood
- **Three Emotion Categories**: Angry, Happy, and Neutral/Sad
- **Interactive Music Controls**: Pause, resume, stop, and exit functionality
- **Error Handling**: Automatically skips corrupted audio files
- **Cross-Platform**: Works on macOS, Linux, and Windows

## 🚀 Quick Start

### Prerequisites

- Python 3.13 or higher
- Webcam
- macOS, Linux, or Windows

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/bhargav59/SyncIn-Emotion-Music-Player.git
   cd SyncIn-Emotion-Music-Player
   ```

2. **Create and activate virtual environment**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On macOS/Linux
   # OR
   .venv\Scripts\activate     # On Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

```bash
python label.py
```

The application will:

1. Open your webcam in a window titled "Capture"
2. Detect your face and analyze your emotion (collects 10 predictions)
3. Determine your predominant mood
4. Open a "Music Player Controls" window and start playing music

## 🎮 Controls

### Webcam Window

- **ESC** - Exit the application

### Music Player Controls Window

- **P** - Pause music
- **R** - Resume music
- **S** - Stop current song
- **E** or **Q** - Exit player

## 📚 Libraries & Technologies

| Library          | Version | Purpose                                 |
| ---------------- | ------- | --------------------------------------- |
| **OpenCV (cv2)** | Latest  | Face detection and webcam capture       |
| **TensorFlow**   | 2.20+   | Deep learning emotion recognition model |
| **NumPy**        | Latest  | Numerical operations and array handling |
| **Pandas**       | Latest  | Reading and managing song playlists     |
| **Pygame**       | Latest  | Audio playback and UI controls          |

## 🔄 How It Works

### System Flow

```
┌─────────────────┐
│  Webcam Capture │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Face Detection  │ (OpenCV Haar Cascade)
│ haarcascade_    │
│ frontalface_    │
│ alt.xml         │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Emotion         │ (TensorFlow Model)
│ Recognition     │ retrained_graph.pb
│ (label_image.py)│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Collect 10      │
│ Predictions     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Determine Most  │
│ Common Emotion  │
│ (Angry/Happy/   │
│  Neutral-Sad)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Load Song from  │
│ emotions_file/  │
│ [emotion].csv   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Play Music      │ (Pygame)
│ from songs/     │
└─────────────────┘
```

### Detailed Process

1. **Face Detection (`label.py`)**

   - Captures video from webcam using OpenCV
   - Detects faces using Haar Cascade classifier
   - Extracts face region and saves as `test.jpg`

2. **Emotion Recognition (`label_image.py`)**

   - Loads pre-trained TensorFlow model (`retrained_graph.pb`)
   - Processes face image through neural network
   - Returns emotion classification (1=Angry, 2=Happy, 3=Neutral/Sad)

3. **Prediction Collection**

   - Collects 10 emotion predictions for accuracy
   - Calculates most frequent emotion detected

4. **Music Selection (`play_music_pygame.py`)**
   - Reads corresponding CSV file from `emotions_file/`
   - Randomly selects a song from the playlist
   - Loads and plays the MP3 file using Pygame

## 📁 Project Structure

```
SyncIn-Emotion-Music-Player/
├── label.py                              # Main application entry point
├── label_image.py                        # TensorFlow emotion recognition
├── play_music_pygame.py                  # Music player with controls
├── face_crop.py                          # Face cropping utility
├── retrain.py                            # Model training script
├── requirements.txt                      # Python dependencies
├── retrained_graph.pb                    # Pre-trained TensorFlow model
├── retrained_labels.txt                  # Emotion labels mapping
├── haarcascade_frontalface_alt.xml       # Face detection cascade
├── emotions_file/                        # Emotion-based playlists
│   ├── Angry.csv
│   ├── Happy.csv
│   └── NeutralOrSad.csv
├── songs/                                # Music library (MP3 files)
└── images/                               # Training dataset
    ├── angry/
    ├── happy/
    └── neutral or sad/
```

## 🎓 Training Your Own Model

If you want to train a custom emotion recognition model:

1. Add training images to the `images/` folders (angry, happy, neutral or sad)
2. Follow instructions in `how to train.txt`
3. Run `retrain.py` to generate a new `retrained_graph.pb` model
4. The new model will be used automatically

## 🎵 Adding Your Own Songs

1. Add MP3 files to the `songs/` folder
2. Update the corresponding CSV file in `emotions_file/`:
   - `Angry.csv` for angry mood songs
   - `Happy.csv` for happy mood songs
   - `NeutralOrSad.csv` for calm/sad mood songs
3. Add song names (without .mp3 extension) to the CSV

## 🐛 Troubleshooting

### Webcam not working

- Check if another application is using the webcam
- Grant camera permissions to Terminal/Python

### TensorFlow warnings

- These are normal compatibility warnings and don't affect functionality

### Corrupted MP3 file error

- The app will automatically skip corrupted files
- Remove or replace the corrupted MP3 from the songs folder

### Permission denied on macOS

- Run: `chmod +x label.py`
- Grant necessary permissions in System Preferences → Security & Privacy

## 🔧 Technical Improvements (v2.0)

- ✅ Updated for TensorFlow 2.x compatibility
- ✅ Replaced keyboard library with Pygame event handling
- ✅ Added error handling for corrupted audio files
- ✅ macOS compatibility fixes (replaced `cls` with `clear`)
- ✅ Improved music player controls with GUI window
- ✅ Added virtual environment support
- ✅ Created comprehensive requirements.txt

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

**Bhargav Sah**

- GitHub: [@bhargav59](https://github.com/bhargav59)
- Portfolio: [bhargav59.github.io/Portfolio](https://bhargav59.github.io/Portfolio/)

## 🙏 Acknowledgments

- Original concept by [mmudit30](https://github.com/mmudit30/SyncIn)
- TensorFlow team for the deep learning framework
- OpenCV community for computer vision tools
- Pygame community for audio playback capabilities

---

⭐ If you found this project helpful, please give it a star!
