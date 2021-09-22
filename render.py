import pygame as pg
from settings import *

def draw(sc, boards):
    area = (H_WIDTH - H_SNAKE_SIZE_PX, H_HEIGHT - H_SNAKE_SIZE_PX,
            SNAKE_SIZE_PX, SNAKE_SIZE_PX)

    sc.fill(WINDOW_BG)

    pg.draw.rect(sc, BLACK, rect=area)

    for board in boards:
        if board.alive:
            pg.draw.circle(sc, APPLE_COLOR,
                           (area[0] + board.apple[0] * SNAKE_SCALE + SNAKE_SCALE / 2, area[1] + board.apple[1] * SNAKE_SCALE + SNAKE_SCALE / 2),
                           radius=SNAKE_SCALE / 2)

    for board in boards:
        if board.alive:
            for snake in board.snake:
                pg.draw.rect(sc, SNAKE_COLOR,
                             rect=(area[0] + snake[0] * SNAKE_SCALE, area[1] + snake[1] * SNAKE_SCALE, SNAKE_SCALE, SNAKE_SCALE))

def text(sc, strings, antialias, color, pos):
    myfont = pg.font.SysFont('Arial', 18)

    for s in strings:
        textsurface = myfont.render(s, antialias, color)
        sc.blit(textsurface, pos)
        pos = pos[0], pos[1] + 20