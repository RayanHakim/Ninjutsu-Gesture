# ⚔️ Shinobi Vision: AI-Powered Ninjutsu Gesture Recognition

A high-performance computer vision project built with **Python 3.12** that recognizes Shinobi hand seals and triggers real-time visual effects (Chroma Keying) and spatial audio. This project demonstrates the integration of AI Pose Estimation, Multimedia Processing, and Real-time State Management.



## ✨ Features
- **Real-time Hand Tracking:** Powered by MediaPipe Hands with `model_complexity=0` for high FPS on laptop CPUs.
- **Dynamic Chroma Keying:** Seamlessly overlays green screen MP4 videos (Fire, Lightning, Water, Rasengan) onto the user's palm coordinates.
- **Synchronized SFX:** Low-latency audio triggers using `pygame.mixer` that loop during active gestures and stop immediately when the hand is withdrawn.
- **Advanced Gesture Logic:** - ✊ **Katon (Fire):** All fingers closed (Fist).
  - 🖐️ **Chidori (Lightning):** All fingers open and spread.
  - 🤘 **Suiton (Water):** Index and Pinky fingers open (Metal pose).
  - ☝️ **Rasengan:** Index finger extended (Pointing pose).
- **Performance Monitor:** Built-in FPS counter to monitor CPU/GPU overhead.

## 🛠️ Tech Stack
- **Python 3.12.10**
- **OpenCV:** Image processing, ROI manipulation, and Chroma Keying.
- **MediaPipe:** ML-based hand landmark detection.
- **Pygame Mixer:** Multi-channel audio management.
- **NumPy:** Matrix operations for mask inversion and bitwise blending.

## 🚀 Installation & Setup

### 1. Prerequisite
Ensure you are using **Python 3.12** (MediaPipe stability on Windows).

### 2. Clone & Install Dependencies
```bash
pip install opencv-python mediapipe pygame numpy
