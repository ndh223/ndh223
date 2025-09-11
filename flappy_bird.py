import pygame
import random
import sys

# Khoi tao pygame
pygame.init()

# Man hinh
WIDTH, HEIGHT = 500, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird Mini")

# Mau sac
BLUE  = (50, 150, 255)
GREEN = (50, 200, 50)
RED   = (200, 50, 50)
BLACK = (0, 0, 0)

# Chim
bird_x = 50
bird_y = HEIGHT // 2
bird_radius = 15
bird_vel = 0
gravity = 0.5
jump_strength = -8

# Ong
pipe_width = 60
pipe_gap = 150
pipe_vel = -3
pipes = []

# Diem
score = 0
font = pygame.font.SysFont(None, 36)

# Trang thai
game_over = False

clock = pygame.time.Clock()

def draw_text_center(text, y, color=BLACK):
    img = font.render(text, True, color)
    rect = img.get_rect(center=(WIDTH//2, y))
    screen.blit(img, rect)

def create_pipe():
    gap_y = random.randint(100, HEIGHT - 200)
    top_rect = pygame.Rect(WIDTH, 0, pipe_width, gap_y)
    bottom_rect = pygame.Rect(WIDTH, gap_y + pipe_gap, pipe_width, HEIGHT)
    return [top_rect, bottom_rect, False]  # False = chua tinh diem

def reset_game():
    global bird_y, bird_vel, pipes, score, game_over
    bird_y = HEIGHT // 2
    bird_vel = 0
    pipes = [create_pipe()]
    score = 0
    game_over = False

# Tao ong ban dau
pipes.append(create_pipe())

running = True
while running:
    screen.fill(BLUE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                bird_vel = jump_strength
            if event.key == pygame.K_r:
                reset_game()
            if event.key == pygame.K_ESCAPE:
                running = False

    if not game_over:
        # Cap nhat chim
        bird_vel += gravity
        bird_y += bird_vel

        # Ve chim
        pygame.draw.circle(screen, RED, (bird_x, int(bird_y)), bird_radius)

        # Cap nhat ong
        for pipe in pipes:
            top_rect, bottom_rect, passed = pipe
            top_rect.x += pipe_vel
            bottom_rect.x += pipe_vel

            pygame.draw.rect(screen, GREEN, top_rect)
            pygame.draw.rect(screen, GREEN, bottom_rect)

            # Kiem tra va cham
            bird_rect = pygame.Rect(bird_x - bird_radius, bird_y - bird_radius,
                                    bird_radius*2, bird_radius*2)
            if bird_rect.colliderect(top_rect) or bird_rect.colliderect(bottom_rect):
                game_over = True

            # Tinh diem khi chim qua ong
            if not pipe[2] and top_rect.x + pipe_width < bird_x:
                score += 1
                pipe[2] = True   # Danh dau la da tinh diem

        # Xoa ong cu va tao ong moi
        if pipes[-1][0].x < WIDTH - 200:
            pipes.append(create_pipe())
        if pipes[0][0].x < -pipe_width:
            pipes.pop(0)

        # Kiem tra roi xuong dat
        if bird_y > HEIGHT - bird_radius:
            game_over = True

    else:
        # Ve chim dung yen
        pygame.draw.circle(screen, RED, (bird_x, int(bird_y)), bird_radius)

        # Ve lai ong dung yen
        for top_rect, bottom_rect, _ in pipes:
            pygame.draw.rect(screen, GREEN, top_rect)
            pygame.draw.rect(screen, GREEN, bottom_rect)

        # Thong bao game over
        draw_text_center("GAME OVER!", HEIGHT//2 - 40, RED)
        draw_text_center("Nhan R de choi lai", HEIGHT//2, BLACK)
        draw_text_center("Nhan Esc de thoat", HEIGHT//2 + 40, BLACK)

    # Hien thi diem
    draw_text_center(f"Diem: {score}", 40, BLACK)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
