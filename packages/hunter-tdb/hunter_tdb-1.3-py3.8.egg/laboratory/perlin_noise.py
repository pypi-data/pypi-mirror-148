#!/usr/bin/env python3

from opensimplex import OpenSimplex
import random as rand

# add parent dir to syspath
import sys
import pathlib
dir_path = pathlib.Path(__file__).parent.resolve()
sys.path.append(f"{dir_path}/..")

import hunter_pkg.map_generator as mapgen


def main():
    height = 50
    width = 38
    zoom = 0.3

    map = mapgen.generate(height, width, zoom)
    map.render()


if __name__ == "__main__":
    main()
