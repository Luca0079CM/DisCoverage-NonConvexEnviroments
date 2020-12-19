import pygame as pg
import math
import numpy as np
from random import *
import time
# Colors
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
window = pg.display.set_mode((600, 600))
robot_image = pg.image.load("robot1.png")
GRIDSIZE = 20
ROWS = int(window.get_width() / GRIDSIZE)
COLUMNS = int(window.get_height() / GRIDSIZE)
# Speed
v = 0
# Delta
pi = math.pi
converter = 180/pi
standard_delta = [0, pi/4, pi/2, pi*3/4, pi, pi*5/4, pi*3/2, pi*7/4]


def expand_matrix(matrix):
    indexes = []
    for i in range(0, ROWS):
        for j in range(0, COLUMNS):
            if matrix[i][j] == 1:
                ind = [i, j]
                indexes.append(ind)
    for i in range(0, len(indexes)):
        ind = indexes[i]
        matrix[ind[0] - 1][ind[1] - 1] = 1
        matrix[ind[0] - 1][ind[1]] = 1
        matrix[ind[0] - 1][ind[1] + 1] = 1
        matrix[ind[0]][ind[1] - 1] = 1
        matrix[ind[0]][ind[1] + 1] = 1
        matrix[ind[0] + 1][ind[1] - 1] = 1
        matrix[ind[0] + 1][ind[1]] = 1
        matrix[ind[0] + 1][ind[1] + 1] = 1


def calc_matrix(reachable, matrix):
    equal = False
    while not equal:
        expand_matrix(reachable)
        tmp = np.dot(reachable, matrix)
        if np.array_equal(reachable, matrix):
            equal = True
        else:
            reachable = tmp


class Robot(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = robot_image
        self.x = x
        self.y = y
        self.radius = 35
        self.rect = self.image.get_rect(center=(x, y))
        self.delta = standard_delta[0]
        self.reachable_matrix = np.zeros([ROWS, COLUMNS])

    def update(self, matrix):
        x = 0
        #calc_matrix(self.reachable_matrix, matrix)

    def move(self):
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
        self.id = [int(x/GRIDSIZE), int(y/GRIDSIZE)]


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
    x = 0
    y = 0
    for i in range(0, 100):
        x += 1
        if x == 30:
            break
        y += 1
    print(x)
    print(y)


if __name__ == '__main__':
    main()
