import cv2
import pyautogui
import numpy as np
import time

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.01

def detect_finger_tip(frame):
    """Простое распознавание кончика пальца (OpenCV contours)"""
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Желто-оранжевый диапазон кожи
    lower_skin = np.array([0, 20, 70])
    upper_skin = np.array([20, 255, 255])
    mask = cv2.inRange(hsv, lower_skin, upper_skin)
    
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if contours:
        # Самый большой контур
        largest_contour = max(contours, key=cv2.contourArea)
        if cv2.contourArea(largest_contour) > 1000:
            M = cv2.moments(largest_contour)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                return cx, cy
    return None, None

def main():
    cap = cv2.VideoCapture(0)
    cursor_history = []
    last_click = 0
    
    print("🚀 Simple GestureOS (OpenCV)")
    print("👆 Покажите КИСТЬ на камеру")
    print("🖱️  Центр кисти = курсор")
    print("✌️  Сжать кулак = КЛИК")
    
    while True:
        ret, frame = cap.read()
        if not ret: break
        
        # Флип для зеркала
        frame = cv2.flip(frame, 1)
        
        # Поиск кончика пальца
        finger_x, finger_y = detect_finger_tip(frame)
        
        if finger_x:
            h, w = frame.shape[:2]
            # Нормализация к экрану
            screen_x = int(finger_x / w * pyautogui.size().width)
            screen_y = int(finger_y / h * pyautogui.size().height)
            
            # Сглаживание
            cursor_history.append((screen_x, screen_y))
            if len(cursor_history) > 10:
                cursor_history.pop(0)
            
            avg_x = int(np.mean([p[0] for p in cursor_history]))
            avg_y = int(np.mean([p[1] for p in cursor_history]))
            
            pyautogui.moveTo(avg_x, avg_y)
            
            # Детекция "сжатого кулака" (маленькая площадь)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV)
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            click = False
            if contours:
                largest = max(contours, key=cv2.contourArea)
                if cv2.contourArea(largest) < 5000:  # Маленькая площадь = кулак
                    click = True
            
            # Клик с анти-спамом
            current_time = time.time()
            if click and (current_time - last_click > 0.5):
                print("🖱️  КЛИК!")
                pyautogui.click()
                last_click = current_time
            
            # Визуализация
            cv2.circle(frame, (finger_x, finger_y), 15, (0, 255, 0), -1)
            cv2.putText(frame, f"Cursor: {avg_x},{avg_y}", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        
        status = "🖱️ КЛИК" if click else "👆 Tracking"
        cv2.putText(frame, status, (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.imshow("Simple GestureOS", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
