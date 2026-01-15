import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import sys
import time

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.01

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.5)

def count_fingers_up(landmarks):
    fingers = 0
    tips = [4, 8, 12, 16, 20]
    if landmarks[4].x < landmarks[3].x:
        fingers += 1
    for tip in tips[1:]:
        if landmarks[tip].y < landmarks[tip-2].y:
            fingers += 1
    return fingers

def is_fist(landmarks):
    return count_fingers_up(landmarks) == 0

def main():
    cap = cv2.VideoCapture(0)
    cursor_history = []
    last_click = 0

    print("🚀 GestureOS v2 — MediaPipe")
    print("🖐️ Ладонь = курсор | ✊ Кулак = клик | Q=выход")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        h, w = frame.shape[:2]
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = hands.process(rgb_frame)

        hand_center = None
        is_fist_detected = False
        fingers_up = 0

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                landmarks = hand_landmarks.landmark

                palm_center = landmarks[9]
                hand_center = (int(palm_center.x * w), int(palm_center.y * h))

                fingers_up = count_fingers_up(landmarks)
                is_fist_detected = is_fist(landmarks)

                color = (0, 0, 255) if is_fist_detected else (0, 255, 0)
                cv2.circle(frame, hand_center, 40, color, 5)
                cv2.circle(frame, hand_center, 25, color, -1)

        if hand_center:
            cx, cy = hand_center
            screen_x = int(cx / w * pyautogui.size().width)
            screen_y = int((cy / h * 0.8 + 0.1) * pyautogui.size().height)

            cursor_history.append((screen_x, screen_y))
            if len(cursor_history) > 8:
                cursor_history.pop(0)

            smooth_x = int(np.mean([p[0] for p in cursor_history]))
            smooth_y = int(np.mean([p[1] for p in cursor_history]))
            pyautogui.moveTo(smooth_x, smooth_y)

            if is_fist_detected:
                current_time = time.time()
                if current_time - last_click > 0.5:
                    print("🖱️ КЛИК!")
                    pyautogui.click()
                    last_click = current_time

        status = f"ИЩЕМ КИСТЬ"
        color = (0, 255, 255)
        if hand_center:
            status = f"🖐️ ({fingers_up}/5)" if not is_fist_detected else f"✊ КУЛАК"
            color = (0, 255, 0) if not is_fist_detected else (0, 0, 255)

        cv2.putText(frame, status, (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 3)
        cv2.putText(frame, "Q=выход", (20, h-30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        cv2.imshow("GestureOS v2", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⏹️ Остановлено")
