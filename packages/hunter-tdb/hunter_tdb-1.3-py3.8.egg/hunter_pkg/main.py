#!/usr/bin/env python3

from bisect import insort
import cProfile as profile
import io
from math import floor
import pstats
import time
import tcod

from hunter_pkg.entities import camp as cp
from hunter_pkg.entities import hunter as htr

from hunter_pkg.helpers import rng

from hunter_pkg import engine as eng
from hunter_pkg import flogging
from hunter_pkg import game_map as gm
from hunter_pkg import input_handlers
from hunter_pkg import log_level
from hunter_pkg import renderer as rndr
from hunter_pkg import stats


flog = flogging.Flogging.get(__file__, log_level.LogLevel.get(__file__))

def main() -> None:
    seed = stats.get("settings.seed")
    if seed == None:
        seed = round(time.time())

    flog.info(f"rng seed: {seed}")
    rng.set_seed(seed)

    seconds_per_frame = 0.016

    view_width = stats.get("settings.view.width")
    view_height = stats.get("settings.view.height")
    map_width = stats.get("settings.map.width")
    map_height = stats.get("settings.map.height")

    input_handler = input_handlers.InputHandler()
    game_map = gm.GameMap(map_width, map_height, seed, stats.get("settings.show-fog"))
    renderer = rndr.Renderer(view_width, view_height, map_width, map_height)
    engine = eng.Engine(intelligent_entities=[], static_entities=[], input_handler=input_handler, game_map=game_map, renderer=renderer)

    x, y = engine.find_hunter_spawn_point()
    
    camp = cp.Camp(engine, x, y)
    game_map.tiles[camp.y][camp.x].add_entities([camp])

    hunter = htr.Hunter(engine, camp.x, camp.y)
    game_map.tiles[hunter.y][hunter.x].add_entities([hunter])

    renderer.view_x = hunter.x - floor(renderer.view_width / 2)
    renderer.view_y = hunter.y - floor(renderer.view_height / 2)
    renderer.compute_view_pos()

    # hard-coding knowledge of camp for now
    hunter.memory.map["camp"] = {
        "x": camp.x,
        "y": camp.y
    }

    engine.intelligent_entities, engine.static_entities = engine.spawn_entities()
    engine.hunter = hunter
    engine.camp = camp
    engine.intelligent_entities.append(hunter)

    engine.generate_tile_views()

    engine.init_ui_collision_layer()
    engine.init_stats_panel()
    engine.init_hover_panel()
    engine.init_selection_panel()
    engine.init_action_log_panel()
    engine.init_game_menu_panel()
    engine.init_controls_panel()
    engine.init_entity_overview_panel()
    engine.init_fog_reveal()
    engine.init_renderer_terrain_layer()

    engine.init_entropy_event_queue(engine.intelligent_entities)
    engine.init_entropy_event_queue(engine.static_entities)
    engine.init_ai_event_queue(engine.intelligent_entities)

    n = 0
    profiler_on = stats.get("debug.profiler")
    profler_out = stats.get('debug.profiler-out')

    while True:
        current = time.time()

        if profiler_on:
            n += 1

        if profiler_on and (engine.dump_profiler or n == 100):
            flog.debug(f"Profiling `advance_game_state` -- saving results to '{profler_out}'")
            pr = profile.Profile()

            pr.enable()
            advance_game_state(engine)
            pr.disable()

            s = io.StringIO()
            ps = pstats.Stats(pr, stream=s).sort_stats('tottime')
            ps.print_stats()

            with open(profler_out, 'a') as f:
                f.write(f"{'-' * 100}\n")
                f.write(s.getvalue())

            engine.dump_profiler = False
        else:
            advance_game_state(engine)

        previous = current
        current = time.time()
        elapsed_time = current - previous
        sleep_time = seconds_per_frame - elapsed_time
        # #flog.debug(f"et:{elapsed_time}")
        # #flog.debug(f"st:{sleep_time}")

        if(sleep_time > 0):
            time.sleep(sleep_time)

def advance_game_state(engine):
    inputs = tcod.event.get()
    engine.handle_inputs(inputs)

    if not engine.paused:
        engine.advance_game_time()
        engine.process_entropy_events()
        engine.process_ai_events()

    engine.render()


if __name__ == "__main__":
    main()
