import cv2
import pyautogui
import numpy as np
import time

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.01

def main():
    cap = cv2.VideoCapture(0)
    cursor_history = []
    last_click = 0
    
    print("🚀 GestureOS - ПРОСТАЯ РАБОЧАЯ ВЕРСИЯ")
    print("🖐️ Ладонь = зеленый курсор")
    print("✊ Кулак = красный клик")
    
    while True:
        ret, frame = cap.read()
        if not ret: 
            print("Камера ошибка")
            break
        
        frame = cv2.flip(frame, 1)
        h, w = frame.shape[:2]
        
        # HSV кожи
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_skin = np.array([0, 30, 60])
        upper_skin = np.array([25, 255, 255])
        mask = cv2.inRange(hsv, lower_skin, upper_skin)
        
        kernel = np.ones((7,7), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        hand_center = None
        is_fist = False
        
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 8000:
                M = cv2.moments(contour)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])
                    hand_center = (cx, cy)
                    
                    perimeter = cv2.arcLength(contour, True)
                    compactness = 4 * np.pi * area / (perimeter ** 2)
                    is_fist = compactness > 0.4
                    break
        
        if hand_center:
            cx, cy = hand_center
            screen_x = int(cx / w * pyautogui.size().width)
            screen_y = int(cy / h * pyautogui.size().height)
            
            cursor_history.append((screen_x, screen_y))
            if len(cursor_history) > 5:
                cursor_history.pop(0)
            
            avg_x = int(np.mean([p[0] for p in cursor_history]))
            avg_y = int(np.mean([p[1] for p in cursor_history]))
            pyautogui.moveTo(avg_x, avg_y)
            
            if is_fist:
                current_time = time.time()
                if current_time - last_click > 0.5:
                    print("🖱️ КЛИК!")
                    pyautogui.click()
                    last_click = current_time
                color = (0, 0, 255)  # Красный кулак
            else:
                color = (0, 255, 0)  # Зеленая ладонь
            
            cv2.circle(frame, hand_center, 30, color, 4)
            cv2.circle(frame, hand_center, 15, color, -1)
            
            status = "✊ КУЛАК" if is_fist else "🖐️ ЛАДОНЬ"
        else:
            status = "⏳ Ищем руку..."
        
        cv2.putText(frame, status, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.imshow("GestureOS", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
