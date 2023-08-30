import unittest
import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "true"  # hide pygame welcome message

from src.constants import INVIS_GRID_TOP, Pieces, Movement, GridBlock as GB
from src.classes import Piece, Tetris, Game, Position


class TestPiece(unittest.TestCase):
    """Tests the Piece class to see if it's storing things properly."""

    def test_change_piece(self):
        """Tests to see if changing piece changes it to the expected number."""
        piece = Piece(3)
        self.assertEqual(piece.piece_num, 3)
        piece.change_piece(5)
        self.assertEqual(piece.piece_num, 5)


class TestTetris(unittest.TestCase):
    """Tests most relevant methods of Tetris class except make_piece and move_is_legal.
    
    This is because testing it beyond ensuring it didn't raise an error is too difficult.
    Also worth saying that make_piece is mostly reliant on generate_next
    so testing that should be enough.
    """
    def setUp(self):
        """Sets up a basic, empty position for every test to use if needed."""
        self.tetris = Tetris(
            grid=[[GB.EMPTY for x in range(10)] for y in range(20 + INVIS_GRID_TOP)],
            current=Piece(2),
            next_=Piece(1)
        )

    def test_generate_next(self):
        """Tests if generate_next generates pieces properly.
        
        This is done by ensuring that the next piece turns into the current one,
        and that the next piece is randomly popped off from the pieces_bag list.
        """
        original_next = Piece(self.tetris.next.piece_num)
        
        self.tetris.generate_next()
        self.assertEqual(self.tetris.current.piece_num, original_next.piece_num)
        self.assertNotIn(self.tetris.next.piece_num, self.tetris.pieces_bag)

    def test_kill_piece(self):
        """Tests if kill_piece kills the active piece properly.
        
        Makes a piece then kills it instantly. Ensures it was killed correctly by seeing
        that there aren't any active piece's blocks on the grid.
        """
        self.tetris.make_piece()
        self.tetris.kill_piece()
        self.assertFalse(self.tetris.piece_alive)

        for row in self.tetris.grid:
            self.assertNotIn(GB.ACTIVE, row)
    
    def test_line_clears(self):
        """tests that line_clears clears the grid's lines properly.
        
        First ensure that it doesn't default to simply clearing any non-filled position,
        then creates 2 filled lines at the bottom of the grid
        and sees if the return value of the function
        is correct and that the last 2 lines are cleared correctly.
        """
        self.assertEqual(self.tetris.line_clears(), 0)
        self.tetris.grid[-2] = [Pieces.COLORS[0]]*10
        self.tetris.grid[-1] = [Pieces.COLORS[0]]*10

        self.assertEqual(self.tetris.line_clears(), 2)
        self.assertTrue(self.tetris.grid[-1] == self.tetris.grid[-2] == [GB.EMPTY]*10)

    def test_move(self):
        """Tests that the move method works properly.
        
        This is done by inserting a hand-made flat line piece next to a right corner,
        then does some moves that are possible and some that hit the wall and checks
        if the possible moves work and if the impossible ones don't.
        """
        block_positions = [(i, INVIS_GRID_TOP+18) for i in range(5, 9)]
        for x, y in block_positions:
            self.tetris.grid[y][x] = GB.ACTIVE

        self.tetris.piece_x = 4
        self.tetris.piece_y = INVIS_GRID_TOP+16

        self.assertTrue(self.tetris.move(1, 0))
        self.assertFalse(self.tetris.move(1, 0))
        self.assertTrue(self.tetris.move(0, 1))
        self.assertFalse(self.tetris.move(0, 1))
    
    def test_rotation(self):
        """Tests that the rotate method works properly.
        
        This is done by inserting a flat line piece next to the right wall,
        then making a series of movements and rotations where some are asserted as possible,
        and some are asserted as not.
        """
        BLOCK_POSITIONS = [(i, INVIS_GRID_TOP+15) for i in range(5, 9)]
        for x, y in BLOCK_POSITIONS:
            self.tetris.grid[y][x] = GB.ACTIVE

        self.tetris.piece_x = 4
        self.tetris.piece_y = INVIS_GRID_TOP+13

        self.assertTrue(self.tetris.rotate())
        self.tetris.move(2, 0)
        self.assertFalse(self.tetris.rotate())
        self.tetris.move(-1, 0)
        for _ in range(4):
            self.assertTrue(self.tetris.rotate())
        

class TestGame(unittest.TestCase):
    """Tests the Game class, which is a subclass of Tetris."""
    def setUp(self):
        """Creates a very basic Game object with a green current piece for testing functions."""
        self.game = Game()
        self.game.current = Piece(0)
        self.game.next = Piece(3)

    def test_empty_hold(self):
        """Tests hold_piece when the held slot has nothing on it.
        
        Ensures that the current piece goes to held, and next piece goes to current.
        """
        original_current = Piece(self.game.current.piece_num)
        original_next = Piece(self.game.next.piece_num)

        self.game.hold_piece()
        self.assertEqual(self.game.held.piece_num, original_current.piece_num)
        self.assertEqual(self.game.current.piece_num, original_next.piece_num)

    def test_filled_hold(self):
        """Tests hold_piece when the held slot has a piece on it.
        
        Ensures that the current piece swaps with held, and next piece doesn't change.
        """
        self.game.held = Piece(2)
        
        original_current = Piece(self.game.current.piece_num)
        original_next = Piece(self.game.next.piece_num)
        original_held = Piece(self.game.held.piece_num)

        self.game.hold_piece()
        self.assertEqual(self.game.held.piece_num, original_current.piece_num)
        self.assertEqual(self.game.current.piece_num, original_held.piece_num)
        self.assertEqual(self.game.next.piece_num, original_next.piece_num)

    def test_reset(self):
        """Tests that the reset method makes every value go back to nothing."""
        self.game.hold_piece()
        self.game.move(0, 5)
        self.game.rotate()

        self.game.reset()
        self.assertEqual([self.game.piece_x, self.game.piece_y, self.game.rotation], [0, 0, 0])
        self.assertIsNone(self.game.held)

    def test_swap_pieces(self):
        """Tests that swap_pieces swaps the pieces passed on it properly."""
        piece1 = Piece(1)
        piece2 = Piece(4)

        self.game.swap_pieces(piece1, piece2)
        self.assertEqual(piece1.piece_num, 4)
        self.assertEqual(piece2.piece_num, 1)


class TestPosition(unittest.TestCase):
    """Tests the Position class which is a subclass of Tetris."""

    def setUp(self):
        """Initialized a very generic Position object for other testing functions to use."""
        fake_pos = {"grid": None, "x": None, "y": None, "rotation": None, "inputs": []}
        self.position = Position(fake_pos, Piece.get_random(), Piece.get_random())

    def test_convert_to_hard_drop(self):
        """tests the convert_to_hard_drop method (which converts position's inputs to a hard-drop).
        
        Tests it by inserting a list of unconverted inputs, then expecting inputs of self.position
        to change such that: there aren't any downs and that all rotations are at the beginning.
        """
        original_inputs = [
            Movement.DOWN, Movement.RIGHT, Movement.DOWN,
            Movement.DOWN, Movement.DOWN, Movement.ROTATION,
            Movement.DOWN, Movement.RIGHT, Movement.DOWN,
            Movement.ROTATION, Movement.DOWN, Movement.RIGHT,
            Movement.DOWN, Movement.DOWN, Movement.DOWN,
            Movement.DOWN, Movement.DOWN, Movement.RIGHT,
            Movement.DOWN, Movement.ROTATION, Movement.DOWN,
            Movement.DOWN, Movement.DOWN, Movement.DOWN
        ]
        self.position.inputs = original_inputs

        self.position.convert_to_hard_drop()
        self.assertNotIn(Movement.DOWN, self.position.inputs)
        
        for move in self.position.inputs:
            self.position.inputs.pop(0)
            if move != Movement.ROTATION:
                self.assertNotIn(Movement.ROTATION, self.position.inputs)
                break
