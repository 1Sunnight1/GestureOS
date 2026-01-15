import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import time

# Настройки PyAutoGUI
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.01

class GestureOS:
    def __init__(self):
        print("🔄 Инициализация GestureOS...")
        self.mp_hands = mp.solutions.hands
        self.mp_draw = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        self.cursor_history = []
        self.last_click = 0
        print("✅ GestureOS готов!")

    def detect_pinch(self, landmarks):
        """Pinch = клик по иконке"""
        thumb_tip = landmarks[4]   # Большой палец
        index_tip = landmarks[8]   # Указательный
        dist = ((thumb_tip.x - index_tip.x)**2 + 
                (thumb_tip.y - index_tip.y)**2)**0.5
        return dist < 0.06

    def process_frame(self, frame):
        """Обработка кадра → курсор + клик"""
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(frame_rgb)
        
        cursor_x, cursor_y = None, None
        pinch = False
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Рисуем landmarks руки
                self.mp_draw.draw_landmarks(
                    frame, hand_landmarks, 
                    self.mp_hands.HAND_CONNECTIONS
                )
                
                landmarks = hand_landmarks.landmark
                index_tip = landmarks[8]
                
                # Указательный палец → курсор экрана
                x = int(index_tip.x * pyautogui.size().width)
                y = int(index_tip.y * pyautogui.size().height)
                
                # Сглаживание курсора (5 кадров)
                self.cursor_history.append((x, y))
                if len(self.cursor_history) > 5:
                    self.cursor_history.pop(0)
                
                cursor_x = int(np.mean([p[0] for p in self.cursor_history]))
                cursor_y = int(np.mean([p[1] for p in self.cursor_history]))
                
                # Проверяем pinch
                pinch = self.detect_pinch(landmarks)
        
        return frame, cursor_x, cursor_y, pinch

def main():
    controller = GestureOS()
    cap = cv2.VideoCapture(0)
    
    print("\n🚀 GESTUREOS АКТИВЕН!")
    print("👆 УКАЗАТЕЛЬНЫЙ ПАЛЕЦ = КУРСОР")
    print("✌️  СВЕДЕНИЕ ПАЛЬЦЕВ = КЛИК ПО ИКОНКЕ!")
    print("Q = ВЫХОД")
    print("-" * 50)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Обработка руки
        frame, cursor_x, cursor_y, pinch = controller.process_frame(frame)
        
        # ДВИЖЕНИЕ КУРСОРА
        if cursor_x and cursor_y:
            pyautogui.moveTo(cursor_x, cursor_y)
            
            # КЛИК по pinch (анти-спам 0.3 сек)
            current_time = time.time()
            if pinch and (current_time - controller.last_click > 0.3):
                print("🖱️  КЛИК ПО ИКОНКЕ!")
                pyautogui.click()
                controller.last_click = current_time
        
        # Отладка на экране
        status = "🖱️ PINCH - КЛИК!" if pinch else "👆 Tracking..."
        cv2.putText(frame, status, (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        if cursor_x:
            cv2.putText(frame, f"Cursor: {cursor_x},{cursor_y}", (10, 60),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
        
        cv2.imshow("GestureOS - Рука → Мышь → Клик!", frame)
        
        # Выход
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    print("👋 GestureOS остановлен")

if __name__ == "__main__":
    main()
