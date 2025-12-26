from ppb import Vector, GameEngine, Scene
from ppb_sdl2.sprites import Sprite
from ppb_sdl2.systems import Image, Renderer, EventPoller, Font, Text

font = Font("resources/ubuntu_font/Ubuntu-R.ttf", size=72)
my_first_text = Text("My first text", font=font, color=(255, 255, 255))
my_second_text = Text("My second text", font=font, color=(255, 255, 255))


def setup(scene):
    scene.add(Sprite(image=my_first_text))
    scene.add(Sprite(image=my_second_text, position=Vector(0, -2)))


with GameEngine(Scene, systems=[EventPoller, Renderer], scene_kwargs={"set_up": setup}, resolution=(800, 600)) as eng:
    eng.run()