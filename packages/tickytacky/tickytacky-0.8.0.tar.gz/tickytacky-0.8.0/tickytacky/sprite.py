import json
from flask import Flask, render_template
import logging

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__, template_folder="../tools/")


@app.route('/')
def sprite_maker():
    return render_template('sprite_maker16.html')


@app.route('/spriteOutput.html')
def sprite_output():
    return render_template('spriteOutput.html')


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


if __name__ == "__main__":
    app.run(host="0.0.0.0")
