from bisect import insort
from collections import deque
from math import floor
from time import time
from typing import Set, Iterable, Any

import numpy.random as nprand
from tcod.context import Context
from tcod.console import Console

from hunter_pkg.entities import berry_bush as bb
from hunter_pkg.entities import camp as cp
from hunter_pkg.entities import deer as dr
from hunter_pkg.entities import hunter as htr
from hunter_pkg.entities import fog
from hunter_pkg.entities import rabbit as rbt
from hunter_pkg.entities import wolf as wlf
from hunter_pkg.entities import maps

from hunter_pkg.helpers import generic as gen
from hunter_pkg.helpers import layers
from hunter_pkg.helpers import math
from hunter_pkg.helpers import rng
from hunter_pkg.helpers import time_of_day as tod

from hunter_pkg.ui import panel as ui_panel
from hunter_pkg.ui import collision as ui_cllsn

from hunter_pkg import event as ev
from hunter_pkg import flogging
from hunter_pkg import log_level
from hunter_pkg import stats
from hunter_pkg import terrain
from hunter_pkg import vision_map as vsmap


flog = flogging.Flogging.get(__file__, log_level.LogLevel.get(__file__))

class Engine:
    def __init__(self, intelligent_entities, static_entities, input_handler, game_map, renderer):
        self.settings = stats.get("settings")
        self.paused = False
        self.game_speed = stats.get("settings.game-speed")
        self.game_speed_adj = 0
        self.game_speed_max = stats.get("settings.game-speed-max")
        self.game_speed_min = stats.get("settings.game-speed-min")
        self.game_time = stats.get("settings.game-time.initial")
        self.intelligent_entities = intelligent_entities
        self.static_entities = static_entities
        self.input_handler = input_handler
        self.game_map = game_map
        self.renderer = renderer
        self.layer_visibility = {
            layers.UI:        True,
            layers.FOG:       True,
            layers.CREATURES: True,
            layers.TERRAIN:   True,
        }
        self.entropy_event_queue = deque()
        self.ai_event_queue = deque()
        self.hunter = None
        self.camp = None
        self.hovered_tile = None
        self.hovered_ui_element = None
        self.selected_entity = None
        self.time_of_day = tod.MORNING # init this to morning for now
        self.days_elapsed = 1
        self.dump_profiler = False

    def handle_inputs(self, inputs: Iterable[Any]) -> None:
        for input in inputs:
            action = self.input_handler.dispatch(input)

            if action is None:
                continue

            action.perform(self)

    def init_entropy_event_queue(self, entities):
        for entity in entities:
            self.entropy_event_queue.append(ev.EntropyEvent(entity))

        self.entropy_event_queue = deque(sorted(self.entropy_event_queue))

    def init_ai_event_queue(self, entities):
        for entity in entities:
            self.ai_event_queue.append(ev.AIEvent(entity, rng.range_float(0, stats.get("settings.default-update-interval"), 0.0001)))

        self.ai_event_queue = deque(sorted(self.ai_event_queue))

    def advance_game_time(self):
        prev_time = self.game_time
        prev_time_of_day = self.get_time_of_day(prev_time)
        factor = stats.get(f"settings.game-time.factors.{prev_time_of_day}")
        new_time = self.game_time + (factor * (self.game_speed + self.game_speed_adj))
        new_time_of_day = self.time_of_day = self.get_time_of_day(new_time)

        if new_time_of_day != prev_time_of_day:
            flog.debug(f"it's now {new_time_of_day}")
            self.renderer.redraw_all_transition()

        if math.get_decimal(new_time) >= stats.get("settings.game-time.thresholds.max"):
            flog.debug("it's a new day!")
            self.days_elapsed += 1

            if self.hunter.alive:
                self.hunter.days_survived += 1

        self.game_time = math.round_game_time(new_time)
    
    def get_time_of_day(self, full_time):
        day_time = full_time - floor(full_time)

        if day_time > stats.get("settings.game-time.thresholds.night"):
            return tod.NIGHT
        elif day_time > stats.get("settings.game-time.thresholds.evening"):
            return tod.EVENING
        elif day_time > stats.get("settings.game-time.thresholds.afternoon"):
            return tod.AFTERNOON
        elif day_time > stats.get("settings.game-time.thresholds.morning"):
            return tod.MORNING
        else:
            return tod.NIGHT

    # Queue of events that should occur steadily as the game progresses e.g. berry bush regrows berries, hunter becomes more hungry/tired, etc.
    def process_entropy_events(self):
        flog.debug(f"entropy_event_queue len: {len(self.entropy_event_queue)}")
        while(len(self.entropy_event_queue) > 0):
            event = self.entropy_event_queue[0]

            if event.time < self.game_time:
                event.process()
                self.entropy_event_queue.popleft()
                if event.entity.requeue():
                    insort(self.entropy_event_queue, ev.EntropyEvent(event.entity))
            else:
                break

    # Queue of events that don't occur steadily, but rather have independent "cooldowns" e.g. hunter shoot bow action, hunter move action, etc.
    def process_ai_events(self):
        flog.debug(f"ai_event_queue len: {len(self.ai_event_queue)}")
        while(len(self.ai_event_queue) > 0):
            event = self.ai_event_queue[0]

            if event.time < self.game_time:
                cooldown = event.process()
                self.ai_event_queue.popleft()
                if event.entity.requeue():
                    insort(self.ai_event_queue, ev.AIEvent(event.entity, self.game_time + cooldown))
            else:
                break

    def spawn_entities(self):
        intelligent_entities = []
        static_entities = []
        self.berry_bush_count = 0

        # wolf = wlf.Wolf(self, 80, 20)
        # self.game_map.tiles[20][80].entities.append(wolf)
        # intelligent_entities.append(wolf)

        for y, row in enumerate(self.game_map.tiles):
            for x, tile in enumerate(row):
                if tile.terrain.walkable:
                    if rng.rand() < stats.get("rabbit.spawn"):
                        burrow = rbt.Burrow(x, y)
                        rabbit = rbt.Rabbit(self, x, y)
                        rabbit.burrow = burrow
                        self.game_map.tiles[y][x].add_entities([burrow, rabbit])
                        intelligent_entities.append(rabbit)
                    if rng.rand() < stats.get("wolf.spawn"):
                        wolf = wlf.Wolf(self, x, y)
                        self.game_map.tiles[y][x].entities.append(wolf)
                        intelligent_entities.append(wolf)
                    if rng.rand() < stats.get("deer.spawn"):
                        buck = dr.Buck(self, x, y)
                        self.game_map.tiles[y][x].entities.append(buck)
                        intelligent_entities.append(buck)

                        for i in range(rng.range_int(1, 4)):
                            doe = dr.Doe(self, x, y, buck)
                            self.game_map.tiles[y][x].entities.append(doe)
                            intelligent_entities.append(doe)
                            buck.herd.append(doe)
                if isinstance(tile.terrain, terrain.Grass) or isinstance(tile.terrain, terrain.Forest):
                    if rng.rand() < stats.get("berry-bush.spawn"):
                        berry_bush = bb.BerryBush(self, x, y)
                        self.game_map.tiles[y][x].entities.append(berry_bush)
                        static_entities.append(berry_bush)
                        self.berry_bush_count += 1

        return intelligent_entities, static_entities

    def get_entity_counts(self):
        counts = {
            bb.BerryBush: self.berry_bush_count,
            dr.Buck: 0,
            dr.Doe: 0,
            htr.Hunter: 0,
            wlf.Wolf: 0,
            rbt.Rabbit: 0,
        }

        for entity in self.intelligent_entities:
            if (gen.has_member(entity, 'alive') and entity.alive) or not gen.has_member(entity, 'alive'):
                if not entity.__class__ in counts:
                    counts[entity.__class__] = 1
                else:
                    counts[entity.__class__] += 1
        
        return counts

    def generate_tile_views(self):
        self.game_map.generate_tile_views()

    def init_ui_collision_layer(self):
        self.ui_collision_layer = ui_cllsn.CollisionLayer(self.renderer.view_height, self.renderer.view_width)

    def init_stats_panel(self):
        margin = 2
        self.stats_panel = ui_panel.StatsPanel(x=1, y=1, height=16, width=17, engine=self)

    def init_hover_panel(self):
        self.hover_panel = ui_panel.HoverPanel(x=1, y=17, height=20, width=17, engine=self)

    def init_selection_panel(self):
        height = self.renderer.view_height - self.stats_panel.height - self.hover_panel.height - 2
        self.selection_panel = ui_panel.SelectionPanel(x=1, y=37, height=height, width=17, engine=self)

    def init_action_log_panel(self):
        x = 20
        height = 13
        margin = 2
        self.action_log_panel = ui_panel.ActionLogPanel(x=x, y=self.renderer.view_height - height - 1, height=height, width=self.renderer.view_width - x - margin, engine=self)

    def init_game_menu_panel(self):
        height = 27
        width = 29
        y_offset = -3
        x = round((self.renderer.view_width / 2) - (width / 2))
        y = round((self.renderer.view_height / 2) - (height / 2)) + y_offset
        self.game_menu_panel = ui_panel.GameMenuPanel(x=x, y=y, height=height, width=width, button_width=17, engine=self)

    def init_controls_panel(self):
        height = 20
        width = 33
        y_offset = -3
        x = round((self.renderer.view_width / 2) - (width / 2))
        y = round((self.renderer.view_height / 2) - (height / 2)) + y_offset
        self.controls_panel = ui_panel.ControlsPanel(x=x, y=y, height=height, width=width, engine=self)

    def init_entity_overview_panel(self):
        width = 19
        x = self.renderer.view_width - width - 2
        self.entity_overview_panel = ui_panel.EntityOverviewPanel(x=x, y=1, height=16, width=width, engine=self)

    # TODO dedup this (duplicated in hunter.py)
    def init_fog_reveal(self):
        vd = self.hunter.vision_distance[self.time_of_day]
        vision_map = vsmap.circle(vd)
        x_start = self.hunter.x - vd
        x_end = self.hunter.x + vd
        y_start = self.hunter.y - vd
        y_end = self.hunter.y + vd

        for y in range(y_start, y_end+1):
            for x in range(x_start, x_end+1):
                # This is confusing. Basic idea is to apply the vision map to the hunter's memory and the game map, but only
                # set "explored" to True, never to False i.e. don't let the corners of a circular vision map "unexplore" tiles.
                # And clamp everything so we dont accidentally affect the opposite side of the map.
                clamp_width = self.hunter.engine.game_map.width-1
                clamp_height = self.hunter.engine.game_map.height-1
                rel_x = math.clamp(x - x_start, 0, clamp_width)
                rel_y = math.clamp(y - y_start, 0, clamp_height)
                clmp_x = math.clamp(x, 0, clamp_width)
                clmp_y = math.clamp(y, 0, clamp_height)
                prev_visible = f"{clmp_x},{clmp_y}" in self.hunter.memory.map["explored-terrain"].keys() and self.hunter.memory.map["explored-terrain"][f"{clmp_x},{clmp_y}"]
                curr_visible = vision_map[rel_y][rel_x].visible
                self.hunter.memory.map["explored-terrain"][f"{clmp_x},{clmp_y}"] = curr_visible or prev_visible
                self.game_map.tiles[clmp_y][clmp_x].explored = curr_visible or prev_visible

                if curr_visible or prev_visible:
                    self.renderer.remove(layers.FOG, clmp_x, clmp_y)

    def init_renderer_terrain_layer(self):
        self.renderer.layers[layers.TERRAIN] = self.game_map.tiles

    def find_hunter_spawn_point(self):
        camp_x_min = round(self.game_map.width * 0.25)
        camp_x_max = round(self.game_map.width * 0.75)
        camp_y_min = round(self.game_map.height * 0.2)
        camp_y_max = round(self.game_map.height * 0.6)
        found = False

        # TODO make this smarter
        while(not found):
            x = rng.range_int(camp_x_min, camp_x_max)
            y = rng.range_int(camp_y_min, camp_y_max)

            if self.game_map.tiles[y][x].terrain.walkable:
                return [x, y]

    def render(self):
        self.renderer.progress_redraw_all_transition()

        self.renderer.render(self)
