import pygame as pg
import math
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


def main():
    pg.display.set_caption("Non-Convex Exploration")
    icon = pg.image.load("robot1.png")
    pg.display.set_icon(icon)
    is_running = True
    surface, map, n_total_tiles = Map.map_create(window)
    # Robots
    robots = [Robot.Robot(1, 1 * 110, window.get_height() - 110, BLACK),
              Robot.Robot(2, 300, window.get_height() - 310, GREEN),
              Robot.Robot(3, 600, window.get_height() - 190, RED)
              # Robot.Robot(3, window.get_width() - 40, 130, RED)
              ]
    start = time.time()
    l = 0
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
        for robot in robots:
            if not robot.empty_frontier:
                robot.update(surface, map)
            else:
                if not robot.disabled:
                    l += 1
                    for i in range(1, len(robot.target_vector)):
                        pg.draw.line(surface, robot.line_color, robot.target_vector[i], robot.target_vector[i - 1], 2)
                    print(l)
                    robot.deactivate()

        if l == len(robots):
            stop = time.time()
            t = stop - start
            print("SUCCESS EXPLORATION")
            print("\nNumero di Robot:", len(robots))
            print("Tempo impiegato:", math.trunc(t / 60), " minuti", round(t - math.trunc(t / 60) * 60), " secondi")
            l = 0 
        # Draw
        window.blit(surface, (0, 0))
        for robot in robots:
            window.blit(robot.image, robot.rect)
        pg.display.update()


if __name__ == '__main__':
    main()
