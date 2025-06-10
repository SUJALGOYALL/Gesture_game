import cv2
import mediapipe as mp
import numpy as np
import time
import keyboard

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

# Cooldown timers
last_kick_time = 0
last_punch_time = 0
cooldown_kick = 0.1  # seconds
cooldown_punch = 0.1  # seconds

# Thresholds
HARD_KICK_THRESHOLD = 0.40
NORMAL_KICK_THRESHOLD = 0.20
UPPER_PUNCH_Y_THRESHOLD = 0.1
HIGH_PUNCH_ARM_EXTEND = 0.20
JOIN_HANDS_THRESHOLD = 0.05

# For on-screen label
detected_move = ""
label_timer = 0
label_duration = 1.0  # seconds

# Activation flag
gesture_control_active = False

# Start video capture
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    result = pose.process(rgb)
    current_time = time.time()

    if result.pose_landmarks:
        landmarks = result.pose_landmarks.landmark

        # Key landmarks
        r_ankle = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE]
        l_ankle = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE]
        r_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST]
        l_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]
        r_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]

        # Detect join hands to start
        hands_distance = np.sqrt((r_wrist.x - l_wrist.x) ** 2 + (r_wrist.y - l_wrist.y) ** 2)
        if not gesture_control_active and hands_distance < JOIN_HANDS_THRESHOLD:
            gesture_control_active = True
            detected_move = "Gesture Control Started"
            label_timer = current_time

        if gesture_control_active:
            # Kick detection
            foot_dist = np.sqrt((r_ankle.x - l_ankle.x) ** 2 + (r_ankle.y - l_ankle.y) ** 2)
            foot_x_dist = abs(r_ankle.x - l_ankle.x)

            if current_time - last_kick_time > cooldown_kick:
                if foot_dist > HARD_KICK_THRESHOLD:
                    print("🦵 Hard Kick")
                    keyboard.press_and_release('j')
                    detected_move = "Hard Kick"
                    label_timer = current_time
                    last_kick_time = current_time
                elif foot_x_dist > NORMAL_KICK_THRESHOLD:
                    print("➡️ Move Forward")
                    keyboard.press_and_release('d')  # ← updated key from 'k' to 'd'
                    detected_move = "Move Forward"   # ← updated label
                    label_timer = current_time
                    last_kick_time = current_time

            # Upper punch detection
            wrist_shoulder_y = r_shoulder.y - r_wrist.y
            wrist_shoulder_x = abs(r_wrist.x - r_shoulder.x)

            if current_time - last_punch_time > cooldown_punch:
                if wrist_shoulder_y > UPPER_PUNCH_Y_THRESHOLD:
                    print("👊 Upper Punch")
                    keyboard.press_and_release('l')
                    detected_move = "Upper Punch"
                    label_timer = current_time
                    last_punch_time = current_time
                elif wrist_shoulder_x > HIGH_PUNCH_ARM_EXTEND:
                    print("👊 High Punch")
                    keyboard.press_and_release('i')
                    detected_move = "High Punch"
                    label_timer = current_time
                    last_punch_time = current_time

        # Draw landmarks
        mp_drawing.draw_landmarks(frame, result.pose_landmarks, mp_pose.POSE_CONNECTIONS)

    # Show label
    if detected_move and current_time - label_timer < label_duration:
        cv2.putText(frame, f"{detected_move}", (30, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (128, 128, 128), 2, cv2.LINE_AA)

    cv2.imshow("Pose Detection", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC to exit
        break

cap.release()
cv2.destroyAllWindows()
