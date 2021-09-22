from settings import *
import numpy as np

class Board:
    def __init__(self, brain):
        snake_dir = [
            (0, 1),
            (0, -1),
            (1, 0),
            (-1, 0)
        ][np.random.randint(0, 4)]
        randPoint = tuple(np.random.randint(4, SNAKE_SIZE - 4, size=(2,)))

        self.snake = [
            (randPoint[0] - snake_dir[0] * i, randPoint[1] - snake_dir[1] * i) for i in range(4)
        ]
        self.snake_dir = snake_dir
        self.alive = True
        self.eaten = 0
        self.aliveTime = 0
        self.eatenLastTime = 0

        self.apple = tuple(np.random.randint(0, SNAKE_SIZE, size=(2,)))

        self.brain = brain

    def movement(self):
        if (not self.alive):
            return

        nextPos = self.nextPos(self.snake[0], self.snake_dir)
        wall, snake, apple = self.detectIntersection(nextPos)
        if (wall or snake):
            self.alive = False
        elif apple:
            self.eaten += 1
            self.eatenLastTime = 0
            self.apple = tuple(np.random.randint(0, SNAKE_SIZE, size=(2,)))
            self.snake = [nextPos] + self.snake
        elif (self.alive):
            self.snake = [nextPos] + self.snake[:-1]

    @property
    def score(self):
        return self.aliveTime * 2 ** min(self.eaten, 10) * (max(self.eaten, 10) - 9)

    def ai(self):
        see = np.array(self.see()).flatten()
        predict = self.brain.predict(see)
        self.snake_dir = predict @ np.array(self.snake_dir)

    def nextPos(self, head, dir):
        return head[0] + dir[0], head[1] + dir[1]

    def detectIntersection(self, nextPos):
        wall, snake, apple = False, False, False
        if (nextPos[0] < 0 or nextPos[0] >= SNAKE_SIZE):
            wall = True
        elif (nextPos[1] < 0 or nextPos[1] >= SNAKE_SIZE):
            wall = True
        elif (nextPos in self.snake):
            snake = True
        elif nextPos == self.apple:
            apple = True

        return wall, snake, apple

    def see(self):
        snakeHead = self.snake[0]

        forward = np.array(self.snake_dir)
        backward = np.array([[-1, 0], [0, -1]]) @ forward
        right = np.array([[0, -1], [1, 0]]) @ forward
        left = np.array([[0, 1], [-1, 0]]) @ forward
        # forward_right = forward + right
        # forward_left = forward + left
        # backward_right = backward + right
        # backward_left = backward + left

        fwd = self.getDistances(snakeHead, forward)
        bwd = self.getDistances(snakeHead, backward)
        rght = self.getDistances(snakeHead, right)
        lft = self.getDistances(snakeHead, left)
        # fr = self.getDistances(snakeHead, forward_right)
        # fl = self.getDistances(snakeHead, forward_left)
        # br = self.getDistances(snakeHead, backward_right)
        # bl = self.getDistances(snakeHead, backward_left)

        mdir = np.array([[forward[0] + forward[1], 0], [0, forward[1] + forward[0]]])
        appleSensor = np.array(self.apple) - np.array(snakeHead)
        appleSensor = mdir @ appleSensor
        appleSensor = appleSensor / (np.absolute(appleSensor).sum() + 1e-7)

        # return (fwd, bwd, rght, lft, fr, fl, br, bl)
        return fwd, bwd, rght, lft, appleSensor

    def getDistances(self, head, dir):
        next = head
        wall_dist, snake_dist, apple_dist = 0, 0, 0
        for i in range(SNAKE_SIZE):
            if (wall_dist == 0 and snake_dist == 0 and apple_dist == 0):
                next = self.nextPos(next, dir)
                wall, snake, apple = self.detectIntersection(next)
                wall_dist = 1 / (i + 1) if wall else 0
                snake_dist = 1 / (i + 1) if snake else 0
                # apple_dist = 1 / (i + 1) if apple else 0
        return wall_dist, snake_dist