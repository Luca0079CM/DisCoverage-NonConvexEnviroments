import pygame as pg
import math
import Dijkstra

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 153, 76)
RED = (255, 0, 0)
BLUE = (0, 128, 255)

robot_image = pg.image.load("robot1.png")
robot_image_2 = pg.image.load("robot2.png")
robot_image_3 = pg.image.load("robot3.png")
# Speed
v = 1
# Delta
pi = math.pi
converter = 180 / pi
tollerance = 0.1
standard_delta = [0, pi / 4, pi / 2, pi * 3 / 4, pi, pi * 5 / 4, pi * 3 / 2, pi * 7 / 4]


class Robot(pg.sprite.Sprite):
    def __init__(self, id, x, y, line_color):
        super().__init__()
        self.id = id
        self.image = robot_image
        self.x = x
        self.y = y
        self.radius = 35
        self.rect = self.image.get_rect(center=(x, y))
        self.delta = standard_delta[0]
        self.white_tiles = []
        self.frontier = []
        self.is_moving = False
        self.target = None
        self.target_vector = []
        self.current_target = None
        self.path = []
        self.empty_frontier = False
        self.line_color = line_color
        self.first = True
        self.disabled = False

    def update(self, surface, map):
        if not self.is_moving:
            start = self.calculate_start_and_frontier(surface, map)
            if self.first:
                self.target_vector.append(start.rect.center)
                self.first = False
            self.target = self.calculate_target()
            if self.target is None:
                self.empty_frontier = True
                self.is_moving = False
            if not self.empty_frontier:
                self.target_vector.append(self.target.rect.center)
                pg.draw.rect(surface, BLUE, self.target.rect)
                self.path = self.calculate_path(start)
                trg = self.path.pop(0)
                for m in map:
                    if m.id[0] == trg[0] and m.id[1] == trg[1]:
                        self.current_target = m
                        break
                self.is_moving = True

        if not self.empty_frontier:
            if math.dist(self.rect.center, self.target.rect.center) < tollerance:
                self.is_moving = False
                self.current_target = None
                for f in self.frontier:
                    pg.draw.rect(surface, WHITE, f.rect)
                self.frontier.clear()
                self.path.clear()

            if self.current_target is not None:
                self.delta = math.atan2(self.current_target.rect.center[1] - self.rect.center[1],
                                        self.current_target.rect.center[0] - self.rect.center[0])
                x, y = self.rect.center
                if self.id % 3 == 1:
                    self.image, self.rect = rotate(robot_image, x, y, self.delta)
                elif self.id % 3 == 2:
                    self.image, self.rect = rotate(robot_image_2, x, y, self.delta)
                elif self.id % 3 == 0:
                    self.image, self.rect = rotate(robot_image_3, x, y, self.delta)
                dx = math.cos(self.delta) * v
                dy = math.sin(self.delta) * v
                self.x += dx
                self.y += dy
                self.rect = self.image.get_rect(center=(self.x, self.y))
                if math.dist(self.rect.center, self.current_target.rect.center) < tollerance and \
                        self.current_target.id != self.target.id:
                    trg = self.path.pop(0)
                    for m in map:
                        if m.id[0] == trg[0] and m.id[1] == trg[1]:
                            self.current_target = m
                            break

    def calculate_start_and_frontier(self, surface, map):
        start = None
        min_dist = 10000

        for m in self.white_tiles:
            if self.rect.colliderect(m.rect):
                if math.dist(self.rect.center, m.rect.center) < min_dist:
                    start = m
                    min_dist = math.dist(self.rect.center, m.rect.center)

        frontier = []
        for t in self.white_tiles:
            grey_neighbour = False
            black_neighbour = False
            for m in map:
                n = 0
                for i in range(0, len(t.neighbour_ids)):
                    if m.id[0] == t.neighbour_ids[i][0] and m.id[1] == t.neighbour_ids[i][1]:
                        n += 1
                        if m.is_obstacle:
                            black_neighbour = True
                            grey_neighbour = False
                        elif m.found == 0:
                            grey_neighbour = True
                        break
                if black_neighbour:
                    break
                if n == 4:
                    break
            if grey_neighbour:
                frontier.append(t)

        for f in frontier:
            if f not in self.frontier:
                self.frontier.append(f)
                f.color = RED
                pg.draw.rect(surface, f.color, f.rect)
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
        for t in self.white_tiles:
            nodes[i] = t.id
            i += 1
        for n in self.white_tiles:
            l = -1
            vertex = {}
            for k in range(0, len(nodes)):
                if nodes[k] == n.id:
                    l = k
                    break
            for i in range(1, len(n.neighbour_ids) + 1):
                for j in range(0, len(nodes)):
                    if n.neighbour_ids[i - 1][0] == nodes[j][0] and n.neighbour_ids[i - 1][1] == nodes[j][1]:
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

    def deactivate(self):
        self.disabled = True


def rotate(image, x, y, angle):
    angle = angle * converter
    angle = -angle
    rotated_image = pg.transform.rotozoom(image, angle, 1)
    rotated_rect = rotated_image.get_rect(center=(x, y))
    return rotated_image, rotated_rect
