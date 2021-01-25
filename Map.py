import pygame as pg
import math
GRIDSIZE = 20
# Colors
GREY = (160, 160, 160)
LIGHTGREY = (190, 190, 190)
BLACK = (0, 0, 0)


class MapRect(pg.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.rect = pg.Rect((x, y), (GRIDSIZE, GRIDSIZE))
        self.color = color
        self.found = 0
        self.is_obstacle = False
        self.id = [int(x/GRIDSIZE), int(y/GRIDSIZE)]
        self.neighbour_ids = []
        self.neighbour_distances = {}


def map_create(window):
    surface = pg.Surface([window.get_width(), window.get_height()])
    map = []
    n_total_tiles = 0
    for i in range(0, window.get_width(), GRIDSIZE):
        for j in range(0, window.get_height(), GRIDSIZE):
            if ((i + j)/GRIDSIZE) % 2 == 0:
                r = MapRect(i, j, GREY)
            else:
                r = MapRect(i, j, LIGHTGREY)
            if i == 0 or i == window.get_width() - GRIDSIZE or j == 0 or j == window.get_height() - GRIDSIZE:
                r.is_obstacle = True
                r.color = BLACK
            pg.draw.rect(surface, r.color, r.rect)
            map.append(r)
            n_total_tiles += 1

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

    # Neighbour
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

    return surface, map, n_total_tiles


def search_by_id(map, id):
    x, y = id
    for m in map:
        if m.id[0] == x and m.id[1] == y:
            return m
