import cv2
from hand_controller import HandController
import pyautogui

def main():
    cap = cv2.VideoCapture(0)
    controller = HandController()
    
    print("🚀 GestureOS v1.0")
    print("👆 Указательный палец = курсор")
    print("✌️  Pinch (сведение пальцев) = КЛИК")
    print("Q = выход")
    
    while True:
        ret, frame = cap.read()
        if not ret: break
        
        frame, cursor_x, cursor_y, pinch = controller.process_frame(frame)
        
        # ДВИГАЕМ КУРСОР
        if cursor_x and cursor_y:
            pyautogui.moveTo(cursor_x, cursor_y)
            
            # PINCH = КЛИК!
            if pinch:
                print("🖱️  КЛИК!")
                pyautogui.click()
                time.sleep(0.2)  # Анти-спам
        
        # Информация на экране
        status = "PINCH 🖱️" if pinch else "Tracking 👆"
        cv2.putText(frame, status, (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
        
        if cursor_x:
            cv2.circle(frame, (int(index_tip.x*640), int(index_tip.y*480)), 10, (0,0,255), -1)
        
        cv2.imshow("GestureOS - Hand → Mouse", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
