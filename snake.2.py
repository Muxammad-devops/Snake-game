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

    