"""
Tests the sound system without initializing anything else.

NOTE: Does not open a window.
"""
from ppb import GameEngine, Scene, events
from ppb_sdl2.systems import SoundController, Sound


class SoundScene(Scene):
    sound = Sound("laser1.ogg")
    running = 0
    lifespan = 2

    def on_scene_started(self, event, signal):
        print("Scene start")
        signal(events.PlaySound(sound=self.sound))

    def on_update(self, event, signal):
        self.running += event.time_delta
        if self.running > self.lifespan:
            signal(events.Quit())


with GameEngine(SoundScene, systems=[SoundController], resolution=(800, 600)) as eng:
    eng.run()
