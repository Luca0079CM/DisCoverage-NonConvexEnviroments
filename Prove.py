import pygame as pg
import math
# Colors
GRIDSIZE = 20
BLACK = (0, 0, 0)
LIGHTBLACK = (32, 32, 32)
WHITE = (255, 255, 255)
GREY = (160, 160, 160)
LIGHTGREY = (190, 190, 190)
GREEN = (0, 153, 76)

#Window
pg.display.init()
window = pg.display.set_mode((800, 600))
robot_image = pg.image.load("robot1.png")


class Robot(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = robot_image
        self.rect = self.image.get_rect(center=(x, y))
        self.x = x
        self.y = y
        self.delta = 0
        self.vx = 0.25
        self.vy = 0.25

    def update(self):
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.delta = math.atan2(self.y, self.x)
        self.x += self.vx * math.cos(self.delta)
        self.y += self.vy * - math.sin(self.delta)
        self.rect.x, self.rect.y = self.x, self.y


class MapRect(pg.Rect):
    def __init__(self, left, top, width, height, color):
        pg.Rect.__init__(self, (left, top), (width, height))
        self.color = color
        self.found = False


def map_create():
    surface = pg.Surface([window.get_width(), window.get_height()])
    walls = [pg.Rect(0, 0, GRIDSIZE, window.get_height()),  # Lato Sinisto
             pg.Rect(window.get_width() - GRIDSIZE, 0, GRIDSIZE, window.get_height()),  # Lato Destro
             pg.Rect(0, 0, window.get_width(), GRIDSIZE),  # Lato Superiore
             pg.Rect(0, window.get_height() - GRIDSIZE, window.get_width(), GRIDSIZE),  # Lato Inferiore
             pg.Rect(200, window.get_height() - GRIDSIZE - 200, GRIDSIZE, 200),  # Ostacolo 1
             pg.Rect(400, GRIDSIZE, GRIDSIZE, 300),  # Ostacolo 2
             ]

    map = []
    for i in range(0, window.get_width(), GRIDSIZE):
        for j in range(0, window.get_height(), GRIDSIZE):
            r = MapRect(i, j, GRIDSIZE, GRIDSIZE, GREY)
            pg.draw.rect(surface, r.color, r)
            map.append(r)
    return surface, walls, map


def rotate(image, sprite, angle):
    rotated_image = pg.transform.rotozoom(image, angle, 1)
    rotated_rect = rotated_image.get_rect(center=(sprite.x, sprite.y))
    return rotated_image, rotated_rect


def main():
    is_running = True
    robot = Robot(400, 400)
    while is_running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                is_running = False
        robot.x += 0.01
        robot.y += 0.01
        robot.rect = robot.image.get_rect(center=(robot.x, robot.y))
        window.blit(robot.image, robot.rect)
        pg.draw.rect(window, WHITE, robot.rect, 1)
        pg.display.update()


if __name__ == '__main__':
    main()
