"""
A Renderable Mixin for rendering with ppb_sdl2.
"""
from inspect import getfile
from pathlib import Path

import ppb_sdl2.systems
import ppb.gomlib

__all__ = (
    "RenderableMixin",
    "Sprite",
)


class RenderableMixin:
    """
    A class implementing the API expected by ppb_sdl2.systems.renderer.Renderer.

    The render expects a width and height (see :class:`RectangleMixin`) and will
    skip rendering if a sprite has no shape. You can use
    :class:`RectangleMixin`, :class:`SquareMixin`, or set the values yourself.

    Additionally, if :attr:`~RenderableMixin.image` is ``None``, the sprite will not
    be rendered. If you just want a basic shape to be rendered, see
    :mod:`ppb_sdl2.assets`.
    """
    #: (:py:class:`ppb_sdl2.Image`): The image asset
    image = ...  # TODO: Type hint appropriately
    size = 1
    blend_mode: 'ppb_sdl2.flags.BlendMode' # One of four blending modes
    opacity: int # An opacity value from 0-255
    tint: 'ppb_sdl2.utils.Color' # A 3-tuple color with values 0-255

    def __image__(self):
        """
        Returns the sprite's image attribute if provided, or sets a default
        one.
        """
        if self.image is ...:
            klass = type(self)
            prefix = Path(klass.__module__.replace('.', '/'))
            try:
                klassfile = getfile(klass)
            except TypeError:
                prefix = Path('.')
            else:
                if Path(klassfile).name != '__init__.py':
                    prefix = prefix.parent
            if prefix == Path('.'):
                self.image = ppb_sdl2.systems.Image(f"{klass.__name__.lower()}.png")
            else:
                self.image = ppb_sdl2.systems.Image(f"{prefix!s}/{klass.__name__.lower()}.png")
        return self.image


class Sprite(RenderableMixin, ppb.Sprite):
    """The basic ppb Sprite with rendering details."""
    pass
