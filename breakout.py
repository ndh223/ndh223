import pygame
import sys

# Khoi tao pygame
pygame.init()

# Man hinh
WIDTH, HEIGHT = 600, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Breakout - Đập gạch")

# Mau sac
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE  = (50, 150, 255)
RED   = (200, 50, 50)
GREEN = (50, 200, 50)

# Bien
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# Tham so game
PADDLE_W, PADDLE_H = 100, 15
BALL_SIZE = 12
ROWS, COLS = 10, 12
BRICK_W, BRICK_H = WIDTH // COLS, 15

def create_bricks():
    bricks = []
    for row in range(ROWS):
        for col in range(COLS):
            rect = pygame.Rect(col*BRICK_W, row*BRICK_H + 50, BRICK_W-2, BRICK_H-2)
            bricks.append(rect)
    return bricks

def reset_game():
    paddle = pygame.Rect(WIDTH//2 - PADDLE_W//2, HEIGHT-40, PADDLE_W, PADDLE_H)
    ball = pygame.Rect(WIDTH//2, HEIGHT//2, BALL_SIZE, BALL_SIZE)
    ball_vel = [4, -4]
    bricks = create_bricks()
    score = 0
    game_over = False
    return paddle, ball, ball_vel, bricks, score, game_over

# Khoi tao ban dau
paddle, ball, ball_vel, bricks, score, game_over = reset_game()

running = True
while running:
    screen.fill(BLACK)

    # Xu ly su kien
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_r:
                paddle, ball, ball_vel, bricks, score, game_over = reset_game()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle.left > 0:
        paddle.move_ip(-6, 0)
    if keys[pygame.K_RIGHT] and paddle.right < WIDTH:
        paddle.move_ip(6, 0)

    if not game_over:
        # Cap nhat bong
        ball.x += ball_vel[0]
        ball.y += ball_vel[1]

        # Va cham tuong
        if ball.left <= 0 or ball.right >= WIDTH:
            ball_vel[0] = -ball_vel[0]
        if ball.top <= 0:
            ball_vel[1] = -ball_vel[1]

        # Va cham thanh
        if ball.colliderect(paddle):
            ball_vel[1] = -abs(ball_vel[1])

        # Va cham gạch
        hit_index = ball.collidelist(bricks)
        if hit_index != -1:
            hit_rect = bricks.pop(hit_index)
            score += 1
            ball_vel[1] = -ball_vel[1]

        # Check thua
        if ball.bottom >= HEIGHT:
            game_over = True

    # Ve thanh, bong, gach
    pygame.draw.rect(screen, BLUE, paddle)
    pygame.draw.ellipse(screen, RED, ball)
    for brick in bricks:
        pygame.draw.rect(screen, GREEN, brick)

    # Hien thi diem
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    if game_over:
        gameover_text = font.render("GAME OVER! Nhan R de choi, Esc de thoat", True, RED)
        rect = gameover_text.get_rect(center=(WIDTH//2, HEIGHT//2))
        screen.blit(gameover_text, rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
