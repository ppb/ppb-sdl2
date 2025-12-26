"""Provide floats for color arguments. Shouldn't crash"""

from ppb import GameEngine, Scene
from ppb_sdl2.assets import Square
from ppb_sdl2.sprites import Sprite
from ppb_sdl2.systems import Image, Renderer, EventPoller


class MyScene(Scene):
    background_color = (200.5, 125.6, 127.8)


def setup(scene):
    scene.add(Sprite(image=Square(123.5, 200.8, 156.22)))


with GameEngine(MyScene, systems=[EventPoller, Renderer], scene_kwargs={"set_up": setup}, resolution=(800, 600)) as eng:
    eng.run()