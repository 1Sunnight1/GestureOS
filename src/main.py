import pygame
import sys
import os

# Инициализация Pygame
pygame.init()
screen = pygame.display.set_mode((1024, 768))
pygame.display.set_caption("GestureOS v0.1 - Hand Tracking Keyboard")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# Поле ввода текста
text_input = ""
cursor_pos = [150, 150]

# Виртуальные клавиши (пример)
keys = [
    {"text": "Q", "x": 100, "y": 500},
    {"text": "W", "x": 160, "y": 500},
    {"text": "E", "x": 220, "y": 500},
]

print("🚀 GestureOS запущен! ESC для выхода")
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    
    # Имитация курсора мыши (позже заменим на руку)
    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[pygame.K_LEFT]:  cursor_pos[0] -= 5
    if keys_pressed[pygame.K_RIGHT]: cursor_pos[0] += 5
    if keys_pressed[pygame.K_UP]:    cursor_pos[1] -= 5
    if keys_pressed[pygame.K_DOWN]:  cursor_pos[1] += 5
    
    # Проверка нажатия клавиш (SPACE = ввод)
    if keys_pressed[pygame.K_SPACE]:
        for key in keys:
            if (abs(cursor_pos[0] - key["x"]) < 30 and 
                abs(cursor_pos[1] - key["y"]) < 30):
                text_input += key["text"]
    
    # Отрисовка
    screen.fill((20, 20, 40))  # Темный фон
    
    # Курсор (зеленый круг)
    pygame.draw.circle(screen, (0, 255, 0), cursor_pos, 15)
    
    # Клавиши
    for key in keys:
        # Подсветка при наведении
        distance = ((cursor_pos[0] - key["x"])**2 + (cursor_pos[1] - key["y"])**2)**0.5
        color = (100, 200, 255) if distance < 30 else (80, 80, 80)
        pygame.draw.rect(screen, color, (key["x"]-25, key["y"]-25, 50, 50))
        text_surf = font.render(key["text"], True, (255, 255, 255))
        screen.blit(text_surf, (key["x"]-10, key["y"]-12))
    
    # Поле ввода
    pygame.draw.rect(screen, (100, 150, 255), (50, 50, 600, 60))
    text_surf = font.render(text_input, True, (255, 255, 255))
    screen.blit(text_surf, (70, 65))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
