from multiprocessing import Pool

from .generate_moves import generate_all_moves
from .constants import COLS, ROWS, INVIS_GRID_TOP, Movement, AiMultipliers, GridBlock as GB


def ai_move(game_copy):
    """Main function of this file.
     
    1. Gets generated positions for current piece and held piece.
    2. Generates their sub-positions (positions of next piece).
    3. Evaluates those positions to set them as the real score of the parent-position.
    4. Returns the best one.
    """
    # get positions of current and held piece
    end_positions = generate_all_moves(game_copy, swapped=False)
    game_copy.hold_piece()
    end_positions += generate_all_moves(game_copy, swapped=True)

    # get true scores of position after generating their sub-positions to set the scores
    with Pool(processes=5) as pool:
        sub_positions = pool.map(find_best_sub_position, end_positions, chunksize=4)
        for pos, sub_position in zip(end_positions, sub_positions):
            pos.score = sub_position.score

    best_position = get_best_position(end_positions)
    correct_inputs(best_position)
    best_position.inputs.append(Movement.DROP) # always add the hard-drop so the piece is killed
    return best_position


def find_best_sub_position(position) -> int:
    """evaluates the passed position's sub-positions to predict the future score of it."""
    # keep track of the piece we just placed
    for x, y in position.current.shape[position.rotation]:
        position.grid[y+position.piece_y][x+position.piece_x] = GB.PREVIOUS

    # prepare for next move
    position.line_clears()
    position.make_piece()

    sub_positions = generate_all_moves(position)
    for pos in sub_positions:
        eval_holes(pos)
        eval_height(pos)
        
        bumpiness = find_bumps(pos)
        eval_empty_pillars(pos, bumpiness)
        eval_bumpiness(pos, bumpiness)

    return get_best_position(sub_positions)


def get_best_position(positions):
    """Find the best score from a list of positions."""
    best_position = positions[0]  # default

    for position in positions:
        if position.score > best_position.score:
            best_position = position
    return best_position


def correct_inputs(position) -> None:
    """Either keeps the inputs of the position or converts it to one we can hard-drop.
    
    By default we have our inputs done one by one from generate_moves.py, but most of the time
    we can actually hard-drop to reach a position instead of going down one by one.
    So we check by seeing if an active block's under a dead one,
    because it means the position can't be reached via a hard-drop.
    """
    hard_drop = True
    for x in range(COLS):
        dead_block_found = False
        for y in range(ROWS+INVIS_GRID_TOP):

            if position.grid[y][x] not in [GB.ACTIVE, GB.EMPTY]:
                dead_block_found = True

            elif position.grid[y][x] == GB.ACTIVE and dead_block_found:
                hard_drop = False
    if hard_drop:
        position.convert_to_hard_drop()


def eval_holes(position) -> None:
    """Finds all holes and categorizes them.

    A hole is an empty block which has a piece's block above it.
    Here we use a method to subtract holes since they're kinda special
    and require the class internally checking stuff to determine if they're closed or open.
    """
    open_holes, closed_holes = [], []
    rows_with_holes = set()

    for x in range(COLS):
        piece_detected = False

        for y in range(ROWS+INVIS_GRID_TOP):
            if position.grid[y][x] != GB.EMPTY:
                piece_detected = True

            if position.grid[y][x] == GB.EMPTY and piece_detected:
                add_hole(position.grid, open_holes, closed_holes, x, y)
                rows_with_holes.add(y)

    for _ in open_holes:
        position.score += AiMultipliers.OPEN_HOLE
    for _ in closed_holes:
        position.score += AiMultipliers.CLOSED_HOLE
    for _ in rows_with_holes:
        position.score += AiMultipliers.ROWS_WITH_HOLES


def add_hole(grid, open_holes, closed_holes, x, y) -> None:
    """Determines if a found hole is closed or open.
    
    A closed hole is a hole which is closed by another block or the wall
    on both sides, which makes it impossible to fill using fancy spins.
    """
    right_closed = grid[y][x+1] != GB.EMPTY if x != COLS-1 else True
    left_closed = grid[y][x-1] != GB.EMPTY if x != 0 else True

    # edge case where we have wall to our left or right
    if (right_closed and x == 0) or (left_closed and x == COLS-1):
        closed_holes.append((x, y))

    elif right_closed and left_closed:
        closed_holes.append((x, y))
        
    # if all failed, then the hole is open.
    else:
        open_holes.append((x, y))


def eval_height(position):
    """Check how high the piece is (lower is better)."""
    real_height = 0
    for row_idx, row in enumerate(reversed(position.grid)):
        if GB.ACTIVE in row or GB.PREVIOUS in row:
            real_height = row_idx
            
    position.score += real_height * AiMultipliers.HEIGHT


def find_bumps(position) -> list[int]:
    """Finds grid bumpiness by seeing how low is the lowest non-empty block on each column."""
    bumpiness = []
    for x in range(COLS):
        bump_found = False
        
        for y in range(ROWS+INVIS_GRID_TOP):
            if position.grid[y][x] == GB.EMPTY:
                continue
            bumpiness.append(y)
            bump_found = True
            break
        # if no pieces are in a column, then grid height is the bumpiness
        if not bump_found:
            bumpiness.append(ROWS+INVIS_GRID_TOP)
    return bumpiness


def eval_empty_pillars(position, bumpiness):
    """Finds pillars where the smallest bump to the side is 3+ in height.

    which means it can only be filled with a line piece if you don't want to create a hole.
    """
    for idx, bump in enumerate(bumpiness):
        if idx == 0:
            lowest_bump = bumpiness[1]
        elif idx == len(bumpiness)-1:
            lowest_bump = bumpiness[-2]
        else:
            lowest_bump = max(bumpiness[idx-1], bumpiness[idx+1])
            
        if bump-lowest_bump >= 3:
            position.score += AiMultipliers.EMPTY_PILLARS


def eval_bumpiness(position, bumpiness):
    """Lose score for general bumpiness of the grid."""
    previous_height = bumpiness[0]
    for bump in bumpiness:

        position.score += (abs(previous_height-bump)) * AiMultipliers.BUMPINESS
        previous_height = bump
