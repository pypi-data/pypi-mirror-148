import json


class Sprite():
    def __init__(self, sprite_files=[]):
        self.pixel_sprites = []
        for sprite_file in sprite_files:
            data = self.load_sprite_file(sprite_file)
            self.pixel_sprites.append(
                {"name": data.get("name"),
                 "data": data}
            )

    def load_sprite_file(self, file):
        with open(file, "r") as json_file:
            sprite = json.load(json_file)
        return sprite
