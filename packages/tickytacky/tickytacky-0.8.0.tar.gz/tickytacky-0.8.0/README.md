# Tickytacky

[![tickytacky pypi shield](https://img.shields.io/pypi/v/tickytacky)](https://pypi.org/project/tickytacky/)

## Description

This library aims to make it easy to make retro-style games with Pyglet.

## Examples

Examples can be found here, in the examples, repo:

[Tickytacky Examples](https://github.com/numbertheory/tickytacky-examples)

## Sprite Maker

The sprite library contains a small Flask app you can run to assist with making
sprites.

Example:
```
python tickytacky/sprite.py
```

1. Select colors from the large color button. It's an HTML5 color selector, so it will
use your system's color picker to select any color.

2. Click the "Create Color option" to add it to the palette.

3. Choose that color from the palette options and draw with it. By default, the color name
will show as undefined, but you can change that in the text box.

4. If you remove a color from the palette, all pixels with that color will also be removed.

5. When done drawing, name the sprite and click the "Export" button. This will create a
new page which will show the JSON format for the sprite you drew.

6. Copy that info into a JSON file in your game.
