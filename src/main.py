import sys
import copy

from .ai import ai_move
from .classes import Game, AiExecutor
from .constants import COLS, ROWS, IS_MAIN_PROCESS, INVIS_GRID_TOP, Movement, GridBlock as GB

SPACE = 30
GRID_WIDTH = SPACE*COLS
GRID_HEIGHT = SPACE*ROWS

RIGHT_MARGIN, LEFT_MARGIN = 350, 350
BOTTOM_MARGIN, TOP_MARGIN = 100, 150

NEXT_X, NEXT_Y = 400 + (COLS*SPACE), 150
HELD_X, HELD_Y = 50, 150

if IS_MAIN_PROCESS:
    import pygame

    pygame.init()
    X_SCREEN_GRID_PAD = SPACE*10 if GRID_WIDTH < SPACE*10 else GRID_WIDTH # sets default in case too few cols
    Y_SCREEN_GRID_PAD = SPACE*20 if GRID_HEIGHT < SPACE*20 else GRID_HEIGHT # sets default in case too few rows
    DISPLAY = pygame.display.set_mode(
        (X_SCREEN_GRID_PAD+RIGHT_MARGIN+LEFT_MARGIN, Y_SCREEN_GRID_PAD+TOP_MARGIN+BOTTOM_MARGIN)
    )


def show_grid():
    """Draw a red rectangle around the grid and the gray lines which divide each block."""
    RECT_THICKNESS = 10
    red_rect = pygame.draw.rect(
        DISPLAY, "red", (LEFT_MARGIN-10, TOP_MARGIN-10, (COLS*SPACE) + 21, (ROWS*SPACE) + 21), RECT_THICKNESS
    )

    # draw gray lines that divide columns and rows
    for line in range(1, COLS):
        pygame.draw.line(
            DISPLAY, "dark gray", 
            (line*SPACE + LEFT_MARGIN, red_rect.top+RECT_THICKNESS),
            (line*SPACE + LEFT_MARGIN, red_rect.bottom-RECT_THICKNESS-1)
        )

    for line in range(1, ROWS):
        pygame.draw.line(
            DISPLAY, "dark gray", 
            (red_rect.right-RECT_THICKNESS-1, line*SPACE + TOP_MARGIN),
            (red_rect.left+RECT_THICKNESS, line*SPACE + TOP_MARGIN)
        )


def draw_pieces(game):
    """Draws every piece's squares on the grid.

    This is except the ones at the highest rows (ones that just spawned),
    because they're above the visible grid.

    It chooses color by either picking current piece's active color
    or reading the color of the dead piece on the grid,
    because pieces are killed by turning from ACTIVEs on the grid
    to a word of their color (Eg: "blue" or "red").
    """
    for row_idx, row in enumerate(game.grid):
        for col_idx, col in enumerate(row):
            color = game.current.color if col == GB.ACTIVE else col

            # square empty or piece above grid
            if col == GB.EMPTY or row_idx < INVIS_GRID_TOP:
                continue
            pygame.draw.rect(
                DISPLAY, color, 
                (col_idx*SPACE + LEFT_MARGIN,
                 (row_idx-INVIS_GRID_TOP) * SPACE + TOP_MARGIN,
                 SPACE-1,
                 SPACE-1)
            )
            pygame.draw.rect(
                DISPLAY, "black", 
                (col_idx*SPACE + LEFT_MARGIN,
                 (row_idx-INVIS_GRID_TOP) * SPACE + TOP_MARGIN,
                 SPACE+1,
                 SPACE+1),
                 3
            )


def ghost_piece(game):
    """Displays a ghost that helps player gauge where they'd go if they hard-drop."""
    downs_counter = 0
    can_move = True

    # find how low the ghost should go
    while can_move:
        can_move = game.move_is_legal(x=0, y=downs_counter+1)
        if can_move:
            downs_counter += 1

    # draw the ghost
    for row_idx, row in enumerate(game.grid):
        for col_idx, col in enumerate(row):

            if col != GB.ACTIVE or row_idx+downs_counter < INVIS_GRID_TOP:
                continue
            pygame.draw.rect(
                DISPLAY, game.current.ghost_color, 
                (col_idx*SPACE + LEFT_MARGIN+1,
                 (row_idx-INVIS_GRID_TOP+downs_counter) * SPACE + TOP_MARGIN,
                 SPACE-1,
                 SPACE-1)
            )
            pygame.draw.rect(
                DISPLAY, "black", 
                (col_idx*SPACE + LEFT_MARGIN,
                 (row_idx-INVIS_GRID_TOP+downs_counter) * SPACE + TOP_MARGIN,
                 SPACE+1,
                 SPACE+1),
                 3
            )


def piece_frame(start_x, start_y, piece):
    """Draws a square frame that's empty or has a piece in it.
    
    Frame has a gray background made on the passed start_x and start_y
    coordinates starting from top-left and a piece inside the frame shaped on a 5x5 grid.
    """
    OUTER_SIZE = 250
    INNER_SIZE = OUTER_SIZE-20
    PIECE_MARGIN = OUTER_SIZE/10
    BLOCK_SIZE = SPACE*1.33

    pygame.draw.rect(DISPLAY, "red", (start_x, start_y, OUTER_SIZE, OUTER_SIZE), 10)
    pygame.draw.rect(DISPLAY, "gray", (start_x+10, start_y+10, INNER_SIZE, INNER_SIZE))

    if piece is None:
        return  # no shape available

    # draw piece shape
    for y in range(5):
        for x in range(5):
            if (x, y) not in piece.shape[0]:
                continue
            pygame.draw.rect(
                DISPLAY, piece.color, 
                (start_x + PIECE_MARGIN + x*BLOCK_SIZE - x*4,
                 start_y + PIECE_MARGIN*2 + y*BLOCK_SIZE - y*4,
                 BLOCK_SIZE,
                 BLOCK_SIZE)
            )
            pygame.draw.rect(
                DISPLAY, "black", 
                (start_x + PIECE_MARGIN + x*BLOCK_SIZE - x*4,
                 start_y + PIECE_MARGIN*2 + y*BLOCK_SIZE - y*4,
                 BLOCK_SIZE,
                 BLOCK_SIZE), 4
            )


def get_ai_inputs(game):
    """Produces a position calculated by the A.I. And returns the inputs to reach the position."""
    ai_tetris = copy.deepcopy(game)
    position = ai_move(ai_tetris)
    if position.using_held:
        game.hold_piece()

    return position.inputs


def handle_event(game, event, ai, auto_move_timer):
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()

    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not game.running:
        game.reset()
        pygame.time.set_timer(auto_move_timer, 1000)

    # automatically moves down slowly
    if game.running and not ai.on and event.type == auto_move_timer:
        game.move(0, 1)

    if game.running and not ai.on and event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RIGHT:
            game.move(1, 0)
        if event.key == pygame.K_LEFT:
            game.move(-1, 0)

        if event.key == pygame.K_UP:
            game.rotate()

        if event.key == pygame.K_z:
            game.hold_piece()

        if event.key == pygame.K_RCTRL:
            game.hard_drop()

        # move down faster
        if event.key == pygame.K_DOWN:
            pygame.time.set_timer(auto_move_timer, 100)
            game.move(0, 1)

    if game.running and event.type == pygame.KEYDOWN and event.key == pygame.K_t:
        if ai.on:
            ai.turn_off()
        else:
            ai.turn_on(get_ai_inputs(game))

    # set speed back to normal when you release down
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_DOWN:
            pygame.time.set_timer(auto_move_timer, 1000)


def game_tick(game, ai, font):
        DISPLAY.fill("#EEEEEE")
        show_grid()
        game.line_clears()

        if not game.piece_alive:
            game.make_piece()
            if ai.on:
                ai.change_piece_executed(get_ai_inputs(game))

        piece_frame(NEXT_X, NEXT_Y, game.next)
        piece_frame(HELD_X, HELD_Y, game.held)
        ghost_piece(game)
        draw_pieces(game)

        if ai.on:
            ai.execute_move()
        
        # display score
        score_text = font.render(f"Score: {game.score}", False, "black")
        score_rect = score_text.get_rect(
            center=(GRID_WIDTH/2 + LEFT_MARGIN, TOP_MARGIN-5 - score_text.get_height()/2)
        )
        DISPLAY.blit(score_text, score_rect)


def menu_tick(game, font):
    """Displays menu screen and a piece in the middle shaped on a 5x5 grid with some text."""
    display_width, display_height = DISPLAY.get_size()[0], DISPLAY.get_size()[1]

    PIECE_MARGIN = (display_width+display_height) // 7
    BLOCK_SIZE = PIECE_MARGIN//3
    DISPLAY.fill(game.next.ghost_color)

    # draw piece
    for y in range(5):
        for x in range(5):
            if (x, y) not in game.next.shape[0]:
                continue
            pygame.draw.rect(
                DISPLAY, game.next.color,
                (x*BLOCK_SIZE + PIECE_MARGIN - x*7,
                 y*BLOCK_SIZE + PIECE_MARGIN - y*7,
                 BLOCK_SIZE,
                 BLOCK_SIZE)
            )
            pygame.draw.rect(
                DISPLAY, "black", 
                (x*BLOCK_SIZE + PIECE_MARGIN - x*7,
                 y*BLOCK_SIZE + PIECE_MARGIN - y*7,
                 BLOCK_SIZE,
                 BLOCK_SIZE), 10
            )
    # menu text
    instructions_text = font.render("Press Space to Begin", False, "white")
    instructions_rect = instructions_text.get_rect(
        center=((X_SCREEN_GRID_PAD+RIGHT_MARGIN+LEFT_MARGIN)//2, PIECE_MARGIN + BLOCK_SIZE*5)
    )
    DISPLAY.blit(instructions_text, instructions_rect)

    score_text = font.render(f"Your score is  {game.score}!", False, "white")
    score_rect = score_text.get_rect(
        center=((X_SCREEN_GRID_PAD//2 + LEFT_MARGIN), PIECE_MARGIN-BLOCK_SIZE)
    )
    DISPLAY.blit(score_text, score_rect)


def main():
    """Main function which runs pygame's game loop and calls updating functions every frame."""
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()
    font = pygame.font.Font("assets\pixeltype.ttf", 85)

    auto_move_timer = pygame.USEREVENT + 1
    pygame.time.set_timer(auto_move_timer, 1000)
    
    game = Game()
    ai = AiExecutor(game)
    while True:
        for event in pygame.event.get():
            handle_event(game, event, ai, auto_move_timer)

        if game.running:
            game_tick(game, ai, font)
        else:
            menu_tick(game, font)

        pygame.display.update()
        clock.tick(60)
