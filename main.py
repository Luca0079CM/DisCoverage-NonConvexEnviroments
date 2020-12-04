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
circle_image = pg.image.load("circle.png").convert_alpha()
pg.transform.scale(circle_image, (1, 1))
#Speed
v = 0.5


class Robot(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = robot_image
        self.rect = self.image.get_rect(center=(x, y))
        self.x = x
        self.y = y
        self.delta = 0
        self.radius = 50

    def update(self):
        mx, my = pg.mouse.get_pos()
        self.delta = math.atan2(self.x - mx, self.y - my)
        self.x += v * math.cos(self.delta)
        self.y += v * - math.sin(self.delta)
        self.rect.x, self.rect.y = self.x, self.y


class MapRect(pg.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.rect = pg.Rect((x, y), (GRIDSIZE, GRIDSIZE))
        self.color = color
        self.found = False
        self.is_obstacle = False


def map_create():
    surface = pg.Surface([window.get_width(), window.get_height()])

    map = []
    for i in range(0, window.get_width(), GRIDSIZE):
        for j in range(0, window.get_height(), GRIDSIZE):
            r = MapRect(i, j, GREY)
            if i == 0 or i == window.get_width() - GRIDSIZE or j == 0 or j == window.get_height() - GRIDSIZE:
                r.is_obstacle = True
            pg.draw.rect(surface, r.color, r.rect)
            map.append(r)

    #Ostacolo 1
    i = GRIDSIZE * 20
    for j in range(400, window.get_height(), GRIDSIZE):
        for m in map:
            if m.rect.x == i and m.rect.y == j:
                m.is_obstacle = True

    #Ostacolo 2
    j = GRIDSIZE * 10
    for i in range(400, window.get_width(), GRIDSIZE):
        for m in map:
            if m.rect.x == i and m.rect.y == j:
                m.is_obstacle = True

    return surface, map


def rotate(image, sprite, angle):
    rotated_image = pg.transform.rotozoom(image, angle, 1)
    rotated_rect = rotated_image.get_rect(center=(sprite.x, sprite.y))
    return rotated_image, rotated_rect


def main():
    pg.display.set_caption("DisCoverage Exploration")
    icon = pg.image.load("robot1.png")
    pg.display.set_icon(icon)
    is_running = True
    surface, map = map_create()

    # Robots
    robot = Robot(100, window.get_height() - 100)

    while is_running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                is_running = False
        for m in map:
            if not m.found:
                if pg.sprite.collide_circle(robot, m):
                    if m.is_obstacle:
                        m.color = BLACK
                    else:
                        m.color = WHITE
                    m.found = True
                    pg.draw.rect(surface, m.color, m.rect)
        """
        robot.delta += 30
        robot.image, robot.rect = rotate(robot_image, robot, robot.delta)
        """
        window.blit(surface, (0, 0))
        window.blit(robot.image, robot.rect)
        pg.draw.rect(window, BLACK, robot.rect, 1)
        robot.update()
        pg.display.update()


if __name__ == '__main__':
    main()
