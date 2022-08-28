from dataclasses import dataclass
from enum import Enum
from typing import List, BinaryIO, Union
from pathlib import Path

from PIL import Image
import numpy as np


def array_to_img(array: np.ndarray, width: int, height: int) -> Image.Image:
    return Image.fromarray(array).convert("P").resize((width, height))
                

def make_gif(path: Union[Path, BinaryIO], images: List[Image.Image]) -> None:
    images[0].save(
            path, save_all=True, append_images=images[1:], optimize=False,
            duration=40, loop=0)


class Direction(Enum):
    RIGHT = 0
    DOWN = 90
    LEFT = 180
    UP = 270


@dataclass
class Ant:
    __slots__ = "x", "y", "_angle"
    x: int
    y: int
    _angle: Direction

    def move(self, cell: bool) -> None:
        # direction change
        if cell == True:
            self.angle = self.angle.value + 90
        else:
            self.angle = self.angle.value - 90
        # movement
        if self.angle == Direction.RIGHT:
            self.x += 1
        elif self.angle == Direction.DOWN:
            self.y += 1
        elif self.angle == Direction.LEFT:
            self.x -= 1
        elif self.angle == Direction.UP:
            self.y -= 1

    @property
    def angle(self) -> Direction:
        return self._angle

    @angle.setter
    def angle(self, val: int) -> None:
        self._angle = Direction(val % 360)
