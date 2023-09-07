from .classes import Tetris, Position
from .constants import ROWS, INVIS_GRID_TOP, Movement, GridBlock as GB


def inputs_convert(rotations, x_move, y_move):
    """Converts a number of movements to a list/queue of instructions."""
    new_inputs = [Movement.ROTATION for _ in range(rotations)]

    if x_move < 0:
        new_inputs.append(Movement.LEFT)
    elif x_move > 0:
        new_inputs.append(Movement.RIGHT)

    if y_move > 0:
        new_inputs.append(Movement.DOWN)

    return new_inputs


def generate_all_moves(initial_pos, swapped=False):
    """Main file function that gets all the moves and returns them to the caller."""
    real_starting_pos = lower_piece(initial_pos)

    new_positions = find_moves(real_starting_pos, initial_pos.current)

    # convert positions from dictionary to Position objects
    final_positions = [Position(pos, initial_pos.current, initial_pos.next, has_swapped=swapped)
                       for pos in new_positions]
    return final_positions


def find_moves(starting_pos, current_piece):
    """Algorithm for generating all possible moves in any given tetris position.

    Generates them using dictionaries instead of dataclasses (or other classes)
    to store positions in order to maximize speed.
    """
    end_positions = []
    unexplored = [starting_pos]

    positions_found = {
        (starting_pos['rotation'], starting_pos['x'], starting_pos['y']): starting_pos
    }
    while len(unexplored) > 0:
        new_unexplored = []

        for current_pos in unexplored:
            # convert to tetris class so we can call move() and rotate() on it
            tetris_pos = dict_to_tetris(current_pos, current_piece)

            if not tetris_pos.move_is_legal(x=0, y=1):
                filter_end_pos(end_positions, current_pos, tetris_pos)

            # check sub-moves of each rotation
            for r in range(4):
                has_rotated = True if r == 0 else tetris_pos.rotate()
                if not has_rotated:  # can't rotate anymore
                    break
                find_sub_moves(current_pos, tetris_pos, positions_found, new_unexplored, r)

        unexplored = new_unexplored
    return end_positions


def find_sub_moves(current_pos, tetris_pos, positions_found, new_unexplored, r):
    """Finds all sub-moves (left, right and down) from a specific position's rotation."""
    MOVEMENTS = ((0, 0), (-1, 0), (1, 0), (0, 1))
    for x, y in MOVEMENTS:
        already_found_pos = positions_found.get(
            (tetris_pos.rotation, tetris_pos.piece_x+x, tetris_pos.piece_y+y)
        )
        # deals with already found positions
        if already_found_pos:
            if len(current_pos["inputs"]) + abs(x) + abs(y) + r < len(already_found_pos["inputs"]):
                new_inputs = inputs_convert(r, x, y)
                full_inputs = current_pos["inputs"] + new_inputs

                already_found_pos["inputs"] = full_inputs
            continue

        new_inputs = inputs_convert(r, x, y)
        full_inputs = current_pos["inputs"] + new_inputs
        
        # x=0 and y=0 would mean we don't need to simulate move
        if x != 0 or y != 0:
            if not tetris_pos.move(x, y):
                continue
                               
        new_position = {
            "x": tetris_pos.piece_x,
            "y": tetris_pos.piece_y,
            "rotation": tetris_pos.rotation,
            "grid": list(grid_copy(tetris_pos.grid)),
            "inputs": full_inputs
        }
        # undo if we moved
        if x != 0 or y != 0:
            tetris_pos.move(-x, -y)
            
        new_unexplored.append(new_position)
        positions_found[(new_position['rotation'],
                         new_position['x'],
                         new_position['y'])] = new_position


def filter_end_pos(end_positions, current_pos, tetris_pos):
    """Filter a new position depending on whether it's been reached or it provides a shorter path.
    
    Ignores given position it if it's been found 
    and it takes more inputs than original way of reaching it.
    Otherwise replaces inputs with the shorter inputs if it has been found, 
    but new solution reaches ending faster.
    """
    for pos in end_positions:
        if current_pos["grid"] == pos["grid"]:
            pos["inputs"] = (pos["inputs"] if len(pos["inputs"]) <= len(current_pos["inputs"])
                             else current_pos["inputs"])
            return
    
    end_positions.append({
        "x": current_pos["x"],
        "y": current_pos["y"],
        "rotation": current_pos["rotation"],
        "grid": list(grid_copy(tetris_pos.grid)),
        "inputs": current_pos["inputs"]
    })


def grid_copy(grid):
    """Generator which yields a copy of a grid's rows one by one.
    
    An optimization for creating copies faster than copy.deepcopy() and comprehension.
    """
    for row in grid:
        yield list(row)


def dict_to_tetris(position, current_piece):
    """Convert a position from a dict to a Tetris object, so we can use move() and rotate()."""
    converted_grid = Tetris(
        position["grid"], position["rotation"], position["x"], position["y"]
    )
    converted_grid.current = current_piece

    return converted_grid


def lower_piece(converted_grid):
    """Ai piece goes down while the place is generally empty to save computation time.
    
    Goes down while we're 4 squares above structure height (defined by first dead block).
    This is because the tallest piece -the line- is 4 squares tall,
    so computing anything above that instead of going down is a waste of time.
    """
    structure_height = get_structure_height(converted_grid)

    inputs = []
    while converted_grid.piece_y < structure_height-5:
        converted_grid.move(0, 1)
        inputs.append(Movement.DOWN)

    algo_start_position = {
            "x": converted_grid.piece_x,
            "y": converted_grid.piece_y,
            "rotation": converted_grid.rotation,
            "grid": list(grid_copy(converted_grid.grid)),
            "inputs": inputs
    }
    return algo_start_position


def get_structure_height(converted_grid):
    """Find structure height which is how high the highest dead-block is."""
    for row_idx, row in enumerate(converted_grid.grid):
        for col in row:
            if col not in [GB.ACTIVE, GB.EMPTY]:
                return row_idx
    return ROWS+INVIS_GRID_TOP # no dead blocks in the grid
