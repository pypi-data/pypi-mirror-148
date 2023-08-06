from hunter_pkg import colors


class Fog():
    def get_graphic_dt(self):
        return (ord(" "), colors.black, colors.black)

instance = Fog()