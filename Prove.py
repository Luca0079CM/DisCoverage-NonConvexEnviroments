import pygame as pg
import math
from random import *
import Map, Dijkstra
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
# Speed
v = 0.2
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
        self.radius = 25
        self.rect = self.image.get_rect(center=(x, y))
        self.delta = standard_delta[0]
        self.front_tiles = []
        self.frontier = []
        self.is_moving = False
        self.target = None
        self.current_target = None
        self.path = []

    def update(self, surface, map):
        if not self.is_moving:
            start = self.calculate_start_and_frontier(surface, map)
            self.target = self.calculate_target()
            pg.draw.rect(surface, BLUE, self.target.rect)
            self.path = self.calculate_path(start)
            print(self.path)
            trg = self.path.pop(0)
            for m in map:
                if m.id[0] == trg[0] and m.id[1] == trg[1]:
                    self.current_target = m
                    break
            self.is_moving = True

        if self.current_target is not None:
            self.delta = math.atan2(self.current_target.rect.center[1] - self.rect.center[1],
                               self.current_target.rect.center[0] - self.rect.center[0])
            x, y = self.rect.center
            self.image, self.rect = rotate(robot_image, x, y, self.delta)
            dx = math.cos(self.delta) * v
            dy = math.sin(self.delta) * v
            self.x += dx
            self.y += dy
            self.rect = self.image.get_rect(center=(self.x, self.y))
            if self.current_target.id[0] != self.target.id[0] and self.current_target.id[1] != self.target.id[1] and\
                    self.rect.collidepoint(self.current_target.rect.center):
                print(len(self.path))
                self.current_target = self.path.pop(0)

        if self.rect.collidepoint(self.target.rect.center):
            self.is_moving = False
            for f in self.frontier:
                pg.draw.rect(surface, WHITE, f.rect)
            self.frontier.clear()
            self.path.clear()

    def calculate_start_and_frontier(self, surface, map):
        front_tiles = []
        start = None
        min_dist = 10000
        for m in map:
            if m.color == WHITE:
                angle = self.delta + math.atan2(m.rect.center[1] - self.rect.center[1],
                                                m.rect.center[0] - self.rect.center[0])
                if round(math.sin(angle), 2) <= 0:
                    front_tiles.append(m)
                    if math.dist(self.rect.center, m.rect.center) < min_dist:
                        start = m
                        min_dist = math.dist(self.rect.center, m.rect.center)
        for t in front_tiles:
            for m in map:
                for i in range(0, len(t.neighbour_ids)):
                    if m.found == 0 and m.id[0] == t.neighbour_ids[i][0] and m.id[1] == t.neighbour_ids[i][1]:
                        self.frontier.append(t)
        for f in self.frontier:
            f.color = RED
            pg.draw.rect(surface, f.color, f.rect)
        self.front_tiles = front_tiles
        return start

    def calculate_target(self):
        minimum = None
        min_dist = 0
        for f in self.frontier:
            if math.dist(self.rect.center, f.rect.center) < min_dist or min_dist == 0:
                min_dist = math.dist(self.rect.center, f.rect.center)
                minimum = f
        return minimum

    def calculate_path(self, start):
        g = Dijkstra.Graph()
        nodes = {}
        i = 0
        for t in self.front_tiles:
            nodes[i] = t.id
            i += 1
        """
        print(nodes)
        for n in self.front_tiles:
            print(n.id)
            for i in range(1, len(n.neighbour_ids) + 1):
                print(" ", n.neighbour_ids[i - 1], "=>", n.neighbour_distances[i])
        """
        for n in self.front_tiles:
            l = -1
            vertex = {}
            for k in range(0, len(nodes)):
                if nodes[k] == n.id:
                    l = k
                    break
            for i in range(1, len(n.neighbour_ids) + 1):
                for j in range(0, len(nodes)):
                    if n.neighbour_ids[i-1][0] == nodes[j][0] and n.neighbour_ids[i-1][1] == nodes[j][1]:
                        tmp = str(j)
                        vertex[tmp] = n.neighbour_distances[i]
                        break
            l = str(l)
            g.add_vertex(l, vertex)

        s, t = 0, 0
        for i in range(0, len(nodes)):
            if nodes[i] == start.id:
                s = str(i)
            if nodes[i] == self.target.id:
                t = str(i)

        tmp_path = g.shortest_path(s, t)
        path = []
        for v in tmp_path:
            path.append(nodes.get(int(v)))
        return path


def rotate(image, x, y, angle):
    angle -= pi/2
    angle = angle * converter
    rotated_image = pg.transform.rotozoom(image, angle, 1)
    rotated_rect = rotated_image.get_rect(center=(x, y))
    return rotated_image, rotated_rect


if __name__ == '__main__':
    main()


def main():
    x = []
    for i in range(0, 10):
        x.append(i)



if __name__ == '__main__':
    main()

    for m in map:
        i += 1
        if not m.is_obstacle:
            m.neighbour_ids.append((m.id[0] - 1, m.id[1] - 1))
            m.neighbour_distances[1] = math.dist(m.rect.center,
                                                 search_by_id(map, (m.id[0] - 1, m.id[1] - 1)).rect.center)
            m.neighbour_ids.append((m.id[0] - 1, m.id[1]))
            m.neighbour_distances[2] = math.dist(m.rect.center,
                                                 search_by_id(map, (m.id[0] - 1, m.id[1])).rect.center)
            m.neighbour_ids.append((m.id[0] - 1, m.id[1] + 1))
            m.neighbour_distances[3] = math.dist(m.rect.center,
                                                 search_by_id(map, (m.id[0] - 1, m.id[1] + 1)).rect.center)

            m.neighbour_ids.append((m.id[0], m.id[1] - 1))
            m.neighbour_distances[4] = math.dist(m.rect.center,
                                                 search_by_id(map, (m.id[0], m.id[1] - 1)).rect.center)
            m.neighbour_ids.append((m.id[0], m.id[1] + 1))
            m.neighbour_distances[5] = math.dist(m.rect.center,
                                                 search_by_id(map, (m.id[0], m.id[1] + 1)).rect.center)

            m.neighbour_ids.append((m.id[0] + 1, m.id[1] - 1))
            m.neighbour_distances[6] = math.dist(m.rect.center,
                                                 search_by_id(map, (m.id[0] + 1, m.id[1] - 1)).rect.center)
            m.neighbour_ids.append((m.id[0] + 1, m.id[1]))
            m.neighbour_distances[7] = math.dist(m.rect.center,
                                                 search_by_id(map, (m.id[0] + 1, m.id[1])).rect.center)
            m.neighbour_ids.append((m.id[0] + 1, m.id[1] + 1))
            m.neighbour_distances[8] = math.dist(m.rect.center,
                                                 search_by_id(map, (m.id[0] + 1, m.id[1] + 1)).rect.center)