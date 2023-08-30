import sys
import copy

from .ai import ai_move
from .classes import Game
from .constants import IS_MAIN_PROCESS, INVIS_GRID_TOP, Movement, GridBlock as GB

SPACE = 30
GRID_WIDTH = SPACE*10
GRID_HEIGHT = SPACE*20

RIGHT_MARGIN, LEFT_MARGIN = 350, 350
BOTTOM_MARGIN, TOP_MARGIN = 100, 150

NEXT_X, NEXT_Y = 700, 150
HELD_X, HELD_Y = 50, 150

if IS_MAIN_PROCESS:
    import pygame

    pygame.init()
    DISPLAY = pygame.display.set_mode(
        (GRID_WIDTH+RIGHT_MARGIN+LEFT_MARGIN, GRID_HEIGHT+TOP_MARGIN+BOTTOM_MARGIN)
    )


def show_grid():
    """Draw a red rectangle around the grid and the gray lines which divide each block."""
    RECT_THICKNESS = 10
    red_rect = pygame.draw.rect(
        DISPLAY, "red", (LEFT_MARGIN-10, TOP_MARGIN-10, 321, 621), RECT_THICKNESS
    )

    for line in range(1, 10):
        pygame.draw.line(
            DISPLAY, "dark gray", 
            (line*SPACE + LEFT_MARGIN, red_rect.top+RECT_THICKNESS),
            (line*SPACE + LEFT_MARGIN, red_rect.bottom-RECT_THICKNESS-1)
        )

    for line in range(1, 20):
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
                (col_idx*SPACE + LEFT_MARGIN, (row_idx-INVIS_GRID_TOP) * SPACE + TOP_MARGIN,
                 SPACE-1, SPACE-1)
            )
            pygame.draw.rect(
                DISPLAY, "black", 
                (col_idx*SPACE + LEFT_MARGIN, (row_idx-INVIS_GRID_TOP) * SPACE + TOP_MARGIN,
                 SPACE+1, SPACE+1), 3
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
                 SPACE-1, SPACE-1)
            )
            pygame.draw.rect(
                DISPLAY, "black", 
                (col_idx*SPACE + LEFT_MARGIN,
                 (row_idx-INVIS_GRID_TOP+downs_counter) * SPACE + TOP_MARGIN,
                 SPACE+1, SPACE+1), 3
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
                 BLOCK_SIZE, BLOCK_SIZE)
            )
            pygame.draw.rect(
                DISPLAY, "black", 
                (start_x + PIECE_MARGIN + x*BLOCK_SIZE - x*4,
                 start_y + PIECE_MARGIN*2 + y*BLOCK_SIZE - y*4,
                 BLOCK_SIZE, BLOCK_SIZE), 4
            )


def do_ai_move(game, ai_input):
    """Gets a specific instruction and calls its function."""
    if ai_input == Movement.ROTATION:
        game.rotate()
    elif ai_input == Movement.RIGHT:
        game.move(1, 0)
    elif ai_input == Movement.LEFT:
        game.move(-1, 0)
    elif ai_input == Movement.DOWN:
        game.move(0, 1)
    else:
        game.hard_drop()


def get_ai_inputs(game):
    """Produces a position calculated by the A.I. And returns the inputs to reach the position."""
    ai_tetris = copy.deepcopy(game)
    position = ai_move(ai_tetris)
    if position.using_held:
        game.hold_piece()

    return position.inputs


def menu(game, font):
    """Displays menu screen and a piece in the middle shaped on a 5x5 grid with some text."""
    BLOCK_SIZE = 100
    PIECE_MARGIN = 250

    DISPLAY.fill(game.next.ghost_color)

    for y in range(5):
        for x in range(5):
            if (x, y) not in game.next.shape[0]:
                continue
            pygame.draw.rect(
                DISPLAY, game.next.color,
                (x*BLOCK_SIZE + PIECE_MARGIN - x*7,
                 y*BLOCK_SIZE + PIECE_MARGIN - y*7,
                 BLOCK_SIZE, BLOCK_SIZE)
            )
            pygame.draw.rect(
                DISPLAY, "black", 
                (x*BLOCK_SIZE + PIECE_MARGIN - x*7,
                 y*BLOCK_SIZE + PIECE_MARGIN - y*7,
                 BLOCK_SIZE, BLOCK_SIZE), 10
            )
                
    instructions = font.render("Press Space to Begin", False, "white")
    instructions_rect = instructions.get_rect(
        center=((GRID_WIDTH+RIGHT_MARGIN+LEFT_MARGIN)/2, 700)
    )
    DISPLAY.blit(instructions, instructions_rect)

    score_text = font.render(f"Your score is  {game.score}!", False, "white")
    score_rect = score_text.get_rect(
        center=((GRID_WIDTH+RIGHT_MARGIN+LEFT_MARGIN)/2, 200)
    )
    DISPLAY.blit(score_text, score_rect)


def main():
    """Main function which runs pygame while loop and calls functions every frame."""
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()
    font = pygame.font.Font("assets\pixeltype.ttf", 85)

    auto_move_timer = pygame.USEREVENT + 1
    pygame.time.set_timer(auto_move_timer, 1000)

    music = pygame.mixer.Sound("assets\\audio\\Music.mp3")
    music.set_volume(0.6)
    music.play(loops=-1)
    
    ai_on = False
    input_idx = 0
    game = Game()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not game.running:
                game.running = True
                pygame.time.set_timer(auto_move_timer, 1000)

            # automatically moves down slowly
            if game.running and not ai_on and event.type == auto_move_timer:
                game.move(0, 1)

            if game.running and not ai_on and event.type == pygame.KEYDOWN:
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
                if ai_on:
                    ai_on = False
                    input_idx = 0
                else:
                    ai_on = True
                    ai_inputs = get_ai_inputs(game)

            # set speed back to normal when you release down
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    pygame.time.set_timer(auto_move_timer, 1000)

        if game.running:
            DISPLAY.fill("#EEEEEE")
            show_grid()
            game.line_clears()

            if not game.piece_alive:
                game.make_piece()
                if ai_on:
                    input_idx = 0
                    ai_inputs = get_ai_inputs(game)

            piece_frame(NEXT_X, NEXT_Y, game.next)
            piece_frame(HELD_X, HELD_Y, game.held)
            ghost_piece(game)
            draw_pieces(game)

            if ai_on:
                do_ai_move(game, ai_inputs[input_idx])
                input_idx += 1
            
            # display score
            score_text = font.render(f"Score: {game.score}", False, "black")
            score_rect = score_text.get_rect(
                bottomleft=(GRID_WIDTH/2 - score_text.get_width()/2 + LEFT_MARGIN, TOP_MARGIN-15)
            )
            DISPLAY.blit(score_text, score_rect)
        else:
            menu(game, font)

        pygame.display.update()
        clock.tick(60)
