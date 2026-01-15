import pygame
import sys

# Инициализация с проверкой ошибок
pygame.init()
try:
    screen = pygame.display.set_mode((1024, 768))
    pygame.display.set_caption("GestureOS v0.1 - НАЖМИ СТРЕЛКИ!")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    print("✅ GestureOS: окно создано! Управление: СТРЕЛКИ + ПРОБЕЛ")
except Exception as e:
    print(f"❌ Ошибка pygame: {e}")
    sys.exit(1)

text_input = ""
cursor_pos = [150, 150]
keys = [
    {"text": "Q", "x": 100, "y": 500},
    {"text": "W", "x": 160, "y": 500},
    {"text": "E", "x": 220, "y": 500},
]

running = True
frame_count = 0

while running:
    frame_count += 1
    
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    
    # Управление курсором (стрелки)
    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[pygame.K_LEFT]:   cursor_pos[0] = max(0, cursor_pos[0] - 5)
    if keys_pressed[pygame.K_RIGHT]:  cursor_pos[0] = min(1000, cursor_pos[0] + 5)
    if keys_pressed[pygame.K_UP]:     cursor_pos[1] = max(0, cursor_pos[1] - 5)
    if keys_pressed[pygame.K_DOWN]:   cursor_pos[1] = min(700, cursor_pos[1] + 5)
    
    # Ввод текста (SPACE над клавишей)
    if keys_pressed[pygame.K_SPACE]:
        for key in keys:
            dist = ((cursor_pos[0] - key["x"])**2 + (cursor_pos[1] - key["y"])**2)**0.5
            if dist < 35:
                text_input += key["text"]
                pygame.time.wait(200)  # Анти-спам
    
    # ОТРИСОВКА — ВАЖНО: каждый кадр!
    screen.fill((20, 20, 40))  # Темно-синий фон
    
    # Текст инструкций
    instr = font.render("СТРЕЛКИ = курсор | ПРОБЕЛ = ввод | ESC = выход", True, (100, 255, 100))
    screen.blit(instr, (10, 10))
    
    # Поле ввода
    pygame.draw.rect(screen, (100, 150, 255), (50, 60, 600, 60))
    text_surf = font.render(text_input, True, (255, 255, 255))
    screen.blit(text_surf, (70, 75))
    
    # Зеленый курсор
    pygame.draw.circle(screen, (0, 255, 0), (int(cursor_pos[0]), int(cursor_pos[1])), 15)
    pygame.draw.circle(screen, (255, 255, 0), (int(cursor_pos[0]), int(cursor_pos[1])), 15, 3)
    
    # Клавиши с подсветкой
    for key in keys:
        dist = ((cursor_pos[0] - key["x"])**2 + (cursor_pos[1] - key["y"])**2)**0.5
        color = (100, 200, 255) if dist < 35 else (60, 60, 80)
        pygame.draw.rect(screen, color, (key["x"]-25, key["y"]-25, 50, 50))
        pygame.draw.rect(screen, (255,255,255), (key["x"]-25, key["y"]-25, 50, 50), 2)
        text_surf = font.render(key["text"], True, (255, 255, 255))
        screen.blit(text_surf, (key["x"]-12, key["y"]-18))
    
    # FPS счётчик (отладка)
    fps_text = font.render(f"FPS: {int(clock.get_fps())}", True, (100, 100, 255))
    screen.blit(fps_text, (10, 740))
    
    # 🔥 ГЛАВНОЕ: ОБНОВИТЬ ЭКРАН КАЖДЫЙ КАДР!
    pygame.display.flip()
    clock.tick(60)

print("👋 GestureOS завершен")
pygame.quit()
sys.exit()
