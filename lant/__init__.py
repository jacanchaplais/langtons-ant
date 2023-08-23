from dataclasses import dataclass
from enum import Enum
from typing import Tuple, Literal
from pathlib import Path
from contextlib import contextmanager

import numpy as np
import numpy.typing as npt
import cv2


BoolVector = npt.NDArray[np.bool_]
Uint8Vector = npt.NDArray[np.uint8]


def create_grid(
    dims: Tuple[int, int], init: Literal["white", "black", "noise"]
) -> BoolVector:
    dtype = np.bool_
    if init == "white":
        return np.ones(dims, dtype=dtype)
    if init == "black":
        return np.zeros(dims, dtype=dtype)
    if init == "noise":
        rng = np.random.default_rng()
        return rng.integers(0, 2, size=dims, dtype=dtype)
    raise ValueError(f"{init=} is not a recognised value")


def array_as_frame(array: BoolVector, scale: int) -> Uint8Vector:
    frame = array.view(np.uint8) * 255
    return np.repeat(np.repeat(frame, scale, axis=0), scale, axis=1)


@contextmanager
def video_writer(path: Path, codec: str, rate: int, res: Tuple[int, int]):
    fourcc = cv2.VideoWriter_fourcc(*codec)
    video_file = cv2.VideoWriter(str(path), fourcc, rate, res, False)
    try:
        yield video_file
    finally:
        video_file.release()


class Direction(Enum):
    """Angular direction, in units of PI / 2."""
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3


@dataclass
class Ant:
    __slots__ = "x", "y", "_angle"
    x: int
    y: int
    _angle: Direction

    def move(self, grid: BoolVector) -> BoolVector:
        cell = grid[self.y, self.x]
        grid[self.y, self.x] = ~cell
        # direction change
        if cell:
            self.angle = self.angle.value + 1
        else:
            self.angle = self.angle.value - 1
        # movement
        if self.angle == Direction.RIGHT:
            self.x += 1
        elif self.angle == Direction.DOWN:
            self.y += 1
        elif self.angle == Direction.LEFT:
            self.x -= 1
        else:
            self.y -= 1
        # release the updated grid
        return grid

    @property
    def angle(self) -> Direction:
        return self._angle

    @angle.setter
    def angle(self, val: int) -> None:
        self._angle = Direction(val % 4)

    def bounded(self, bounds: Tuple[int, int]) -> bool:
        by, bx = bounds
        return ((self.x >= 0) and (self.x < bx)
                and (self.y >= 0) and (self.y < by))
