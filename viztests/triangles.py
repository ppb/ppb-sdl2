"""
An array of sprites using different aspect ratios in various colors on a black background.

Order:

______________________________________________________________
|    shape  || tall         | wide         | square          |
--------------------------------------------------------------
| rectangle || tall_rect    | wide_rect    | square          |
| triangle  || tall_tri     | wide_tri     | square_tri
| ellipse   || tall_ellipse | wide_ellipse | circle          |
______________________________________________________________
"""

from ppb import Vector, GameEngine, Scene, RectangleSprite
from ppb_sdl2.assets import Rectangle, Square, Triangle, Ellipse, Circle
from ppb_sdl2.sprites import Sprite
from ppb_sdl2.systems import Image, Renderer, EventPoller


class RSprite(Sprite, RectangleSprite):
    pass


def setup(scene):
    scene.background_color = (0, 0, 0)
    scene.add(RSprite(
        width=0.5, height=1,
        image=Rectangle(200, 0, 0, (1, 2)), position=(-2, 2)))
    scene.add(RSprite(
        width=1, height=0.5,
        image=Rectangle(100, 200, 0, (2, 1)), position=(0, 2)))
    scene.add(Sprite(size=1,
                     image=Square(200, 200, 100), position=(2, 2)))
    scene.add(RSprite(
        width=0.5, height=1,
        image=Triangle(0, 200, 0, (1, 2)), position=(-2, 0)))
    scene.add(RSprite(
        width=1, height=0.5,
        image=Triangle(0, 200, 100, (2, 1)), position=(0, 0)))
    scene.add(Sprite(image=Triangle(50, 200, 150), position=(2, 0)))
    scene.add(RSprite(
        width=0.5, height=1,
        image=Ellipse(0, 0, 200, (1, 2)), position=(-2, -2)))
    scene.add(RSprite(
        width=1, height=0.5,
        image=Ellipse(100, 0, 200, (2, 1)), position=(0, -2)))
    scene.add(Sprite(image=Circle(150, 50, 200), position=(2, -2)))


with GameEngine(Scene, systems=[EventPoller, Renderer], scene_kwargs={"set_up": setup}, resolution=(800, 600)) as eng:
    eng.run()
