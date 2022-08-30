# Langton's Ant

An implementation of [Langton's Ant][wiki] in Python for fun.

## Installation

```bash
pip install lant
```

### Dependencies

Requires `Python>=3.8`. For faster video writing, consider installing the
conda environment, using `environment.yml` from the root of the git repo:

```bash
conda env create -f environment.yml
```

or installing `opencv=4.6.0` into your existing virtual environment.
The package shipped with PyPI does not use GPU acceleration.

## Usage

To get started, you may invoke the program with:

```bash
ant-walk 100000 output.mp4
```

This produces the evolution of the ant on the grid until it walks over the
edge, or the maximum number of steps is met, in this case 100k.

For more advanced usage, see the helptext:

```bash
ant-walk --help
```

[wiki]: https://en.wikipedia.org/wiki/Langton%27s_ant
