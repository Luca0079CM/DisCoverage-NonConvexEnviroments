import pygame as pg
import math
import numpy as np
from random import *
import time
# Colors
GRIDSIZE = 20
BLACK = (0, 0, 0)
LIGHTBLACK = (32, 32, 32)
WHITE = (255, 255, 255)
DARKWHITE = (224, 224, 224)
GREY = (160, 160, 160)
LIGHTGREY = (190, 190, 190)
GREEN = (0, 153, 76)
RED = (255, 0, 0)
BLUE = (0, 128, 255)

# Window
pg.display.init()
window = pg.display.set_mode((800, 600))
robot_image = pg.image.load("robot1.png")
# Speed
v = 0.1
# Delta
pi = math.pi
converter = 180/pi
standard_delta = [0, pi/4, pi/2, pi*3/4, pi, pi*5/4, pi*3/2, pi*7/4]


class Robot(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = robot_image
        self.x = x
        self.y = y
        self.radius = 35
        self.rect = self.image.get_rect(center=(x, y))
        self.delta = standard_delta[7]
        self.reachable_matrix = np.zeros([int(window.get_width() / GRIDSIZE), int(window.get_height() / GRIDSIZE)])

    def update(self, matrix):

        dx = -math.cos(self.delta - (math.pi / 2)) * v
        dy = math.sin(self.delta - (math.pi / 2)) * v
        self.x += dx
        self.y += dy
        self.rect = self.image.get_rect(center=(self.x, self.y))


class MapRect(pg.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.rect = pg.Rect((x, y), (GRIDSIZE, GRIDSIZE))
        self.color = color
        self.found = 0
        self.is_obstacle = False


def map_create():
    surface = pg.Surface([window.get_width(), window.get_height()])

    map = []
    for i in range(0, window.get_width(), GRIDSIZE):
        for j in range(0, window.get_height(), GRIDSIZE):
            if ((i + j)/GRIDSIZE) % 2 == 0:
                r = MapRect(i, j, GREY)
            else:
                r = MapRect(i, j, LIGHTGREY)
            if i == 0 or i == window.get_width() - GRIDSIZE or j == 0 or j == window.get_height() - GRIDSIZE:
                r.is_obstacle = True
            pg.draw.rect(surface, r.color, r.rect)
            map.append(r)

    # Ostacolo 1
    i = GRIDSIZE * 20
    for j in range(400, window.get_height(), GRIDSIZE):
        for m in map:
            if m.rect.x == i and m.rect.y == j:
                m.is_obstacle = True

    # Ostacolo 2
    j = GRIDSIZE * 10
    for i in range(400, window.get_width(), GRIDSIZE):
        for m in map:
            if m.rect.x == i and m.rect.y == j:
                m.is_obstacle = True

    return surface, map


def rotate(image, x, y, angle):
    angle = angle * converter
    rotated_image = pg.transform.rotozoom(image, angle, 1)
    rotated_rect = rotated_image.get_rect(center=(x, y))
    return rotated_image, rotated_rect


def main():
    pg.display.set_caption("DisCoverage Exploration")
    icon = pg.image.load("robot1.png")
    pg.display.set_icon(icon)
    is_running = True
    surface, map = map_create()
    matrix = np.zeros([int(window.get_width() / GRIDSIZE), int(window.get_height() / GRIDSIZE)])

    # Robots
    robot = Robot(110, window.get_height() - 110)

    # Set Matrix
    for m in map:
        if m.color == BLACK:
            matrix[int(m.rect.x / GRIDSIZE)][int(m.rect.y / GRIDSIZE)] = 1
        if math.dist(robot.rect.center, m.rect.center) < 45:
            angle = robot.delta + math.atan2(m.rect.center[1] - robot.rect.center[1],
                                             m.rect.center[0] - robot.rect.center[0])
            if round(math.sin(angle), 2) <= 0:
                robot.reachable_matrix[int(m.rect.x / GRIDSIZE)][int(m.rect.y / GRIDSIZE)] = 1

    # Main Loop
    while is_running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                is_running = False
            elif event.type == pg.KEYDOWN:
                seed()
                rand = randint(0, len(standard_delta) - 1)
                robot.delta = standard_delta[rand]

        for m in map:
            if not m.found:
                if pg.sprite.collide_circle(robot, m):
                    if m.is_obstacle:
                        m.color = BLACK
                    else:
                        m.color = WHITE
                        matrix[int(m.rect.x / GRIDSIZE)][int(m.rect.y / GRIDSIZE)] = 1
                    m.found = 1
                    pg.draw.rect(surface, m.color, m.rect)
            if robot.rect.colliderect(m) and m.color == BLACK:
                seed()
                rand = randint(0, len(standard_delta) - 1)
                robot.delta = standard_delta[rand]
            if m.color is not BLACK and math.dist(robot.rect.center, m.rect.center) < 45:
                angle = robot.delta + math.atan2(m.rect.center[1] - robot.rect.center[1],
                                                 m.rect.center[0] - robot.rect.center[0])
                if round(math.sin(angle), 2) <= 0:
                    robot.reachable_matrix[int(m.rect.x / GRIDSIZE)][int(m.rect.y / GRIDSIZE)] = 1

        for i in range(0, int(window.get_width() / GRIDSIZE)):
            for j in range(0, int(window.get_height() / GRIDSIZE)):
                if robot.reachable_matrix[i][j] == 1:
                    pg.draw.circle(surface, RED, ((i*GRIDSIZE)+GRIDSIZE/2, (j*GRIDSIZE)+GRIDSIZE/2), 2)
        robot.update(matrix)
        # Draw
        x, y = robot.rect.center
        robot.image, robot.rect = rotate(robot_image, x, y, robot.delta)
        window.blit(surface, (0, 0))
        window.blit(robot.image, robot.rect)
        pg.display.update()

        # time.sleep(10)


if __name__ == '__main__':
    main()
