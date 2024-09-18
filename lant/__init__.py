import enum
import typing as ty
from dataclasses import dataclass
from pathlib import Path
from contextlib import contextmanager

import numpy as np
import numpy.typing as npt
import cv2


BoolVector = npt.NDArray[np.bool_]
Uint8Vector = npt.NDArray[np.uint8]


def create_grid(
    dims: tuple[int, int], init: ty.Literal["white", "black", "noise"]
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


def array_as_frame(array: BoolVector) -> Uint8Vector:
    return array.view(np.uint8) * 255


@contextmanager
def video_writer(path: Path, codec: str, rate: int, res: tuple[int, int]):
    fourcc = cv2.VideoWriter_fourcc(*codec)
    video_file = cv2.VideoWriter(str(path), fourcc, rate, res, isColor=False)
    try:
        yield video_file
    finally:
        video_file.release()


class Direction(enum.IntEnum):
    """Angular direction, in units of PI / 2."""
    UP = enum.auto()
    RIGHT = enum.auto()
    DOWN = enum.auto()
    LEFT = enum.auto()

    def clockwise(self: ty.Self) -> ty.Self:
        cls, value = type(self), self.value
        if value == len(cls):
            return cls(1)
        return cls(value + 1)

    def anticlockwise(self: ty.Self) -> ty.Self:
        cls, value = type(self), self.value
        if value == 1:
            return cls(len(cls))
        return cls(value - 1)


@dataclass(slots=True)
class Ant:
    x: int
    y: int
    angle: Direction

    def move(self, grid: BoolVector) -> BoolVector:
        cell = grid[self.y, self.x]
        grid[self.y, self.x] = ~cell
        if cell:
            self.angle = self.angle.clockwise()
        else:
            self.angle = self.angle.anticlockwise()
        match self.angle:
            case Direction.UP:
                self.y -= 1
            case Direction.DOWN:
                self.y += 1
            case Direction.LEFT:
                self.x -= 1
            case Direction.RIGHT:
                self.x += 1
        return grid

    def bounded(self, bound_x: int, bound_y: int) -> bool:
        if (not (0 <= self.x < bound_x)) or (not (0 <= self.y < bound_y)):
            return False
        return True
