import pygame
import sys
import random

# Khởi tạo
pygame.init()
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Steal An Egg - Mini")
clock = pygame.time.Clock()

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (50, 200, 50)
YELLOW = (255, 220, 50)
RED = (220, 50, 50)
BLUE = (50, 120, 255)
BROWN = (160, 100, 40)

# Nhân vật
player_size = 40
player_x = WIDTH // 2
player_y = HEIGHT // 2
player_speed = 5

# Trứng
eggs = []
for _ in range(8):
    eggs.append({
        "x": random.randint(50, WIDTH - 50),
        "y": random.randint(50, HEIGHT - 50),
        "collected": False
    })

# Điểm
score = 0
font = pygame.font.SysFont("arial", 30)

# Vòng lặp game
running = True
while running:
    clock.tick(60)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Điều khiển nhân vật
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        player_y -= player_speed
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        player_y += player_speed
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        player_x += player_speed

    # Giới hạn trong màn hình
    player_x = max(0, min(WIDTH - player_size, player_x))
    player_y = max(0, min(HEIGHT - player_size, player_y))

    # Kiểm tra nhặt trứng
    player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
    for egg in eggs:
        if not egg["collected"]:
            egg_rect = pygame.Rect(egg["x"], egg["y"], 25, 30)
            if player_rect.colliderect(egg_rect):
                egg["collected"] = True
                score += 1

    # Vẽ
    screen.fill((180, 230, 255))  # nền trời

    # Vẽ đất
    pygame.draw.rect(screen, GREEN, (0, HEIGHT - 80, WIDTH, 80))

    # Vẽ trứng
    for egg in eggs:
        if not egg["collected"]:
            pygame.draw.ellipse(screen, BROWN, (egg["x"], egg["y"], 25, 30))
            pygame.draw.ellipse(screen, YELLOW, (egg["x"] + 5, egg["y"] + 5, 15, 18))

    # Vẽ nhân vật
    pygame.draw.rect(screen, BLUE, (player_x, player_y, player_size, player_size))
    # đầu
    pygame.draw.circle(screen, (255, 200, 150), (player_x + 20, player_y - 10), 15)

    # Điểm số
    score_text = font.render(f"Trứng đã cướp: {score}", True, BLACK)
    screen.blit(score_text, (20, 20))

    instruction = font.render("Dùng WASD hoặc phím mũi tên để di chuyển", True, BLACK)
    screen.blit(instruction, (20, 60))

    pygame.display.flip()

pygame.quit()
sys.exit()
