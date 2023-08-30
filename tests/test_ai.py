import unittest
from copy import deepcopy
import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "true"  # hide pygame welcome message

from tests.positions import AI_HELPERS_POSITIONS, PLACED_POSITIONS
from src.constants import AiMultipliers, Movement
from src.classes import Position, Piece
from src.ai import (
    eval_holes,
    eval_height,
    find_bumps,
    eval_bumpiness,
    eval_empty_pillars,
    find_best_sub_position,
    get_best_position,
    correct_inputs,
    add_hole
)


class TestEvaluations(unittest.TestCase):
    """Class that specifically tests evaluation functions from ai.py."""

    def setUp(self):
        """Sets up a list of Position objects to be used for each evaluation test."""
        self.positions = [
            Position(
                deepcopy(pos_info["position"]),
                pos_info["pieces"]["current"],
                pos_info["pieces"]["next"]
            )
            for pos_info in PLACED_POSITIONS
        ]

    def test_holes(self):
        """Tests the eval_holes function.
        
        it does so by comparing the function's
        modification on test_pos.score vs the hard-coded, correct numbers.
        """
        for pos_info, test_pos in zip(PLACED_POSITIONS, self.positions):
            test_info = pos_info["test info"]
            eval_holes(test_pos)
            expected_eval = (
                AiMultipliers.OPEN_HOLE*test_info["open holes"]
                + AiMultipliers.CLOSED_HOLE*test_info["closed holes"]
                + AiMultipliers.ROWS_WITH_HOLES*test_info["rows with holes"]
            )
            self.assertAlmostEqual(test_pos.score, expected_eval, places=5)

    def test_height(self):
        """Tests evaluating the height of the piece by comparing to the hard-coded answer."""
        for pos_info, test_pos in zip(PLACED_POSITIONS, self.positions):
            eval_height(test_pos)
            expected_eval = AiMultipliers.HEIGHT*pos_info["test info"]["height"]
            self.assertAlmostEqual(test_pos.score, expected_eval, places=5)
    
    def test_bumpiness(self):
        """Tests eval_bumpiness by comparing its effect on score vs the hard-coded answer."""
        for pos_info, test_pos in zip(PLACED_POSITIONS, self.positions):
            eval_bumpiness(test_pos, pos_info["test info"]["bumpiness"])

            expected_eval = pos_info["test info"]["bumps"]*AiMultipliers.BUMPINESS
            self.assertAlmostEqual(test_pos.score, expected_eval, places=5)
    
    def test_empty_pillars(self):
        """Tests eval_empty_pillars by comparing its effect on score vs the hard-coded answer."""
        for pos_info, test_pos in zip(PLACED_POSITIONS, self.positions):
            eval_empty_pillars(test_pos, pos_info["test info"]["bumpiness"])
            expected_eval = pos_info["test info"]["empty pillars"]*AiMultipliers.EMPTY_PILLARS
            self.assertAlmostEqual(test_pos.score, expected_eval, places=5)


class TestAiEvaluationsHelpers(unittest.TestCase):
    """Class that tests helper evaluation functions (ones that don't impact position's score)."""

    def setUp(self):
        """Initializer for positions."""
        self.positions = []
        for pos_info in AI_HELPERS_POSITIONS:
            self.positions.append((pos_info, Position(
                deepcopy(pos_info["position"]),
                deepcopy(pos_info["pieces"]["current"]),
                deepcopy(pos_info["pieces"]["next"])
            )))

    def test_find_bumps(self):
        """Tests find_bumps by comparing the returned value to a hard-coded one."""
        for pos_info in PLACED_POSITIONS:
            test_pos = Position(
                deepcopy(pos_info["position"]),
                pos_info["pieces"]["current"],
                pos_info["pieces"]["next"]
            )
            bumpiness = find_bumps(test_pos)
            self.assertEqual(bumpiness, pos_info["test info"]["bumpiness"])

    def test_get_best_position(self):
        """Tests get_best_position with dummy Positions.
         
        It does so by creating Positions with pre-made scores and ensuring it always returns max.
        """
        fake_pos = {"grid": None, "x": None, "y": None, "rotation": None, "inputs": []}
        scores = [
            [-2, -1, -6, -4, -10],
            [-2, -5.4, -1.3, -9.4, -0.2],
            [-3.1, -2.8, -8.4, -4.5, -35.2]
        ]
        for score_list in scores:
            positions = []

            for score in score_list:
                test_pos = Position(fake_pos, Piece(0), Piece(0), None)
                test_pos.score = score
                positions.append(test_pos)
            self.assertEqual(get_best_position(positions).score, max(score_list))
    
    def test_find_best_sub_position(self):
        """Test find_best_sub_position by comparing score with a hard-coded one."""
        for pos_info, test_pos in self.positions:
            returned_pos = find_best_sub_position(test_pos)
            self.assertAlmostEqual(returned_pos.score, pos_info["test info"]["score"], places=5)

    def test_add_hole(self):
        """Tests add_hole by making sure it separates hard-coded open/closed holes correctly."""
        for pos_info, test_pos in self.positions:
            open_holes, closed_holes = [], []
            test_info = pos_info["test info"]

            for x, y in test_info["closed locations"]:
                add_hole(test_pos.grid, open_holes, closed_holes, x, y)
            for x, y in test_info["open locations"]:
                add_hole(test_pos.grid, open_holes, closed_holes, x, y)

            self.assertEqual(open_holes, test_info["open locations"])
            self.assertEqual(closed_holes, test_info["closed locations"])
    
    def test_correct_inputs(self):
        """Tests correct_inputs vs some pre-made positions.
        
        It does so by ensuring it makes the right decision
        by seeing if it removes all the downs 
        (indicating that it converted to hard-drop) or not. 
        """
        for pos_info, test_pos in self.positions:
            correct_inputs(test_pos)
            if pos_info["test info"]["hard drop"]:
                self.assertNotIn(Movement.DOWN, test_pos.inputs)
            else:
                self.assertIn(Movement.DOWN, test_pos.inputs)
