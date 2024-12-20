"""
"""
from ppb import Vector, GameEngine, Scene, RectangleSprite
from ppb_sdl2.assets import Square
from ppb_sdl2.sprites import Sprite
from ppb_sdl2.systems import Image, Renderer, EventPoller


class Square(Sprite, RectangleSprite):
    width = 1
    height = 4

    image = Square(0, 0, 255)


class Tall(Sprite, RectangleSprite):
    width = 2
    height = 4

    image = Image('resources/tall.png')


class Wide(Sprite, RectangleSprite):
    width = 4
    height = 2

    image = Image('resources/wide.png')


def setup(scene):
    scene.add(Square(position=(0, 0)))
    scene.add(Wide(position=(0, 4)))
    scene.add(Tall(position=(4, 0)))


with GameEngine(Scene, systems=[EventPoller, Renderer], scene_kwargs={"set_up": setup}, resolution=(800, 600)) as eng:
    eng.run()
