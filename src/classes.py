import random

from .constants import COLS, ROWS, IS_MAIN_PROCESS, INVIS_GRID_TOP, Movement, Pieces, GridBlock as GB


class Sfx:
    """Loads sound effects, and only if we're doing so with the main process and not a child one.
    
    This is because a child process imports all modules when started,
    and importing pygame (which we need to use pygame sounds)
    would trigger the pygame welcome message and import the whole library (which slows us).
    """
    if IS_MAIN_PROCESS:
    
        import pygame
        
        pygame.mixer.init()
        DEATH = pygame.mixer.Sound("assets\\audio\\Death.wav")

        LINE_CLEAR = pygame.mixer.Sound("assets\\audio\\LineClear.wav")
        LINE_CLEAR.set_volume(0.2)

        PLACE = pygame.mixer.Sound("assets\\audio\\Place.wav")
        PLACE.set_volume(2)


class Piece:
    """Holds a full piece's information which includes: shape, color and ghost color."""
    __slots__ = ("piece_num", "shape", "color", "ghost_color")

    def __init__(self, piece_num):
        self.piece_num = piece_num
        self.shape = Pieces.SHAPES[piece_num]
        self.color =  Pieces.COLORS[piece_num]
        self.ghost_color = Pieces.GHOST_COLORS[piece_num]
        
    def change_piece(self, new_piece_num):
        """Takes a number to swap all attributes to that index in the original lists."""
        self.piece_num = new_piece_num
        self.shape = Pieces.SHAPES[new_piece_num]
        self.color = Pieces.COLORS[new_piece_num]
        self.ghost_color = Pieces.GHOST_COLORS[new_piece_num]
    
    @classmethod
    def get_random(cls):
        """Returns a completely random piece of any shape."""
        return cls(random.randint(0, len(Pieces.SHAPES)-1))
    
    def __repr__(self):
        return f"{__class__.__name__}({self.piece_num})"

    def __str__(self):
        return f"{self.color} piece"


class Tetris:
    """Holds a tetris position which can do tetris things like creating pieces, moving and rotating."""
    __slots__ = ("grid", "pieces_bag", "current", "next", 
                 "piece_alive", "piece_x", "piece_y", "rotation")

    def __init__(
            self, grid, rotation=0, piece_x=None, piece_y=None,
            current=Piece.get_random(), next_=Piece.get_random()
    ):
        self.grid = grid
        self.pieces_bag = list(range(len(Pieces.SHAPES)))

        self.current = current
        self.next = next_
        self.piece_alive = False

        # The x and y begin on the top left of the piece relative to a 5x5 grid the piece's on
        self.piece_x, self.piece_y = piece_x, piece_y
        self.rotation = rotation
    
    def make_piece(self, swapping=False):
        """Places a new piece at the top of the grid. Doesn't get new piece if we're swapping"""
        if not swapping:
            self.generate_next()
        
        x_offset = COLS//2 - 2
        for i in range(4):
            self.grid[self.current.shape[0][i][1]][self.current.shape[0][i][0] + x_offset] = GB.ACTIVE

        self.piece_alive = True
        self.piece_x = x_offset
        self.piece_y = 0
        self.rotation = 0
    
    def generate_next(self):
        """Choose a random next piece while following tetris guidelines on random piece generation.

        The way it works is by choosing one of the pieces
        then removing it off the list like if it was in a bag.
        This makes the next time a piece is chosen have 1 less option until there's no pieces left,
        which after the "bag" is then reset.
        """
        new_piece_num = random.choice(self.pieces_bag)

        self.current.change_piece(self.next.piece_num)
        self.next.change_piece(new_piece_num)

        self.pieces_bag.remove(new_piece_num)
        if len(self.pieces_bag) == 0:
            self.pieces_bag = list(range(len(Pieces.SHAPES)))
    
    def kill_piece(self):
        """Swaps ACTIVE for its color on grid, indicating it's dead."""
        for col, row in self.current.shape[self.rotation]:
            self.grid[row+self.piece_y][col+self.piece_x] = self.current.color

        self.piece_alive = False
    
    def line_clears(self):
        """Checks if any row has only dead blocks (cleared).
        
        Clears the rows by completely removing the cleared row,
        then putting a new, empty row at the very top (before a new piece spawns)
        which gives the illusion that all the pieces dropped from gravity.
        """
        clears = 0
        for idx, row in enumerate(self.grid):
            if GB.EMPTY not in row and GB.ACTIVE not in row:
                clears += 1
                self.grid.pop(idx)
                self.grid.insert(0, [GB.EMPTY]*COLS)
        return clears
    
    def move(self, x, y):
        """Move piece on a given grid."""
        if not self.move_is_legal(x=x, y=y):
            if y:
                self.kill_piece()  # kill if illegal move was down
            return False

        for col, row in self.current.shape[self.rotation]:
            self.grid[row+self.piece_y][col+self.piece_x] = GB.EMPTY

        for col, row in self.current.shape[self.rotation]:
            self.grid[row+y+self.piece_y][col+self.piece_x+x] = GB.ACTIVE

        self.piece_x += x
        self.piece_y += y
        return True

    def rotate(self):
        """Rotates piece. Returns a bool to tell us if rotation was successful or not."""
        if not self.move_is_legal(rotate=True):
            return False
        
        for x, y in self.current.shape[self.rotation]:
            self.grid[y+self.piece_y][x+self.piece_x] = GB.EMPTY

        for x, y in self.current.shape[self.next_rotation]:
            self.grid[y+self.piece_y][x+self.piece_x] = GB.ACTIVE

        self.rotation = self.next_rotation
        return True

    def move_is_legal(self, x=0, y=0, rotate=False):
        """Checks legality of a move without implementing it."""
        rotation = self.next_rotation if rotate else self.rotation

        for col, row in self.current.shape[rotation]:
            new_x, new_y = col+self.piece_x+x, row+self.piece_y+y
            
            if (new_x < 0 or new_x > COLS-1 or new_y > ROWS+INVIS_GRID_TOP-1
                    or self.grid[new_y][new_x] not in [GB.ACTIVE, GB.EMPTY]):
                return False
        return True

    def hard_drop(self):
        while self.move(0, 1):
            pass

    @property
    def next_rotation(self):
        """Returns what would be the next rotation index for the piece."""
        return (self.rotation+1) % 4
    
    def __repr__(self):
        return (f"{__class__.__name__}({self.grid}, {self.rotation}, "
                f"{self.piece_x}, {self.piece_y}, Piece({self.current.piece_num}), Piece({self.next.piece_num}))")
    
    def __str__(self):
        output = ""
        for row in self.grid:
            for col in row:
                if col == GB.ACTIVE:
                    output += "A"
                elif col == GB.EMPTY:
                    output += "."
                else:
                    output += "O"
            output += "\n"
        return output
        # return "".join(["".join(ch[0] for ch in row) + "\n" for row in self.grid])


class Game(Tetris):
    """Tetris but with extra stuff specifically for the game itself."""
    __slots__ = ("grid", "score", "held", "swapped", "running")
    sfx = Sfx()

    def __init__(self):
        self.grid = [[GB.EMPTY for x in range(COLS)] for y in range(ROWS+INVIS_GRID_TOP)]
        super().__init__(self.grid)

        self.score = 0
        self.held = None
        self.swapped = False
        self.running = False

    def hold_piece(self):
        """Holds piece. If there is a held piece then grab current and make next piece current."""
        if self.swapped:
            return  # ensures you don't spam swap
        
        # clear active piece
        self.grid = [[col if col != GB.ACTIVE else GB.EMPTY for col in row] for row in self.grid]
        self.swapped = True
        self.rotation = 0

        if self.held is None:
            self.held = Piece(self.current.piece_num)
            self.make_piece()
        else:
            self.swap_pieces(self.current, self.held)
            self.make_piece(True)

    def reset(self):
        """Restarts everything on screen."""
        self.grid = [[GB.EMPTY for col in row] for row in self.grid]
        
        self.running = False
        self.rotation = 0
        self.score = 0
        self.piece_x, self.piece_y = 0, 0

        self.current = Piece.get_random()
        self.next = Piece.get_random()
        self.held = None
    
    def line_clears(self):
        """Calls parent's line_clear and uses number of clears to get score"""
        clears = super().line_clears()
        score_convert = {"0": 0, "1": 40, "2": 100, "3": 300, "4": 1200}
        self.score += score_convert[str(clears)]

        if clears:
            self.sfx.LINE_CLEAR.play()

    def kill_piece(self):
        """Calls parent's kill_piece then checks for game over since this is game class"""
        super().kill_piece()
        self.check_game_over()
        self.swapped = False
        if self.running:
            self.sfx.PLACE.play()
    
    def check_game_over(self):
        """Checks if game ended by seeing if any dead-block has reached above the visible grid."""
        for row_idx, row in enumerate(self.grid):
            for col in row:
                if row_idx >= INVIS_GRID_TOP:
                    return
                if col in [GB.ACTIVE, GB.EMPTY]:
                    continue
                self.reset()
                self.sfx.DEATH.play()

    @staticmethod
    def swap_pieces(piece1, piece2):
        """Swaps two piece's attributes."""
        original_1_num = piece1.piece_num
        piece1.change_piece(piece2.piece_num)
        piece2.change_piece(original_1_num)


class Position(Tetris):
    """Represents a position produced by AI."""
    __slots__ = ("inputs", "current", "next", "using_held", "score")

    def __init__(self, position, current, next_, has_swapped=False):
        super().__init__(
            position["grid"], position["rotation"], position["x"], position["y"],
            current=Piece(current.piece_num), next_=Piece(next_.piece_num)
        )
        self.inputs = position["inputs"]

        self.using_held = has_swapped
        self.score = 0

    def convert_to_hard_drop(self):
        """Converts inputs to hard-drop.
        
        This was made for extra speed whenever AI's not doing any fancy spins,
        which is done by removing all downs, inserting rotations at the start
        and appending lefts and rights normally.
        """
        new_inputs = []
        for pos_input in self.inputs:
            if pos_input == Movement.DOWN:
                continue
            elif pos_input == Movement.ROTATION:
                new_inputs.insert(0, Movement.ROTATION)
            else:
                new_inputs.append(pos_input)
        self.inputs = new_inputs
    
    def __repr__(self):
        position = {
            "x": self.piece_x,
            "y": self.piece_y,
            "rotation": self.rotation,
            "grid": self.grid,
            "inputs": self.inputs
        }
        return (f"{__class__.__name__}({position}, {self.current.__repr__()}, "
                f"{self.next.__repr__()}, {self.using_held})")
    