#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from dataclasses import dataclass
from enum import Enum

import click

import numpy as np


class Direction(Enum):
    RIGHT = 0
    DOWN = 90
    LEFT = 180
    UP = 270


@dataclass(slots=True)
class Ant:
    x: int
    y: int
    _angle: Direction

    def move(self, cell: bool) -> None:
        # direction change
        if cell:
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


@click.command()
def main() -> None:
    grid = np.zeros((1000, 1000), dtype="<?")
    ant = Ant(500, 500, Direction.RIGHT)

    while True:
        try:
            cell_value = grid[ant.x, ant.y]
            ant.move(cell_value)
            grid[ant.x, ant.y] = ~cell_value
        except IndexError:
            break


if __name__ == '__main__':
    sys.exit(main())
