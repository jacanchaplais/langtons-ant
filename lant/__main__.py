#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import typing as ty
from pathlib import Path

import click
from tqdm import tqdm

from . import Ant, Direction, video_writer, array_as_frame, create_grid


@click.command()
@click.argument("max-steps", type=click.IntRange(1, None))
@click.argument("output", type=click.Path(readable=False, writable=True,
                                          path_type=Path))
@click.option("--init", default="white", show_default=True,
              type=click.Choice(["black", "white", "noise"],
                                case_sensitive=False))
@click.option("--grid-size", nargs=2, default=(250, 250),
              type=click.IntRange(10, None, clamp=True), show_default=True)
@click.option("--rate", type=click.INT, default=300, show_default=True)
def main(
    max_steps: int,
    output: Path,
    init: ty.Literal["white", "black", "noise"],
    grid_size: tuple[int, int],
    rate: int
) -> None:
    if output.exists() and not click.confirm(f"{output} exists! Overwrite?"):
        raise click.Abort()
    bound_y, bound_x = grid_size
    grid = create_grid(grid_size, init)
    ant = Ant(bound_x // 2, bound_y // 2, Direction.RIGHT)
    with video_writer(output, "FFV1", rate, grid_size) as video_file:
        for _ in tqdm(range(max_steps)):
            if not ant.bounded(bound_x, bound_y):
                break
            grid = ant.move(grid)
            video_file.write(array_as_frame(grid))


if __name__ == "__main__":
    sys.exit(main())
