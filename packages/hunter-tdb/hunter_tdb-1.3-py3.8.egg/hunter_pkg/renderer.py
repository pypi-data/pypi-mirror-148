import numpy as np
import tcod

from hunter_pkg.entities import berry_bush as bb
from hunter_pkg.entities import camp as cp
from hunter_pkg.entities import fog
from hunter_pkg.entities import maps
from hunter_pkg.entities import rabbit as rbt

from hunter_pkg.helpers import layers
from hunter_pkg.helpers import math

from hunter_pkg import flogging
from hunter_pkg import log_level
from hunter_pkg import stats


flog = flogging.Flogging.get(__file__, log_level.LogLevel.get(__file__))

class Renderer():
    def __init__(self, view_width, view_height, map_width, map_height):
        self.map_width = map_width
        self.map_height = map_height
        self.view_width = view_width
        self.view_height = view_height
        self.view_x = 0 # left edge
        self.view_y = 0 # top edge

        self.scroll_speed = stats.get(f"settings.scroll-speed")
        self.tileset = tcod.tileset.load_tilesheet("resources/img/dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD)
        self.context = tcod.context.new_terminal(
            view_width,
            view_height,
            tileset=self.tileset,
            title="Hunter",
            vsync=False,
        )
        self.root_console = tcod.Console(view_width, view_height, order="F")

        self.layer_defaults = {
            layers.UI:        None,
            layers.FOG:       fog.instance,
            layers.CREATURES: None,
            layers.TERRAIN:   None,
        }
        self.layers = {}
        self.next_redraw_column = None
        self.redraw_all()
        self.compute_view_pos()

        for name, default in self.layer_defaults.items():
            self.layers[name] = []
            self.init_layer(name, default)

    def scroll_view(self, dir):
        # x-y is backwards for `direction` enum
        self.view_x = math.clamp(self.view_x + (dir[1] * self.scroll_speed), 0, self.map_width - self.view_width)
        self.view_y = math.clamp(self.view_y + (dir[0] * self.scroll_speed), 0, self.map_height - self.view_height)
        self.redraw_all()
        self.compute_view_pos()
    
    def compute_view_pos(self):
        self.view_right = self.view_x + self.view_width
        self.view_bottom = self.view_y + self.view_height

    def place(self, layer, obj, x, y):
        self.layers[layer][y][x] = obj
        self.redraw_tile(x, y)

    def remove(self, layer, x, y):
        self.layers[layer][y][x] = None

        self.redraw_tile(x, y)

    def get(self, layer, x, y):
        return self.layers[layer][y][x]

    def fill(self, layer, obj):
        for y, row in enumerate(self.layers[layer]):
            for x, v in enumerate(row):
                row[x] = obj

        self.redraw_all()

    def init_layer(self, layer, obj=None):
        self.layers[layer] = []
        for y in range(self.map_height):
            self.layers[layer].append([])

            for x in range(self.map_width):
                self.layers[layer][y].append(obj)

        self.redraw_all()

    def redraw_tile(self, x, y):
        if self.is_in_view(x, y):
            self.redraw_matrix[y - self.view_y, x  - self.view_x] = True

    def redraw_tiles(self, top_left_coord, bottom_right_coord):
        for y in range(top_left_coord.y, bottom_right_coord.y + 1):
            for x in range(top_left_coord.x, bottom_right_coord.x + 1):
                if self.is_in_view(x, y):
                    self.redraw_matrix[y - self.view_y, x  - self.view_x] = True

    def redraw_reset(self):
        self.redraw_matrix = np.zeros((self.view_height, self.view_width), dtype=bool)

    def redraw_all(self):
        self.redraw_matrix = np.ones((self.view_height, self.view_width), dtype=bool)

    def redraw_all_transition(self):
        self.next_redraw_column = self.view_width - 1

    def progress_redraw_all_transition(self):
        if self.next_redraw_column != None:
            for i in range(3):
                for row in self.redraw_matrix:
                    row[self.next_redraw_column] = True

                if self.next_redraw_column == 0:
                    self.next_redraw_column = None
                    break
                else:
                    self.next_redraw_column -= 1

    def is_in_view(self, x, y):
        visible_x = self.view_x <= x < self.view_right
        visible_y = self.view_y <= y < self.view_bottom

        return visible_x and visible_y

    def render(self, engine):
        kwargs = {
            "time_of_day": engine.time_of_day,
            "layer_visibility": engine.layer_visibility,
            "game_map": engine.game_map,
            "intelligent_entities": engine.intelligent_entities,
            "camp": engine.camp,
            "render_y_start": self.view_y,
            "render_y_end": self.view_height + self.view_y,
            "render_x_start": self.view_x,
            "render_x_end": self.view_width + self.view_x,
        }

        self.render_fog_and_terrain(**kwargs)
        self.render_entities(**kwargs)
        self.render_ui(engine)

        self.redraw_reset()

        self.context.present(self.root_console)

    # kwargs:
    #   time_of_day:          game time converted to time of day enum e.g. "morning"
    #   layer_visibility:     map of which layers are visible
    #   game_map:             entire game map
    #   intelligent_entities: list of intelligent entities
    #   camp                  reference to hunter's camp - TODO refactor this out
    #   render_y_start:       top-most tile of game map to render
    #   render_y_end:         bottom-most tile of game map to render
    #   render_x_start:       left-most tile of game map to render
    #   render_x_end:         right-most tile of game map to render
    def render_fog_and_terrain(self, **kwargs):
        dest_y = 0
        for src_y in range(kwargs["render_y_start"], kwargs["render_y_end"]):
            dest_x = 0
            for src_x in range(kwargs["render_x_start"], kwargs["render_x_end"]):
                if self.redraw_matrix[dest_y,dest_x]: # redraw_matrix x-y is backwards
                    if kwargs["layer_visibility"][layers.FOG] and self.get(layers.FOG, src_x, src_y) != None:
                        self.root_console.tiles_rgb[dest_x,dest_y] = self.get(layers.FOG, src_x, src_y).get_graphic_dt()
                    else:
                        self.root_console.tiles_rgb[dest_x,dest_y] = self.get(layers.TERRAIN, src_x, src_y).get_view(kwargs["time_of_day"])
                    
                dest_x += 1

            dest_y += 1
    
    def render_entities(self, **kwargs):
        camp = kwargs["camp"]
        if self.is_in_view(camp.x, camp.y) and camp.is_visible():
            rel_y = camp.y - self.view_y
            rel_x = camp.x - self.view_x
            self.root_console.print(rel_x, rel_y, camp.char, fg=camp.fg_color, bg=camp.bg_color)

        # TODO restructure this loop to iterate over each tile in view instead?
        for entity in kwargs["intelligent_entities"]:
            if self.is_in_view(entity.x, entity.y):
                rel_y = entity.y - self.view_y
                rel_x = entity.x - self.view_x

                if kwargs["game_map"].tiles[entity.y][entity.x].explored or not kwargs["layer_visibility"][layers.FOG]:
                    if entity.name in maps.entity_overview_map:
                        if not stats.get(f"settings.entity-visibility.{maps.entity_overview_map[entity.name]}"):
                            continue

                    if entity.hidden:
                        continue

                    self.root_console.print(rel_x, rel_y, entity.char, fg=entity.color, bg=entity.bg_color)

    def render_ui(self, engine):
        if engine.selected_entity != None:
            entity = engine.selected_entity
            if entity.name not in maps.unhighlightable_entities or not maps.unhighlightable_entities[entity.name]:
                render_selected = True

                if entity.name in maps.entity_overview_map:
                    render_selected = stats.get(f"settings.entity-visibility.{maps.entity_overview_map[entity.name]}")

                if render_selected:
                    self.root_console.print(entity.x, entity.y, entity.char, fg=entity.color, bg=entity.bg_color)

        if stats.get("settings.show-ui"):
            engine.stats_panel.render(self.root_console)
            engine.hover_panel.render(self.root_console)
            engine.selection_panel.render(self.root_console)
            engine.action_log_panel.render(self.root_console)
            engine.game_menu_panel.render(self.root_console)
            engine.controls_panel.render(self.root_console)

            if stats.get("settings.show-entity-overview"):
                engine.entity_overview_panel.render(self.root_console)

    def present(self):
        self.context.present(self.root_console)
