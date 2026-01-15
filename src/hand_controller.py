import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import time

class HandController:
    def __init__(self):
        print("🔄 Инициализация MediaPipe...")
        
        # ПРЯМОЙ импорт (без конфликтов)
        self.hands = mp.solutions.hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        self.mp_draw = mp.solutions.drawing_utils
        
        self.cursor_history = []
        self.pinch_history = []
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.01
        print("✅ HandController готов!")

    def detect_pinch(self, landmarks):
        """Pinch = большой+указательный палец близко"""
        thumb_tip = landmarks[4]   # Кончик большого
        index_tip = landmarks[8]   # Кончик указательного
        
        dist = ((thumb_tip.x - index_tip.x)**2 + 
                (thumb_tip.y - index_tip.y)**2)**0.5
        return dist < 0.06

    def process_frame(self, frame):
        """Кадр → курсор + клик"""
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(frame_rgb)
        
        cursor_x, cursor_y = None, None
        pinch = False
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Рисуем руку
                self.mp_draw.draw_landmarks(
                    frame, hand_landmarks, 
                    mp.solutions.hands.HAND_CONNECTIONS
                )
                
                landmarks = hand_landmarks.landmark
                index_tip = landmarks[8]
                
                # Палец → курсор экрана
                x = int(index_tip.x * pyautogui.size().width)
                y = int(index_tip.y * pyautogui.size().height)
                
                # Сглаживание (5 кадров)
                self.cursor_history.append((x, y))
                if len(self.cursor_history) > 5:
                    self.cursor_history.pop(0)
                
                cursor_x = int(np.mean([p[0] for p in self.cursor_history]))
                cursor_y = int(np.mean([p[1] for p in self.cursor_history]))
                
                pinch = self.detect_pinch(landmarks)
        
        return frame, cursor_x, cursor_y, pinch
