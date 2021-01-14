import pygame as pg
import math
from random import *
import Map
import Robot
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
window = pg.display.set_mode((800, 600))
robot_image = pg.image.load("robot1.png")
GRIDSIZE = Map.GRIDSIZE
ROWS = int(window.get_width() / GRIDSIZE)
COLUMNS = int(window.get_height() / GRIDSIZE)

# Delta
pi = math.pi
converter = 180 / pi
standard_delta = [0, pi / 4, pi / 2, pi * 3 / 4, pi, pi * 5 / 4, pi * 3 / 2, pi * 7 / 4]


def main():
    pg.display.set_caption("DisCoverage Exploration")
    icon = pg.image.load("robot1.png")
    pg.display.set_icon(icon)
    is_running = True
    surface, map, n_total_tiles, n_black_tiles = Map.map_create(window)
    print(n_total_tiles)
    print(n_black_tiles)
    # Robots
    robots = [Robot.Robot(1, 1 * 110, window.get_height() - 110),
              Robot.Robot(2, 300, window.get_height() - 310),
              Robot.Robot(3, 600, window.get_height() - 190)
              # Robot.Robot(3, window.get_width() - 40, window.get_height() - 150)
              ]
    start = time.time()
    # Main Loop
    while is_running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                is_running = False

        for m in map:
            for robot in robots:
                if not m.found:
                    if pg.sprite.collide_circle(robot, m):
                        if m.is_obstacle:
                            m.color = BLACK
                        elif m.neighbour_ids:
                            m.color = WHITE
                            robot.white_tiles.append(m)
                        m.found = 1
                    pg.draw.rect(surface, m.color, m.rect)
                if robot.rect.colliderect(m) and m.color == BLACK:
                    seed()
                    rand = randint(0, len(standard_delta) - 1)
                    robot.delta = standard_delta[rand]
        i = 0
        for robot in robots:
            if not robot.empty_frontier:
                robot.update(surface, map)
            else:
                i += 1
        if i == len(robots):
            is_running = False
        # Draw
        window.blit(surface, (0, 0))
        for robot in robots:
            window.blit(robot.image, robot.rect)
        pg.display.update()
    stop = time.time()
    t = stop - start
    print("SUCCESS EXPLORATION")
    print("\nNumero di Robot:", len(robots))
    print("Tempo impiegato:", math.trunc(t/60), " minuti", round(t - math.trunc(t/60) * 60), " secondi")


if __name__ == '__main__':
    main()
