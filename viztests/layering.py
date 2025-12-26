"""
Visual test of the layering system.

The grey circle mover should render above the purple up arrows and below
the yellow down arrows.
"""
from itertools import cycle

from ppb import Vector, events, GameEngine, Scene
from ppb_sdl2.sprites import Sprite
from ppb_sdl2.systems import Image, Renderer, EventPoller


class Mover(Sprite):
    image = Image("resources/mover.png")
    position = Vector(0, -4)
    velocity = Vector(0, 3)

    def on_update(self, update: events.Update, signal):
        self.position += self.velocity * update.time_delta
        if self.position.y > 4 or self.position.y < -4:
            self.velocity *= -1


class TravelOver(Sprite):
    image = Image("resources/travel_over.png")
    layer = -1


class TravelUnder(Sprite):
    image = Image("resources/travel_under.png")
    layer = 1


def setup(scene):
    print(f"setup {scene=}")
    scene.add(Mover())
    for x, klass in zip(range(-3, 4), cycle((TravelOver, TravelUnder))):
        scene.add(klass(position=Vector(0, x)))


with GameEngine(Scene, systems=[EventPoller, Renderer], scene_kwargs={"set_up": setup}, resolution=(800, 600)) as eng:
    eng.run()