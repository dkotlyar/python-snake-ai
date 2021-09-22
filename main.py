import pygame as pg
from settings import *
import render
from board import Board
from brain import Brain
import numpy as np

pg.init()
pg.font.init()
sc = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()

generation = 0
boards = [ Board(Brain()) for i in range(100) ]
gameIter = 0

bestRobot = None

toggleLearnMode = False
learnMode = True
learnGen = None

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
    keys = pg.key.get_pressed()
    if (keys[pg.K_ESCAPE]):
        exit()

    if (keys[pg.K_l] and not toggleLearnMode):
        toggleLearnMode = True
        learnMode = not learnMode
        if learnMode:
            boards = learnGen
        else:
            learnGen = boards
            boards = [Board(bestRobot.brain)]
    elif (not keys[pg.K_l] and toggleLearnMode):
        toggleLearnMode = False

    # if (keys[pg.K_LEFT]):
    #     board.snake_dir = (-1, 0)
    # if (keys[pg.K_RIGHT]):
    #     board.snake_dir = (1, 0)
    # if (keys[pg.K_UP]):
    #     board.snake_dir = (0, -1)
    # if (keys[pg.K_DOWN]):
    #     board.snake_dir = (0, 1)

    gameIter += 1
    if not (gameIter % GAME_SPEED):
        render.draw(sc, boards)
        for board in boards:
            if board.alive:
                board.aliveTime += 1
                board.eatenLastTime += 1
                board.movement()
                board.ai()
                if (board.eatenLastTime > LIVE_WITHOUT_EAT and learnMode):
                    board.alive = False
        gameIter = 0

    bestBoard = None
    for board in boards:
        if bestBoard == None:
            bestBoard = board
        elif bestBoard.score < board.score:
            bestBoard = board

    aliveSnakes = len([board for board in boards if board.alive])
    if not aliveSnakes and learnMode:
        prob = np.array([board.score for board in boards])
        prob = prob / prob.sum()
        moms = np.random.choice(boards, size=len(boards), p=prob)
        dads = np.random.choice(boards, size=len(boards), p=prob)
        boards = [Board(Brain.combine(mom.brain, dad.brain)) for mom, dad in zip(moms, dads)]
        generation += 1
    elif not aliveSnakes and not learnMode:
        boards = [Board(bestRobot.brain)]

    if bestRobot == None or bestRobot.eaten < bestBoard.eaten:
        bestRobot = bestBoard

    render.text(sc, [
        f'Learn mode = %s' % ('yes' if learnMode else 'no'),
        f'Generation = %d' % generation,
        f'Alive snakes = %d' % aliveSnakes,
        f'Apple eaten = %d / %d' % (bestBoard.eaten, bestRobot.eaten),
        f'Score = %d / %d' % (bestBoard.score, bestRobot.score)
    ], True, BLACK, (0, 0))

    pg.display.flip()
    clock.tick(FPS)