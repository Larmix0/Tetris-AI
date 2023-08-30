import unittest
from copy import deepcopy
import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "true"  # hide pygame welcome message

from tests.positions import tetris_to_dict, PLACED_POSITIONS, UNPLACED_POSITIONS
from src.classes import Tetris
from src.constants import Movement
from src.generate_moves import (
    inputs_convert,
    find_moves,
    find_sub_moves,
    filter_end_pos,
    dict_to_tetris,
    lower_piece,
    get_structure_height,
    grid_copy
)


class TestGenerateMoves(unittest.TestCase):
    """Class that tests functions which achieve direct progress in generating moves.
    
    more importantly, it includes functions that need the same setUp method.
    test_lower_piece counts since it needs the same setUp
    and it's also a method that affects generated positions directly.
    """
    def setUp(self):
        """initializer for positions that'll be needed for the tests.
        
        initializes self.position after every test,
        which stores the positions in a tuple of general information of a position
        and a directly usable object.
        """
        self.positions = []
        for pos_info in UNPLACED_POSITIONS:
            position = pos_info["position"]
            tetris = Tetris(
                deepcopy(position["grid"]),
                current=deepcopy(pos_info["pieces"]["current"]),
                next_=deepcopy(pos_info["pieces"]["current"])
            )
            tetris.make_piece()
            self.positions.append((pos_info, tetris))

    def test_lower_piece(self):
        """Tests lower_piece by comparing its return value with a hard-coded answer."""
        for pos_info, test_pos in self.positions:
            lowered_pos = lower_piece(test_pos)
            self.assertEqual(lowered_pos["y"], pos_info["test info"]["lowered y"])
        
    def test_find_sub_moves(self):
        """tests find_sub_moves by expecting certain modifications to a list from the function.
        
        Makes a couple of moves so we're closer to edges,
        then expects the function to modify a list by adding 4 positions:
        The position itself, position + 1 left, position + 1 right and position + 1 down.
        """
        MOVEMENTS = ((0, 0), (-1, 0), (1, 0), (0, 1))
        ACTIONS = ([], [Movement.LEFT], [Movement.RIGHT], [Movement.DOWN])

        for _, test_pos in self.positions:
            for _ in range(5):
                test_pos.move(0, 1)
            test_pos.move(1, 0)
            
            dict_pos = tetris_to_dict(test_pos)
            returned_positions = []
            find_sub_moves(dict_pos, test_pos, {}, returned_positions, r=0)

            for move, action in zip(MOVEMENTS, ACTIONS):
                test_pos_copy = deepcopy(test_pos)
                test_pos_copy.move(*move)

                dict_pos = tetris_to_dict(test_pos_copy, inputs=action)
                self.assertIn(dict_pos, returned_positions)
    
    def test_filter_end_pos(self):
        """Tests filter_end_pos which ensures we don't append the same positions already found.
        
        Soft drops the piece then sees if end_positions gets appended the right dictionary.
        It also ensures the function doesn't add the same positions again
        by repeating the same test twice without changing anything.
        """
        for _, test_pos in self.positions:
            test_pos.rotate()
            test_pos.move(1, 0)
            while test_pos.move_is_legal(0, 1):
                test_pos.move(0, 1)

            end_positions = []
            dict_pos = tetris_to_dict(test_pos)

            # first time it gets appended, second time it's filtered out so list doesn't change
            filter_end_pos(end_positions, dict_pos, test_pos)
            self.assertEqual(end_positions, [dict_pos])
            filter_end_pos(end_positions, dict_pos, test_pos)
            self.assertEqual(end_positions, [dict_pos])

    def test_find_moves(self):
        """Tests the general find_moves function which should return a dictionary of all moves.
        
        Here we compare the returned list's length to a hard-coded value.
        The reason we compare length and not actually returned positions is because
        it'd be too much to store the dozens of positions returned in positions.py.
        """
        for pos_info, test_pos in self.positions:
            lowered_pos = lower_piece(test_pos)

            returned_moves = find_moves(lowered_pos, deepcopy(pos_info["pieces"]["current"]))
            self.assertEqual(len(returned_moves), pos_info["test info"]["placements"])


class TestGenerateMovesHelpers(unittest.TestCase):
    """Tests all other functions of generate_moves.py.
    
    Tests ones that simply don't require the same setUp method in TestGenerateMoves,
    or ones that don't make direct impact on the position like input_convert.
    """
    def test_input_convert(self):
        """Converts a number of rotations + optional x and y moves to a list of instructions.
        
        We have an actions list of certain inputs to test on input_convert,
        then we pop each rotation or an x/y move one by one and ensure the returned list
        doesn't have them any longer.
        """
        ACTIONS = [
            {"rotations": 3, "x": 1, "y": 1},
            {"rotations": 7, "x": -1, "y": 0},
            {"rotations": 0, "x": 0, "y": 1},
            {"rotations": 1, "x": 0, "y": 0},
            {"rotations": 15, "x": -1, "y": 1}
        ]
        for action in ACTIONS:
            movements = inputs_convert(
                rotations=action["rotations"], x_move=action["x"], y_move=action["y"]
            )

            for _ in range(action["rotations"]):
                movements.remove(Movement.ROTATION)
            self.assertNotIn(Movement.ROTATION, movements)
            
            if action["x"] < 0:
                movements.remove(Movement.LEFT)
            elif action["x"] > 0:
                movements.remove(Movement.RIGHT)
            self.assertNotIn(Movement.LEFT, movements)
            self.assertNotIn(Movement.RIGHT, movements)

            if action["y"]:
                movements.remove(Movement.DOWN)
            self.assertNotIn(Movement.DOWN, movements)

    def test_dict_to_tetris(self):
        """Tests if dict_to_tetris properly converts a Tetris object to a dictionary."""
        for pos_info in PLACED_POSITIONS:
            position = pos_info["position"]
            pos_dict = {
                "grid": position["grid"],
                "rotation": position["rotation"],
                "x": position["x"],
                "y": position["y"],
            }
            tetris = dict_to_tetris(pos_dict, deepcopy(pos_info["pieces"]["current"]))
            
            self.assertEqual(tetris.grid, deepcopy(position["grid"]))
            self.assertEqual(tetris.piece_x, position["x"])
            self.assertEqual(tetris.piece_y, position["y"])
            self.assertEqual(tetris.rotation, position["rotation"])

    def test_get_structure_height(self):
        """Tests get_structure_height's return value.
        
        It does so by seeing if the returned height is the same as the hard-coded answer.
        """
        for pos_info in PLACED_POSITIONS:
            position = pos_info["position"]
            tetris = Tetris(
                deepcopy(position["grid"]),
                position["rotation"],
                position["x"],
                position["y"],
                deepcopy(pos_info["pieces"]["current"]),
                deepcopy(pos_info["pieces"]["next"])
            )
            tested_height = get_structure_height(tetris)
            self.assertEqual(tested_height, pos_info["test info"]["structure height"])

    def test_grid_copy(self):
        """Tests if grid_copy (which yields a generator) can be converted to a normal list."""
        for pos_info in PLACED_POSITIONS:
            self.assertEqual(
                pos_info["position"]["grid"], list(grid_copy(pos_info["position"]["grid"]))
            )
