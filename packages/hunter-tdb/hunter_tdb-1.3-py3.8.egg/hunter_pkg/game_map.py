from json import loads
import numpy as np
from os import popen
from tcod.console import Console

from hunter_pkg.entities import berry_bush as bb
from hunter_pkg.entities import camp as cp
from hunter_pkg.entities import fog

from hunter_pkg.helpers.coord import Coord
from hunter_pkg.helpers import generic as gen
from hunter_pkg.helpers import math
from hunter_pkg.helpers import time_of_day as tod

from hunter_pkg import colors
from hunter_pkg import flogging
from hunter_pkg import log_level
from hunter_pkg import map_generator as mapgen
from hunter_pkg import terrain


flog = flogging.Flogging.get(__file__, log_level.LogLevel.get(__file__))

terrain_map = {
    "G": terrain.Grass(),
    "F": terrain.Forest(),
    "^": terrain.Mountain(),
    "~": terrain.Water(),
}

class GameMap:
    def __init__(self, width, height, seed, show_fog):
        self.height = height
        self.width = width
        self.tiles, self.path_map = self.init_empty_map()
        self.show_fog = show_fog
        self.generate_map(seed)
        #self.load_map_from_file('resources/maps/large_zoomed_map.txt')

    def init_empty_map(self):
        tiles = []
        path_map = []

        for i in range(self.height):
            tiles.append([])
            path_map.append([])

        return tiles, path_map

    def load_map_from_file(self, filepath):
        with open(filepath) as file:
            line = file.readline()
            y = 0
            while line:
                x = 0
                cells = line.split(" ")

                for cell in cells:
                    if cell != '':
                        self.tiles[y].append(Tile(self, terrain_map[cell.strip()], x, y))
                        self.path_map[y].append(1 if self.tiles[y][x].terrain.walkable else 0)
                        x = x + 1

                line = file.readline()
                y = y + 1

    def generate_map(self, seed):
        map = mapgen.generate(self.height, self.width, 0.3, seed)

        for y in range(len(map.geo_map)):
            row = map.geo_map[y]
            for x in range(len(row)):
                self.tiles[y].append(Tile(self, terrain_map[row[x].strip()], x, y))
                self.path_map[y].append(1 if self.tiles[y][x].terrain.walkable else 0)

    def generate_tile_views(self):
        for row in self.tiles:
            for tile in row:
                tile.generate_views()

    def in_bounds(self, x, y):
        """Return True if x and y are inside of the bounds of this map."""
        return 0 <= x < self.width and 0 <= y < self.height

    def clamp_coord(self, x, y):
        max_x = self.width - 1
        max_y = self.height - 1
        dest = Coord()
        dest.x = math.clamp(x, 0, max_x)
        dest.y = math.clamp(y, 0, max_y)

        return dest

    def get_tile(self, x, y):
        if y < 0 or x < 0 or y >= self.height or x >= self.width:
            return None
        else:
            return self.tiles[y][x]


class Tile:
    def __init__(self, game_map, terrain, x, y):
        self.game_map = game_map
        self.terrain = terrain
        self.entities = []
        self.x = x
        self.y = y
        self.hovered = False
        self.explored = False
        self.views = {}

    # tile views must be generated after berry bushes are spawned
    def generate_views(self):
        self.views = {
            tod.MORNING: {
                True:  self.get_graphic_dt(tod.MORNING, True),  # hovered: True
                False: self.get_graphic_dt(tod.MORNING, False), # hovered: False
            },
            tod.AFTERNOON: {
                True:  self.get_graphic_dt(tod.AFTERNOON, True),
                False: self.get_graphic_dt(tod.AFTERNOON, False),
            },
            tod.EVENING: {
                True:  self.get_graphic_dt(tod.EVENING, True),
                False: self.get_graphic_dt(tod.EVENING, False),
            },
            tod.NIGHT: {
                True:  self.get_graphic_dt(tod.NIGHT, True),
                False: self.get_graphic_dt(tod.NIGHT, False),
            },
        }

    def get_view(self, time_of_day):
        return self.views[time_of_day][self.hovered]

    def get_graphic_dt(self, time_of_day, hovered):
        if hovered:
            return self.terrain.get_graphic_dt(time_of_day, None, None, colors.light_gray)
        else:
            for entity in self.entities:
                if isinstance(entity, bb.BerryBush):
                    return self.terrain.get_graphic_dt(time_of_day, None, None, entity.bg_color(time_of_day))

        return self.terrain.get_graphic_dt(time_of_day, None, None, None) # gross as hell

    def add_entities(self, entities):
        self.entities.extend(entities)

    def remove_entities(self, entities):
        for e in entities:
            self.entities.remove(e)

    # TODO should probably be moved off of Tile
    def select_next_entity(self, engine):
        if len(self.entities) > 0:
            current_index = None

            for i in range(len(self.entities)):
                if self.entities[i] == engine.selected_entity:
                    current_index = i
                    break

            if current_index == None:
                next_index = 0
            else:
                next_index = current_index + 1

            if next_index >= len(self.entities):
                next_index = 0
            
            if gen.has_method(engine.selected_entity, "deselect"):
                engine.selected_entity.deselect()

            engine.selected_entity = None
            flog.debug("deselected")

            engine.selected_entity = self.entities[next_index]

            if gen.has_method(engine.selected_entity, "select"):
                engine.selected_entity.select()

            flog.debug(f"{engine.selected_entity.__class__} is selected")
        else:
            if gen.has_method(engine.selected_entity, "deselect"):
                engine.selected_entity.deselect()

            engine.selected_entity = None
            flog.debug("deselected")

    def reveal(self):
        self.explored = True
