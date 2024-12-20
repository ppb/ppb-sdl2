"""
Tests that sprites drawn with the square primitive default rotate correctly.

Verify that the square rotates and doesn't resize.
"""
from ppb import Vector, GameEngine, Scene, events
from ppb_sdl2.sprites import Sprite
from ppb_sdl2.systems import Image, Renderer, EventPoller


class Square(Sprite):
    degrees_per_second = 180

    def on_update(self, update: events.Update, signal):
        self.rotate(self.degrees_per_second * update.time_delta)


def setup(scene):
    scene.add(Square())


with GameEngine(Scene, systems=[EventPoller, Renderer], scene_kwargs={"set_up": setup}, resolution=(800, 600)) as eng:
    eng.run()