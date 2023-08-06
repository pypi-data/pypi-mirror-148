import cProfile as profile
import io
import pstats
from random import randint
import tcod

from hunter_pkg import map_generator as mapgen


def main():
    tileset = tcod.tileset.load_tilesheet("resources/img/dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD)

    scroll_speed = 2

    map_height = 200
    map_width = 250
    map_console = tcod.Console(map_width, map_height)

    pr = profile.Profile()
    pr.enable()

    # Print entire map to a map console that is hidden
    create_map(map_console, map_height, map_width)

    pr.disable()
    s = io.StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats('tottime')
    ps.print_stats()
    with open("profiler_results.txt", 'a') as f:
        f.write(f"{'-' * 100}\n")
        f.write(s.getvalue())

    print("Creating root console...")
    window_height = 100
    window_width = 125
    root_console = tcod.Console(window_width, window_height)

    root_console.print(0, 0, "Arrow keys to move")

    sdl_window = tcod.sdl.video.new_window(
        root_console.width * tileset.tile_width,
        root_console.height * tileset.tile_height,
        flags=tcod.lib.SDL_WINDOW_MAXIMIZED,
    )
    sdl_renderer = tcod.sdl.render.new_renderer(sdl_window, target_textures=True)
    atlas = tcod.render.SDLTilesetAtlas(sdl_renderer, tileset)
    console_render = tcod.render.SDLConsoleRender(atlas)

    print("Starting loop...")
    view_x = 0
    view_y = 0
    while True:
        sdl_renderer.copy(console_render.render(root_console))
        sdl_renderer.present()

        # If arrow key input is received, blit only the visible parts of the map console into the root console
        for event in tcod.event.wait():
            if isinstance(event, tcod.event.Quit):
                raise SystemExit()
            elif isinstance(event, tcod.event.KeyDown):
                key = event.sym
                if key == tcod.event.K_UP:
                    view_y -= scroll_speed
                elif key == tcod.event.K_RIGHT:
                    view_x += scroll_speed
                elif key == tcod.event.K_DOWN:
                    view_y += scroll_speed
                elif key == tcod.event.K_LEFT:
                    view_x -= scroll_speed

                blit(map_console, root_console, view_x, view_y)

def create_map(console, height, width):
    print("Generating map...")
    map = mapgen.generate(height, width, 0.3)

    print("Loading map...")
    for y in range(len(map.geo_map)):
        row = map.geo_map[y]
        for x in range(len(row)):
            console.print(x, y, row[x])

def blit(src_console, dest_console, x, y):
    blit_y_start = y
    blit_y_end = dest_console.height + y
    blit_x_start = x
    blit_x_end = dest_console.width + x

    dest_y = 0
    for src_y in range(blit_y_start, blit_y_end):
        dest_x = 0
        for src_x in range(blit_x_start, blit_x_end):
            src_console.blit(dest_console, dest_x, dest_y, src_x, src_y, 10, 10)
            dest_x += 1

        dest_y += 1


if __name__ == "__main__":
    main()