"""
Tests primitive asset types: Square, Circle, and Triangle.

Should display a red square in the bottom left, a black triangle up, and a
magenta circle bottom right.
"""
from ppb import Vector, GameEngine, Scene, events
from ppb_sdl2.assets import Square, Triangle, Circle
from ppb_sdl2.sprites import Sprite
from ppb_sdl2.systems import Image, Renderer, EventPoller


class Rotating(Sprite):
    """
    A rotating sprite.
    """
    degrees_per_second = 90

    def on_update(self, event: events.Update, signal):
        self.rotate(event.time_delta * self.degrees_per_second)


class Square(Rotating):
    image = Square(255, 50, 75)


class Triangle(Rotating):
    image = Triangle(0, 0, 0)


class Circle(Rotating):
    image = Circle(255, 71, 182)


def setup(scene):
    scene.background_color = (160, 155, 180)
    scene.add(Square(position=Vector(-2, 0)))
    scene.add(Triangle(position=Vector(0, 2)))
    scene.add(Circle(position=Vector(2, 0)))


with GameEngine(Scene, systems=[EventPoller, Renderer], scene_kwargs={"set_up": setup}, resolution=(800, 600)) as eng:
    eng.run()
