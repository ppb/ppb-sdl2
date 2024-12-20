"""
Tests rotation vs Vector angles

The center sprite should always face the orbiting sprite, and they should be
moving counter-clockwise.
"""
from ppb import Vector, GameEngine, Scene
from ppb_sdl2.sprites import Sprite
from ppb_sdl2.systems import Image, Renderer, EventPoller

ROTATION_RATE = 90


class CenterSprite(Sprite):
    image = Image('player.png')

    def on_update(self, event, signal):
        self.rotate(ROTATION_RATE * event.time_delta)


class OrbitSprite(Sprite):
    position = Vector(0, -2)
    image = Image('target.png')

    def on_update(self, event, signal):
        self.position = self.position.rotate(ROTATION_RATE * event.time_delta)


def setup(scene):
    scene.add(CenterSprite())
    scene.add(OrbitSprite())


with GameEngine(Scene, systems=[EventPoller, Renderer], scene_kwargs={"set_up": setup}, resolution=(800, 600)) as eng:
    eng.run()