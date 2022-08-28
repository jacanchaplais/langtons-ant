#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from pathlib import Path
from typing import Tuple, BinaryIO

import click
import numpy as np

from . import Ant, array_to_img, make_gif, Direction


@click.command()
@click.argument("max-steps", type=click.IntRange(10, 10_000, clamp=True))
@click.argument("output", type=click.File("wb"))
@click.option("--init", default="white", show_default=True,
              type=click.Choice(["black", "white", "noise"],
                                case_sensitive=False))
@click.option("--res", nargs=2, default=(1000, 1000),
              type=click.IntRange(100, None, clamp=True), show_default=True)
@click.option("--grid-size", nargs=2, default=(250, 250),
              type=click.IntRange(10, None, clamp=True), show_default=True)
def main(max_steps: int, output: BinaryIO, init: str, res: Tuple[int, int],
         grid_size: Tuple[int, int]) -> None:
    bound_x, bound_y = grid_size
    grid = np.zeros((bound_x, bound_y), dtype="<?")
    if init == "white":
        grid[...] = True
    elif init == "noise":
        rng = np.random.default_rng()
        grid = rng.integers(0, 2, size=(bound_x, bound_y), dtype="<?")
    ant = Ant(bound_x // 2, bound_y // 2, Direction.RIGHT)
    images = []
    
    count = 0
    while ((ant.x < bound_x) and (ant.x > 0)
           and (ant.y < bound_y) and (ant.y > 0)
           and (count <= max_steps)):
        x, y = ant.x, ant.y
        cell_val = grid[y, x]
        ant.move(cell_val)
        grid[y, x] = ~cell_val
        images.append(array_to_img(grid, *res))
        count = count + 1

    make_gif(output, images)


if __name__ == "__main__":
    sys.exit(main())
