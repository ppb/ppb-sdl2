import concurrent.futures
import gc
import time

import pytest

from ppb import GameEngine, Scene
import ppb.events
import ppb.assetlib
from ppb.assetlib import (
    DelayedThreadExecutor, Asset, AssetLoadingSystem, BackgroundMixin,
    ChainingMixin, AbstractAsset,
)
from ppb.testutils import Failer


@pytest.fixture
def clean_assets():
    """
    Cleans out the global state of the asset system, so that we start fresh every
    test.
    """
    # Note that while AssetLoadingSystem cleans stuff up when it exits, this
    # makes sure that the tests start fresh.
    ppb.assetlib._executor = DelayedThreadExecutor()


class AssetTestScene(Scene):
    def on_asset_loaded(self, event, signal):
        self.ale = event
        signal(ppb.events.Quit())


def test_executor(clean_assets):
    # Can't easily test the cancellation, since jobs in progress can't be cancelled.
    def work():
        return "spam"

    pool = DelayedThreadExecutor()
    assert not pool._threads

    fut = pool.submit(work)
    time.sleep(0.01)  # Let any hypothetical threads do work
    assert not pool._threads
    assert not (fut.done() or fut.running())

    with pool:
        assert fut.result() == "spam"

    assert pool._shutdown


# def test_loading_root():
#     a = Asset(...)  # TODO: find a cross-platform target in $VENV/bin
#     engine = GameEngine(Scene, basic_systems=[AssetLoadingSystem])
#     with engine:
#         engine.start()

#         assert a.load()


def test_missing_package(clean_assets):
    a = Asset('does/not/exist')
    engine = GameEngine(
        AssetTestScene, basic_systems=[AssetLoadingSystem, Failer],
        fail=lambda e: False, message=None, run_time=1,
    )
    with engine:
        engine.start()

        with pytest.raises(FileNotFoundError):
            assert a.load()


def test_missing_resource(clean_assets):
    a = Asset('ppb_sdl2/dont.touch.this')
    engine = GameEngine(
        AssetTestScene, basic_systems=[AssetLoadingSystem, Failer],
        fail=lambda e: False, message=None, run_time=1,
    )
    with engine:
        engine.start()

        with pytest.raises(FileNotFoundError):
            assert a.load()


def test_missing_parse(clean_assets):
    class Const(Asset):
        def file_missing(self):
            return "igotu"

    a = Const('spam/eggs')
    engine = GameEngine(
        AssetTestScene, basic_systems=[AssetLoadingSystem, Failer],
        fail=lambda e: False, message=None, run_time=1,
    )
    with engine:
        engine.start()

        assert a.load() == "igotu"


def test_free(clean_assets):
    free_called = False

    class Const(Asset):
        def background_parse(self, data):
            return "yoink"

        def free(self, obj):
            nonlocal free_called
            free_called = True

    a = Const('ppb_sdl2/utils.py')
    engine = GameEngine(
        AssetTestScene, basic_systems=[AssetLoadingSystem, Failer],
        fail=lambda e: False, message=None, run_time=1,
    )
    with engine:
        engine.start()

        assert a.load() == "yoink"
        # At this poiint, background processing should have finished

    del engine, a  # Clean up everything that might be holding a reference.
    gc.collect()
    assert free_called


def test_timeout(clean_assets):
    a = Asset('ppb_sdl2/utils.py')

    with pytest.raises(concurrent.futures.TimeoutError):
        a.load(timeout=0.1)


def test_chained(clean_assets):
    class Const(BackgroundMixin, AbstractAsset):
        def __init__(self, value):
            self.value = value
            self._start()

        def _background(self):
            return self.value

    class Concat(ChainingMixin, AbstractAsset):
        def __init__(self, delimiter, *values):
            self.delimiter = delimiter
            self.values = values
            self._start(*values)

        def _background(self):
            return self.delimiter.join(a.load() for a in self.values)

    a = Concat(
        ' ',
        Const("spam"), Const("eggs"), Const("foo"), Const("bar"),
    )
    engine = GameEngine(
        AssetTestScene, basic_systems=[AssetLoadingSystem, Failer],
        fail=lambda e: False, message=None, run_time=1,
    )
    with engine:
        engine.start()

        assert a.load() == "spam eggs foo bar"


def test_chained_big(clean_assets):
    class Concat(ChainingMixin, AbstractAsset):
        def __init__(self, delimiter, *values):
            self.delimiter = delimiter
            self.values = values
            self._start(*values)

        def _background(self):
            return self.delimiter.join(a.load() for a in self.values)

    a = Concat(
        b'\n',
        *(
            Asset(f"ppb_sdl2/{fname}")
            for fname in ppb.vfs.iterdir('ppb_sdl2')
            if ppb.vfs.exists(f"ppb_sdl2/{fname}")
        )
    )
    engine = GameEngine(
        AssetTestScene, basic_systems=[AssetLoadingSystem, Failer],
        fail=lambda e: False, message=None, run_time=1,
    )
    with engine:
        engine.start()

        assert a.load(timeout=5)
