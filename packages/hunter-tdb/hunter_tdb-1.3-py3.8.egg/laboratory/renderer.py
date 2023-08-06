import numpy as np

from hunter_pkg.helpers import layers


class Renderer():
    def __init__(self, map_height, map_width):
        self.layer_order = [
            layers.UI,
            layers.FOG,
            layers.CREATURES,
            layers.TERRAIN
        ]
        self.layers = {}
        self.map_width = map_width
        self.map_height = map_height

        for layer_name in self.layer_order:
            self.layers[layer_name] = []
            for y in range(self.map_height):
                self.layers[layer_name].append([])

                for x in range(self.map_width):
                    self.layers[layer_name][y].append(None)

    def place(self, _type, _object, x, y):
        self.layers[_type][y][x] = _object

    def remove(self, _type, x, y):
        self.layers[_type][y][x] = None

    def get(self, _type, x, y):
        return self.layers[_type][y][x]

    def fill(self, _type, _object):
        for y, row in enumerate(self.layers[_type]):
            for x, v in enumerate(row):
                row[x] = _object

class UIElement():
    pass

class Fog():
    pass

class Hunter():
    pass

class TestObj():
    pass


def main():
    height = 50
    width = 38

    renderer = Renderer(height, width)

    ui_elem = UIElement()
    foggy_cell = Fog()
    hunter = Hunter()
    test_obj = TestObj()

    renderer.fill(layers.FOG, foggy_cell)
    renderer.remove(layers.FOG, 5, 5)
    renderer.place(layers.CREATURES, test_obj, 3, 3)
    renderer.place(layers.TERRAIN, test_obj, 3, 3)
    #renderer.render()

    print(renderer.get(layers.FOG, 0, 3) != None)
    print(renderer.get(layers.FOG, 5, 5) == None)
    print(renderer.get(layers.FOG, 30, 27) != None)
    print(renderer.get(layers.CREATURES, 3, 3) == renderer.get(layers.TERRAIN, 3, 3))

    renderer.remove(layers.CREATURES, 3, 3)
    print(renderer.get(layers.CREATURES, 3, 3) == None)
    print(renderer.get(layers.TERRAIN, 3, 3) == test_obj)


if __name__ == "__main__":
    main()
