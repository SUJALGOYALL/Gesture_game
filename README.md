
# Gesture-Controlled Game Using MediaPipe & OpenCV

This project implements a gesture-based control system for gaming using a webcam. By tracking body landmarks with MediaPipe's pose estimation model, users can trigger game actions like move forward, hard kick, upper punch, and high punch with simple body gestures. No hardware sensors or controllers are needed—just your webcam and some moves!




## 📽️Demo

Insert gif or link to demo (COMMING SOON)


## Gesture guide

| Gesture                   | Action Triggered   | Key Pressed |
| ------------------------- | ------------------ | ----------- |
| 🤝 Join Hands             | Start control mode | —           |
| 🦵 Leg spread > 0.40      | Hard Kick          | `J`         |
| ➡️ Foot x-distance > 0.20 | Move Forward       | `D`         |
| 🙌 Wrist above shoulder   | Upper Punch        | `L`         |
| 👉 Arm extended sideways  | High Punch         | `I`         |

## 🧠 How It Works?

Uses MediaPipe Pose to detect landmarks (wrists, ankles, shoulders).

Calculates distances and positions to interpret gestures.

Uses Python's keyboard library to simulate keypresses mapped to gaming actions.

Displays the current detected move on-screen using OpenCV.
## Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/gesture-game-control.git
cd gesture-game-control
```

2. Install dependencies:
Make sure you’re using Python 3.7+
```bash
pip install opencv-python mediapipe numpy keyboard
```
🚀 How to Run
```bash
python gesture_game.py
```
## Authors

- [@Sujal Goyal](https://github.com/SUJALGOYALL)


## License
This project is open-source and available under the
[MIT License](https://choosealicense.com/licenses/mit/)

