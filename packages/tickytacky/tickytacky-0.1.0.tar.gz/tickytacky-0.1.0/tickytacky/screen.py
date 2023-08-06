import pyglet
from pyglet import shapes


class Screen(pyglet.window.Window):
    def __init__(self, width=240, height=160,
                 factor=6, title="NoName", fixed=False,
                 pixel_sprites=[]):
        super().__init__(width*factor, height*factor, title)
        self.time = 0
        self.batch = pyglet.graphics.Batch()
        self.height = height
        self.width = width
        self.factor = factor
        self.title = title
        self.pixel = []
        self.sprites = dict()
        for sprite in pixel_sprites:
            self.sprites[sprite["name"]] = {
                "name": sprite.get("name"),
                "data": sprite.get("data"),
                "location": sprite.get("location")}

        if fixed:
            super().set_maximum_size(width*factor, height*factor)
            super().set_minimum_size(width*factor, height*factor)

    def pixel_system(self, x, y):
        _width = self.width - 1
        _height = self.height - 1
        _x = x * self.factor
        _y = ((y*-1 + 159) * self.factor)
        f = self.factor
        return [(_width * f) - _width * f + _x,
                (_height * f) - _height * f + _y]

    def set_pixel(self, pixel, color):
        pixel = self.pixel_system(pixel[0], pixel[1])
        if not color:
            return None
        else:
            self.pixel.append(shapes.Rectangle(
                              pixel[0],
                              pixel[1],
                              self.factor, self.factor,
                              color=color, batch=self.batch))

    def add_sprite(self, name, location):
        self.pixel = []
        palette = self.sprites[name]["data"].get("palette")
        shape = self.sprites[name]["data"].get("shape", [])
        max_row_size = 0
        if self.sprites[name]["location"]:
            for r in range(0, len(shape)):
                for c in range(0, len(shape[r])):
                    if max_row_size < len(shape[r]):
                        max_row_size = len(shape[r])
                    self.set_pixel(pixel=(location[0] + c, location[1] + r),
                                   color=palette.get(shape[r][c]))
        self.sprites[name]["location"] = [location[0], location[1]]
        self.batch.draw()

    def on_draw(self):
        """Clear the screen and draw shapes"""
        self.clear()
        self.batch.draw()
