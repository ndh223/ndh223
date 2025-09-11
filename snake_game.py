# snake_game.py
import pygame
import sys
import random

# --- Cấu hình ---
CELL_SIZE = 20           # kích thước ô lưới (pixel)
GRID_WIDTH = 40          # số ô ngang
GRID_HEIGHT = 40         # số ô dọc
SCREEN_WIDTH = CELL_SIZE * GRID_WIDTH
SCREEN_HEIGHT = CELL_SIZE * GRID_HEIGHT
FPS = 10                 # tốc độ game (tăng để khó hơn)

# màu sắc (R,G,B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
GRAY = (40, 40, 40)
YELLOW = (200, 200, 0)

# --- Khởi tạo pygame ---
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Rắn săn mồi - Snake (Python + Pygame)")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 30)

# --- Hàm hỗ trợ ---
def draw_rect(pos, color):
    x, y = pos
    rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, color, rect)

def random_food_position(snake):
    while True:
        pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        if pos not in snake:
            return pos

def draw_grid():
    for x in range(0, SCREEN_WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (SCREEN_WIDTH, y))

def show_text(text, pos, color=WHITE):
    img = font.render(text, True, color)
    screen.blit(img, pos)

# --- Khởi tạo game ---
def main():
    # Snake: list of (x,y) positions, head là phần tử đầu
    snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2),
             (GRID_WIDTH // 2 - 1, GRID_HEIGHT // 2),
             (GRID_WIDTH // 2 - 2, GRID_HEIGHT // 2)]
    direction = (1, 0)  # di chuyển sang phải ban đầu
    next_direction = direction
    food = random_food_position(snake)
    score = 0
    game_over = False

    while True:
        # --- Sự kiện ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                # thiết lập hướng (không cho rẽ 180 độ)
                if event.key == pygame.K_UP and direction != (0, 1):
                    next_direction = (0, -1)
                elif event.key == pygame.K_DOWN and direction != (0, -1):
                    next_direction = (0, 1)
                elif event.key == pygame.K_LEFT and direction != (1, 0):
                    next_direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                    next_direction = (1, 0)

        if not game_over:
            direction = next_direction
            head_x, head_y = snake[0]
            dx, dy = direction
            new_head = (head_x + dx, head_y + dy)

            # kiểm tra va chạm với tường
            if (not 0 <= new_head[0] < GRID_WIDTH) or (not 0 <= new_head[1] < GRID_HEIGHT):
                game_over = True

            # kiểm tra va chạm với chính mình
            elif new_head in snake:
                game_over = True
            else:
                snake.insert(0, new_head)  # di chuyển: thêm đầu mới
                # ăn thức ăn?
                if new_head == food:
                    score += 1
                    food = random_food_position(snake)
                    # tăng tốc 1% mỗi lần ăn (tuỳ ý)
                    # FPS = int(FPS * 1.01)  # nếu muốn tăng tốc độ
                else:
                    snake.pop()  # bỏ đuôi nếu không ăn

        # --- Vẽ ---
        screen.fill(BLACK)
        draw_grid()

        # vẽ thức ăn
        draw_rect(food, RED)

        # vẽ rắn (đầu khác màu)
        if snake:
            draw_rect(snake[0], YELLOW)  # đầu
            for segment in snake[1:]:
                draw_rect(segment, GREEN)

        # hiển thị điểm
        show_text(f"Điem: {score}", (10, 10))

        if game_over:
            show_text("Game Over! Nhan R để choi lai hoac Esc de thoat", (10, SCREEN_HEIGHT//2 - 15), color=WHITE)
            # cho phép restart
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                main()  # restart (đơn giản)
                return

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
