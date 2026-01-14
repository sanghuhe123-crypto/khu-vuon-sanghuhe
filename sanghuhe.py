import pygame
import math
import random

# Khởi tạo
pygame.init()

# Cấu hình màn hình
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)

# Màu sắc
GRASS_GREEN = (100, 200, 100) # Cỏ xanh
SOIL_BROWN = (139, 69, 19)   # Đất nâu gieo hạt
DARK_BROWN = (80, 40, 20)    # Hạt giống
FLOWER_YELLOW = (255, 255, 0)
PLAYER_COLOR = (255, 100, 100)
WHITE = (255, 255, 255)

# 1. Cấu hình Khu đất gieo hạt (Mảnh vườn nhỏ màu nâu)
# Đặt mảnh vườn ở giữa màn hình
garden_w, garden_h = 400, 300
garden_x = (WIDTH - garden_w) // 2
garden_y = (HEIGHT - garden_h) // 2
garden_rect = pygame.Rect(garden_x, garden_y, garden_w, garden_h)

# Cấu hình nhân vật
char_x, char_y = WIDTH // 2, HEIGHT // 2
char_radius = 35
char_speed = 8

# Danh sách hạt giống
seeds_list = []

# Cấu hình Joystick
joy_base_pos = (200, HEIGHT * 3 // 4) 
joy_base_radius = 90               
joy_stick_pos = list(joy_base_pos)  
is_dragging = False                 

# Cấu hình Nút Gieo Hạt
plant_btn_pos = (WIDTH - 200, HEIGHT * 3 // 4)
plant_btn_radius = 80

font = pygame.font.SysFont("Arial", 40, bold=True)
running = True
clock = pygame.time.Clock()

while running:
    # Vẽ nền cỏ xanh
    screen.fill(GRASS_GREEN)
    
    # 2. Vẽ khu vườn nhỏ màu nâu (Mảnh đất gieo hạt)
    pygame.draw.rect(screen, SOIL_BROWN, garden_rect, border_radius=15)
    # Vẽ thêm một vài chi tiết cho đất nhìn thật hơn
    pygame.draw.rect(screen, (100, 50, 10), garden_rect, 5, border_radius=15)

    # Xử lý sự kiện
    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()[0]
    
    click_event = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            click_event = True

    # 3. Logic Joystick & Di chuyển
    dist_joy = math.hypot(mouse_pos[0] - joy_base_pos[0], mouse_pos[1] - joy_base_pos[1])
    if mouse_pressed:
        if dist_joy < joy_base_radius or is_dragging:
            is_dragging = True
            angle = math.atan2(mouse_pos[1] - joy_base_pos[1], mouse_pos[0] - joy_base_pos[0])
            limit_dist = min(dist_joy, joy_base_radius)
            joy_stick_pos[0] = joy_base_pos[0] + limit_dist * math.cos(angle)
            joy_stick_pos[1] = joy_base_pos[1] + limit_dist * math.sin(angle)
            
            dx = (joy_stick_pos[0] - joy_base_pos[0]) / joy_base_radius
            dy = (joy_stick_pos[1] - joy_base_pos[1]) / joy_base_radius
            char_x += dx * char_speed
            char_y += dy * char_speed
    else:
        is_dragging = False
        joy_stick_pos = list(joy_base_pos)

    # 4. Logic Kiểm tra vị trí và Gieo hạt
    # Kiểm tra xem nhân vật có nằm trong khu đất màu nâu không
    is_in_garden = garden_rect.collidepoint(char_x, char_y)
    
    # Màu nút bấm sẽ sáng lên nếu đang đứng trong vườn
    current_btn_color = (50, 200, 50) if is_in_garden else (100, 100, 100)

    dist_to_btn = math.hypot(mouse_pos[0] - plant_btn_pos[0], mouse_pos[1] - plant_btn_pos[1])
    if click_event and dist_to_btn < plant_btn_radius:
        if is_in_garden:
            # Chỉ cho phép gieo nếu đang đứng trong vườn màu nâu
            seeds_list.append([char_x, char_y, 0])
        else:
            # Nếu ngoài vườn, có thể in thông báo hoặc làm gì đó (tùy bạn)
            print("Bạn phải vào mảnh vườn màu nâu để gieo hạt!")

    # Giới hạn nhân vật
    char_x = max(char_radius, min(WIDTH - char_radius, char_x))
    char_y = max(char_radius, min(HEIGHT - char_radius, char_y))

    # 5. Vẽ hạt giống và hoa
    for s in seeds_list:
        s[2] += 1
        if s[2] < 120:
            pygame.draw.circle(screen, DARK_BROWN, (int(s[0]), int(s[1])), 8)
        else:
            # Vẽ hoa đơn giản
            pygame.draw.rect(screen, (50, 150, 50), (s[0]-4, s[1], 8, 15)) # Cành
            pygame.draw.circle(screen, FLOWER_YELLOW, (int(s[0]), int(s[1]-10)), 15)

    # 6. Vẽ Giao diện (UI)
    # Vẽ Nút Gieo
    pygame.draw.circle(screen, current_btn_color, plant_btn_pos, plant_btn_radius)
    btn_text = font.render("GIEO", True, WHITE)
    screen.blit(btn_text, (plant_btn_pos[0]-45, plant_btn_pos[1]-20))
    
    # Vẽ Joystick
    pygame.draw.circle(screen, (150, 150, 150), joy_base_pos, joy_base_radius, 4)
    pygame.draw.circle(screen, (80, 80, 80), joy_stick_pos, 45)
    
    # Vẽ Nhân vật
    pygame.draw.circle(screen, PLAYER_COLOR, (int(char_x), int(char_y)), char_radius)
    
    # Thông báo cho người chơi
    if not is_in_garden:
        status_txt = font.render("Hay di vao khu dat nau!", True, (255, 50, 50))
        screen.blit(status_txt, (WIDTH//2 - 150, 50))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
