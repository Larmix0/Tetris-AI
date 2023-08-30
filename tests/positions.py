from copy import deepcopy

from src.constants import INVIS_GRID_TOP, AiMultipliers, Movement, GridBlock as GB
from src.classes import Piece

"""Module that holds positions to be used in tests.

The reason I made this:
    it was because the positions used for testing
    as you can see are absolutely massive (especially because of the grid).
    So I decided to put all the positions in this one module instead.

Attributes:
    PLACED_POSITIONS (list[dict]): positions where active piece is already placed on the grid.
    UNPLACED_POSITIONS (list[dict]): positions where active piece hasn't been created on the grid.
    AI_HELPERS_POSITIONS (list[dict]): positions specifically for ai.py's helper function's tests.
"""


def tetris_to_dict(tetris, inputs=None):
    """Returns a dictionary from class which stores information about a tetris position."""
    if inputs is None:
        inputs = []
    return {
        "x": tetris.piece_x,
        "y": tetris.piece_y,
        "rotation": tetris.rotation,
        "grid": deepcopy(tetris.grid),
        "inputs": inputs
    }


# Dynamically sized padding for the invisible grid top
GRID_TOP = [[GB.EMPTY] * 10 for _ in range(INVIS_GRID_TOP)]

# Positions where a piece is already placed and ready to be killed
PLACED_POSITIONS = [
    {
        "pieces": {
            "current": Piece(4),
            "next": Piece(0)
        },
        "position": {
            "x": -1,
            "y": INVIS_GRID_TOP + 14,
            "rotation": 1,
            "inputs": [],
            "grid": GRID_TOP + [
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, "green", GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, "green", "green", GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, "green", GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, "blue", "blue", GB.EMPTY, "orange", GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, "blue", GB.EMPTY, GB.EMPTY, "orange", GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.ACTIVE, GB.ACTIVE, "blue", GB.EMPTY, GB.EMPTY, "orange", "orange", GB.EMPTY, GB.EMPTY],
                ["orange", GB.ACTIVE, "yellow", "yellow", GB.EMPTY, "red", "red", GB.EMPTY, GB.EMPTY, "cyan"],
                ["orange", GB.ACTIVE, "yellow", "yellow", GB.EMPTY, GB.EMPTY, "red", "red", GB.EMPTY, "cyan"],
                ["orange", "orange", "purple", GB.EMPTY, GB.EMPTY, GB.EMPTY, "purple", GB.EMPTY, GB.EMPTY, "cyan"],
                [GB.EMPTY, "purple", "purple", "purple", GB.EMPTY, "purple", "purple", "purple", GB.EMPTY, "cyan"]
            ]
        },
        "test info": {
            "open holes": 10,
            "closed holes": 3,
            "rows with holes": 7,
            "height": 4,
            "structure height": INVIS_GRID_TOP + 10,
            "bumpiness": [i + INVIS_GRID_TOP for i in [16, 15, 15, 10, 11, 16, 13, 15, 20, 16]],
            "bumps": 26,
            "empty pillars": 2
        }
    },
    {
        "pieces": {
            "current": Piece(3),
            "next": Piece(1)
        },
        "position": {
            "x": 7,
            "y": -2,
            "rotation": 0,
            "inputs": [],
            "grid": GRID_TOP[:-1] + [  # we exclude last line of grid top cause this example has 2 blocks outside grid
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.ACTIVE, GB.ACTIVE],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.ACTIVE, GB.ACTIVE],
                [GB.EMPTY, "yellow", "yellow", GB.EMPTY, "blue", GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, "orange"],
                [GB.EMPTY, "yellow", "yellow", GB.EMPTY, "blue", "blue", "blue", "orange", "orange", "orange"],
                [GB.EMPTY, GB.EMPTY, "green", "green", "red", GB.EMPTY, GB.EMPTY, "purple", GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, "green", "green", "red", "red", GB.EMPTY, "purple", "purple", "purple", GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, "red", "cyan", "cyan", "cyan", "cyan", GB.EMPTY, GB.EMPTY],
                ["cyan", "cyan", "cyan", "cyan", GB.EMPTY, GB.EMPTY, GB.EMPTY, "blue", "blue", "blue"],
                [GB.EMPTY, GB.EMPTY, "orange", GB.EMPTY, GB.EMPTY, "red", GB.EMPTY, GB.EMPTY, "green", "blue"],
                [GB.EMPTY, GB.EMPTY, "orange", GB.EMPTY, "red", "red", "yellow", "yellow", "green", "green"],
                [GB.EMPTY, GB.EMPTY, "orange", "orange", "red", "purple", "yellow", "yellow", "green", "green"],
                [GB.EMPTY, GB.EMPTY, "red", "red", "purple", "purple", "purple", "orange", "green", "green"],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, "red", "red", GB.EMPTY, GB.EMPTY, "orange", GB.EMPTY, "green"],
                [GB.EMPTY, GB.EMPTY, "blue", "blue", "blue", GB.EMPTY, GB.EMPTY, "orange", "orange", "purple"],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, "purple", "blue", GB.EMPTY, GB.EMPTY, "cyan", "purple", "purple"],
                [GB.EMPTY, "yellow", "yellow", "purple", "purple", GB.EMPTY, GB.EMPTY, "cyan", GB.EMPTY, "purple"],
                [GB.EMPTY, "yellow", "yellow", "purple", "blue", GB.EMPTY, GB.EMPTY, "cyan", "yellow", "yellow"],
                [GB.EMPTY, "orange", "orange", "orange", "blue", GB.EMPTY, GB.EMPTY, "cyan", "yellow", "yellow"],
                [GB.EMPTY, "orange", "red", "blue", "blue", GB.EMPTY, "cyan", "cyan", "cyan", "cyan"],
                [GB.EMPTY, "red", "red", "green", "green", GB.EMPTY, GB.EMPTY, GB.EMPTY, "orange", GB.EMPTY],
                [GB.EMPTY, "red", "green", "green", GB.EMPTY, GB.EMPTY, "orange", "orange", "orange", GB.EMPTY]
            ]
        },
        "test info": {
            "open holes": 50,
            "closed holes": 14,
            "rows with holes": 18,
            "height": 20,
            "structure height": INVIS_GRID_TOP + 1,
            "bumpiness": [i + INVIS_GRID_TOP for i in [6, 1, 1, 3, 1, 2, 2, 2, -1, -1]],
            "bumps": 13,
            "empty pillars": 1
        }
    },
    {
        "pieces": {
            "current": Piece(2),
            "next": Piece(3)
        },
        "position": {
            "x": 3,
            "y": INVIS_GRID_TOP + 17,
            "rotation": 0,
            "inputs": [],
            "grid": GRID_TOP + [
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, "orange", "orange", "orange", GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, "orange", "yellow", "yellow", "blue"],
                [GB.EMPTY, "purple", GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, "purple", "yellow", "yellow", "blue"],
                ["purple", "purple", "purple", GB.EMPTY, GB.ACTIVE, GB.ACTIVE, GB.ACTIVE, GB.ACTIVE, "blue", "blue"]
            ]
        },
        "test info": {
            "open holes": 0,
            "closed holes": 0,
            "rows with holes": 0,
            "height": 0,
            "structure height": INVIS_GRID_TOP + 16,
            "bumpiness": [i + INVIS_GRID_TOP for i in [19, 18, 19, 20, 19, 19, 16, 16, 16, 17]],
            "bumps": 8,
            "empty pillars": 0
        }
    }
]

# Positions where the piece isn't placed
UNPLACED_POSITIONS = [
    {
        "pieces": {
            "current": Piece(2),
            "next": Piece(1),
        },
        "position": {
            "grid": GRID_TOP + [
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                ["yellow", "yellow", GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                ["yellow", GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                ["yellow", GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, "blue", "blue"],
                ["yellow", GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, "blue"],
                ["purple", "purple", "purple", GB.EMPTY, GB.EMPTY, GB.EMPTY, "orange", "orange", "orange", "blue"],
                ["purple", GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, "yellow", "yellow", "blue"],
                ["purple", "purple", "purple", GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, "yellow", "yellow", "blue"],
                ["purple", GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, "blue", "blue"]
            ]
        },
        "test info": {
            "placements": 27,
            "lowered y": INVIS_GRID_TOP + 6,
        }
    },
    {
        "pieces": {
            "current": Piece(6),
            "next": Piece(5)
        },
        "position": {
            "grid": GRID_TOP + [
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, "orange"],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, "orange"],
                ["yellow", GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, "blue", "blue"],
                ["yellow", GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, "orange", "blue"],
                ["purple", GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, "orange", "orange", "blue"],
                ["purple", GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, "yellow", "yellow", "blue"],
                ["purple", "purple", GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, "orange", "yellow", "yellow", "blue"],
                ["purple", "purple", GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, "orange", "orange", "blue", "blue"]
            ]
        },
        "test info": {
            "placements": 34,
            "lowered y": INVIS_GRID_TOP + 7
        }
    },
    {
        "pieces": {
            "current": Piece(3),
            "next": Piece(0)
        },
        "position": {
            "grid": GRID_TOP + [
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, "yellow", GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, "yellow", "yellow", GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, "yellow", "yellow", GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                ["yellow", "yellow", "yellow", GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                ["yellow", GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                ["yellow", GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, "yellow", "yellow", GB.EMPTY, GB.EMPTY, GB.EMPTY],
                ["yellow", GB.EMPTY, GB.EMPTY, "purple", "yellow", "yellow", GB.EMPTY, GB.EMPTY, GB.EMPTY, "orange"],
                ["yellow", GB.EMPTY, GB.EMPTY, "purple", "purple", GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, "orange"],
                ["yellow", GB.EMPTY, GB.EMPTY, GB.EMPTY, "purple", GB.EMPTY, GB.EMPTY, GB.EMPTY, "blue", "blue"],
                ["yellow", GB.EMPTY, GB.EMPTY, GB.EMPTY, "purple", "purple", GB.EMPTY, GB.EMPTY, "orange", "blue"],
                ["purple", GB.EMPTY, GB.EMPTY, "purple", "purple", "purple", GB.EMPTY, "orange", "orange", "blue"],
                ["purple", GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, "purple", "purple", "yellow", "yellow", "blue"],
                ["purple", GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, "orange", "yellow", "yellow", "blue"],
                ["purple", "purple", "purple", GB.EMPTY, GB.EMPTY, GB.EMPTY, "orange", "orange", "blue", "blue"]
            ]
        },
        "test info": {
            "placements": 19,
            "lowered y": INVIS_GRID_TOP + 1
        }
    }
]

AI_HELPERS_POSITIONS = [
    {
        "pieces": {
            "current": Piece(2),
            "next": Piece(0)
        },
        "position": {
            "x": 3,
            "y": INVIS_GRID_TOP + 17,
            "rotation": 0,
            "inputs": [Movement.DOWN, Movement.DOWN, Movement.DOWN, Movement.LEFT, Movement.RIGHT, Movement.DOWN],
            "grid": GRID_TOP + [
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, "purple", "purple", GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, "purple", GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, "orange", GB.EMPTY],
                [GB.EMPTY, "purple", GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, "yellow", "blue"],
                [GB.EMPTY, "purple", GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, "yellow", "blue"],
                ["purple", "purple", "purple", GB.EMPTY, GB.ACTIVE, GB.ACTIVE, GB.ACTIVE, GB.ACTIVE, "blue", "blue"]
            ]
        },
        "test info": {
            "hard drop": True,
            "score": (
                AiMultipliers.OPEN_HOLE*1
                + AiMultipliers.ROWS_WITH_HOLES*1
                + AiMultipliers.HEIGHT*2
                + AiMultipliers.BUMPINESS*12
                + AiMultipliers.EMPTY_PILLARS*1
            ),
            "open locations": [(2, INVIS_GRID_TOP + 16), (2, INVIS_GRID_TOP + 15), (2, INVIS_GRID_TOP + 14)],
            "closed locations": [],
        }
    },
    {
        "pieces": {
            "current": Piece(2),
            "next": Piece(4)
        },
        "position": {
            "x": 3,
            "y": INVIS_GRID_TOP + 17,
            "rotation": 0,
            "inputs": [Movement.LEFT, Movement.DOWN, Movement.ROTATION, Movement.DOWN, Movement.LEFT, Movement.DOWN],
            "grid": GRID_TOP + [
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, "orange", GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, "orange", "orange", GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, "orange", "orange", "orange", GB.EMPTY],
                [GB.EMPTY, "purple", GB.EMPTY, GB.EMPTY, GB.EMPTY, "orange", "orange", "yellow", "yellow", "blue"],
                ["purple", "purple", GB.EMPTY, GB.EMPTY, GB.EMPTY, "orange", "purple", "yellow", "yellow", "blue"],
                ["purple", "purple", "purple", GB.EMPTY, GB.ACTIVE, GB.ACTIVE, GB.ACTIVE, GB.ACTIVE, "blue", "blue"]
            ]
        },
        "test info": {
            "hard drop": False,
            "score": (
                + AiMultipliers.HEIGHT*3
                + AiMultipliers.BUMPINESS*13
            ),
            "open locations": [(5, INVIS_GRID_TOP + 16)],
            "closed locations": [],
        }
    },
    {
        "pieces": {
            "current": Piece(2),
            "next": Piece(3)
        },
        "position": {
            "x": 3,
            "y": INVIS_GRID_TOP + 17,
            "rotation": 0,
            "inputs": [Movement.DOWN, Movement.LEFT, Movement.ROTATION, Movement.DOWN, Movement.DOWN],
            "grid": GRID_TOP + [
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, "orange", GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, "orange", GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, "orange", GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, "orange", GB.EMPTY, "orange", "orange"],
                ["yellow", "yellow", GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, "orange", GB.EMPTY, GB.EMPTY, GB.EMPTY],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, "orange", GB.EMPTY, "orange", "orange"],
                [GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, GB.EMPTY, "orange", "orange", "orange", GB.EMPTY],
                ["orange", "purple", "yellow", GB.EMPTY, GB.EMPTY, "orange", "orange", "yellow", "yellow", "blue"],
                ["purple", "purple", "yellow", GB.EMPTY, GB.EMPTY, "orange", "purple", "yellow", "yellow", "blue"],
                ["purple", "purple", "purple", GB.EMPTY, GB.ACTIVE, GB.ACTIVE, GB.ACTIVE, GB.ACTIVE, "blue", "blue"]
            ]
        },
        "test info": {
            "hard drop": False,
            "score": (
                AiMultipliers.OPEN_HOLE*2
                + AiMultipliers.CLOSED_HOLE*1
                + AiMultipliers.ROWS_WITH_HOLES*2
                + AiMultipliers.HEIGHT*4
                + AiMultipliers.EMPTY_PILLARS*2
                + AiMultipliers.BUMPINESS*25
            ),
            "open locations": [
                (0, INVIS_GRID_TOP + 15),
                (1, INVIS_GRID_TOP + 15),
                (0, INVIS_GRID_TOP + 16),
                (1, INVIS_GRID_TOP + 16),
                (8, INVIS_GRID_TOP + 14),
                (9, INVIS_GRID_TOP + 14)
            ],
            "closed locations": [(9, INVIS_GRID_TOP + 16)]
        }
    }
]
