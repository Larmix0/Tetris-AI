"""Module that stores constants which are used over multiple files.

INVIS_GRID_TOP (int):
    How many invisible rows are above the 20x10 grid (in order to create the piece inside it).

IS_MAIN_PROCESS (bool):
    tells us whether we're importing modules with main process or a child process.
    This is mostly to evade importing pygame multiple times whenever we create a child process.
"""

from multiprocessing import current_process
from enum import Enum, auto

from .pieces import S, Z, I, O, J, L ,T

ROWS = 10
COLS = 20
INVIS_GRID_TOP = 3

IS_MAIN_PROCESS = current_process().name == "MainProcess"


class Pieces:
    """Has all piece types aligned by index."""
    SHAPES = (S, Z, I, O, J, L, T)
    COLORS = ("green", "red", "cyan", "yellow", "blue", "orange", "purple")
    GHOST_COLORS = ("#007d00", "#910000", "#008e8e", "#a1a100", "#00009d", "#965900", "#550099")


class AiMultipliers:
    """Has constant multipliers for all ai.py evaluations."""
    HEIGHT = -0.25
    EMPTY_PILLARS = -1
    BUMPINESS = -0.1

    OPEN_HOLE = -0.4
    CLOSED_HOLE = -1.2
    ROWS_WITH_HOLES = -0.4


class Movement(Enum):
    """Ai movement representation."""
    ROTATION = auto()
    DOWN = auto()
    RIGHT = auto()
    LEFT = auto()
    DROP = auto()


class GridBlock(Enum):
    """Represents what a block/square on the grid is

    On a 2d tetris grid ACTIVE is occupied by a currently active piece, EMPTY is for an empty square,
    and PREVIOUS is for a square taken by the previous piece we placed (only important for ai).
    """
    ACTIVE = auto()
    EMPTY = auto()
    PREVIOUS = auto()
