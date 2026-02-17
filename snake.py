import os
import pygame
import random
import sys

# Classic Snake game using pygame
# Controls: Arrow keys to move, P to pause, Esc to quit

CELL_SIZE = 20
GRID_W = 30
GRID_H = 20
WIDTH = CELL_SIZE * GRID_W
HEIGHT = CELL_SIZE * GRID_H
BASE_FPS = 10
SPEED_STEP = 1
SPEED_EVERY = 4

BLACK = (0, 0, 0)
DARK = (20, 20, 20)
GREEN = (0, 200, 0)
BRIGHT_GREEN = (0, 255, 0)
RED = (220, 50, 50)
WHITE = (245, 245, 245)


def rand_food(snake):
    free_cells = [
        (x, y)
        for x in range(GRID_W)
        for y in range(GRID_H)
        if (x, y) not in snake
    ]
    if not free_cells:
        return None
    return random.choice(free_cells)


def draw_grid(screen):
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, DARK, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, DARK, (0, y), (WIDTH, y))


def load_high_score(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return int(f.read().strip() or 0)
    except (OSError, ValueError):
        return 0


def save_high_score(path, score):
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(str(score))
    except OSError:
        pass


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas", 24)

    high_score_path = os.path.join(os.path.dirname(__file__), "highscore.txt")
    high_score = load_high_score(high_score_path)

    snake = [(GRID_W // 2, GRID_H // 2)]
    direction = (1, 0)
    next_direction = direction
    food = rand_food(snake)
    score = 0
    game_over = False
    paused = False
    won = False
    score_saved = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if score > high_score:
                    save_high_score(high_score_path, score)
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if score > high_score:
                        save_high_score(high_score_path, score)
                    pygame.quit()
                    sys.exit(0)
                if event.key == pygame.K_p and not game_over:
                    paused = not paused
                if event.key == pygame.K_UP and direction != (0, 1):
                    next_direction = (0, -1)
                elif event.key == pygame.K_DOWN and direction != (0, -1):
                    next_direction = (0, 1)
                elif event.key == pygame.K_LEFT and direction != (1, 0):
                    next_direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                    next_direction = (1, 0)
                elif event.key == pygame.K_r and game_over:
                    snake = [(GRID_W // 2, GRID_H // 2)]
                    direction = (1, 0)
                    next_direction = direction
                    food = rand_food(snake)
                    score = 0
                    game_over = False
                    paused = False
                    won = False
                    score_saved = False

        if not game_over and not paused:
            direction = next_direction
            head_x, head_y = snake[0]
            new_head = (head_x + direction[0], head_y + direction[1])
            will_grow = new_head == food

            # Collision with walls
            if (
                new_head[0] < 0
                or new_head[0] >= GRID_W
                or new_head[1] < 0
                or new_head[1] >= GRID_H
            ):
                game_over = True
            # Collision with self
            elif new_head in (snake if will_grow else snake[:-1]):
                game_over = True
            else:
                snake.insert(0, new_head)
                if will_grow:
                    score += 1
                    if score > high_score:
                        high_score = score
                    food = rand_food(snake)
                    if food is None:
                        won = True
                        game_over = True
                else:
                    snake.pop()

        screen.fill(BLACK)
        draw_grid(screen)

        # Draw food
        if food is not None:
            fx, fy = food
            pygame.draw.rect(
                screen,
                RED,
                pygame.Rect(fx * CELL_SIZE, fy * CELL_SIZE, CELL_SIZE, CELL_SIZE),
            )

        # Draw snake
        for i, (sx, sy) in enumerate(snake):
            color = BRIGHT_GREEN if i == 0 else GREEN
            pygame.draw.rect(
                screen,
                color,
                pygame.Rect(sx * CELL_SIZE, sy * CELL_SIZE, CELL_SIZE, CELL_SIZE),
            )

        # Score
        score_text = font.render(f"Score: {score}  Best: {high_score}", True, WHITE)
        screen.blit(score_text, (8, 6))

        if paused:
            msg = font.render("Paused (P to resume)", True, WHITE)
            rect = msg.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(msg, rect)

        if game_over:
            msg_text = "You Win! Press R to restart" if won else "Game Over! Press R to restart"
            msg = font.render(msg_text, True, WHITE)
            rect = msg.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(msg, rect)
            if not score_saved:
                if score > high_score:
                    high_score = score
                save_high_score(high_score_path, high_score)
                score_saved = True

        pygame.display.flip()
        speed_boost = (score // SPEED_EVERY) * SPEED_STEP
        clock.tick(BASE_FPS + speed_boost)


if __name__ == "__main__":
    main()
