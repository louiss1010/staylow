# CONNECT 4 GAME
#Author: Louis Strehlow

# NOTE In this script, "player 1" always means the player with the red pieces
# and "player 2" always means the player with the yellow pieces.
# During actual on-screen gameplay, however, players are only and always referred to as "RED" or "YELLOW".

import pygame
import asyncio

# initialising pygame
pygame.init()
screen = pygame.display.set_mode((800,750))
pygame.display.set_caption("CONNECT 4")
clock = pygame.time.Clock()

# colour values
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"

# board width and height
board_width = 7
board_height = 6

# player piece symbols, useful for displaying the board in a CLI
red = f"{RED}O{RESET}"
yellow = f"{YELLOW}O{RESET}"

# player dictionary for colors
player_colour = {1: red, 2: yellow}

# game end overlay dictionary
game_end_dict = {1: "RED WINS", 2: "YELLOW WINS", 3: "DRAW"}

#saves last move played
last_move = [0,0]

# global statistics variables
player_turn = 1
player1_wins = 0
player2_wins = 0
draws = 0
games_played = 0
move_counts = []

# delay between game ending and UI appearing
game_end_delay = 1000

# initialising fonts
large_font = pygame.font.Font("fonts/PressStart2P-Regular.ttf", 50)
medium_font = pygame.font.Font("fonts/PressStart2P-Regular.ttf", 25)
small_font = pygame.font.Font("fonts/PressStart2P-Regular.ttf", 13)

#initialising pieces and slot graphics
slot = pygame.image.load("graphics/single_slot.png").convert_alpha()

red_surf = pygame.image.load("graphics/red_piece.png").convert_alpha()
red_rect = red_surf.get_rect(center = (300,50))

yellow_surf = pygame.image.load("graphics/yellow_piece.png").convert_alpha()
yellow_rect = yellow_surf.get_rect(center = (300,50))

# initialising main menu display
main_menu_rect = pygame.Rect(300, 350, 200, 100)

title_text_surface = large_font.render("CONNECT 4", True, "White")
title_text_rect = title_text_surface.get_rect(center = (main_menu_rect.centerx, main_menu_rect.centery - 180))

title_new_game_surface = medium_font.render("NEW GAME", True, "White")
title_new_game_surface_hover = medium_font.render("NEW GAME", True, "grey55")
title_new_game_rect = title_new_game_surface.get_rect(center = (main_menu_rect.centerx, main_menu_rect.centery - 40))

title_view_stats_surface = medium_font.render("VIEW STATS", True, "White")
title_view_stats_surface_hover = medium_font.render("VIEW STATS", True, "grey55")
title_view_stats_rect = title_view_stats_surface.get_rect(center = (main_menu_rect.centerx, main_menu_rect.centery + 60))

title_quit_surface = medium_font.render("QUIT", True, "White")
title_quit_surface_hover = medium_font.render("QUIT", True, "grey55")
title_quit_rect = title_quit_surface.get_rect(center = (main_menu_rect.centerx, main_menu_rect.centery + 100))

# initialising stats menu display
stats_rect = pygame.Rect(300, 350, 200, 100)

stats_header_surface = large_font.render("STATS", True, "White")
stats_header_rect = stats_header_surface.get_rect(center = (stats_rect.centerx, stats_rect.centery - 250))

stats_main_menu_surface = medium_font.render("MAIN MENU", True, "White")
stats_main_menu_surface_hover = medium_font.render("MAIN MENU", True, "grey55")
stats_main_menu_rect = stats_main_menu_surface.get_rect(center = (stats_rect.centerx, stats_rect.centery + 250))

# these get populated by update_stats_display() the first time the stats screen is shown
stats_total_games_played_surface = medium_font.render("TOTAL GAMES PLAYED: 0", True, "White")
stats_total_games_played_rect = stats_total_games_played_surface.get_rect(center = (stats_rect.centerx, stats_rect.centery - 150))
stats_player_1_wins_surface = medium_font.render("RED WINS: 0", True, "White")
stats_player_1_wins_rect = stats_player_1_wins_surface.get_rect(center = (stats_rect.centerx, stats_rect.centery - 100))
stats_player_2_wins_surface = medium_font.render("YELLOW WINS: 0", True, "White")
stats_player_2_wins_rect = stats_player_2_wins_surface.get_rect(center = (stats_rect.centerx, stats_rect.centery - 50))
stats_draws_surface = medium_font.render("DRAWS: 0", True, "White")
stats_draws_rect = stats_draws_surface.get_rect(center = (stats_rect.centerx, stats_rect.centery))
stats_average_moves_surface = None
stats_average_moves_rect = None
stats_shortest_game_surface = None
stats_shortest_game_rect = None
stats_longest_game_surface = None
stats_longest_game_rect = None

# initialising game end overlay display
game_end_rect = pygame.Rect(300,350, 200, 100)

game_end_main_menu_surface = small_font.render("MAIN MENU", True, "White")
game_end_main_menu_surface_hover = small_font.render("MAIN MENU", True, "grey55")
game_end_main_menu_rect = game_end_main_menu_surface.get_rect(center = (game_end_rect.centerx, game_end_rect.centery + 20))


def create_board():
    """
    Creates a new 6x7 matrix that functions as the board the users play on

    Args:
        None

    Returns:
        new_board - the newly created board to play the game on (2D list)
    """
    new_board = [["-" for i in range(board_width)] for j in range(board_height)]
    return new_board


def display_board(board:list):
    """
    Displays the current board state on the game window

    Args:
        board - the current board state (2D list)

    Returns:
        None
    """
    # displays the pieces, red or yellow, first, depending on the board state
    for i in range(0,6,1):
        for j in range(0,7,1):
            if board[i][j] == red:
                red_rect.center = ((j+1)*100 , (i+1)*100 + 50)
                screen.blit(red_surf, red_rect)
            elif board[i][j] == yellow:
                yellow_rect.center = ((j+1)*100 , (i+1)*100 + 50)
                screen.blit(yellow_surf, yellow_rect)

    # displays the slots over the pieces to look like the pieces are "inside" the board
    for i in range(0,7,1):
            for j in range(0,6,1):
                screen.blit(slot, (i*100+50, j*100+100))


def get_column_when_clicked(mouse_x:int):
    """
    Returns which column of the board the mouse is currently positioned over.
    If the mouse is outside of the board (in the x direction), returns the closest column, i.e., 0 or 6

    Args:
        mouse_x - x coordinate of the mouse (int)

    Returns:
        i - the column which the mouse is over, or closest to (int)
    """
    # check if mouse directly over the board
    for i in range(0,7,1):
        if i*100 + 50 <= mouse_x < (i+1)*100 + 50:
            return i
    # check if mouse is to the left of the board
    if 0 <= mouse_x < 50:
        return 0
    # check if mouse is to the right of the board
    if 750 <= mouse_x <= 800:
        return 6


def display_hovering_piece(mouse_x: int):
    """
    Displays a hovering piece above the column the user's mouse is over.
    The piece is red or yellow depending on whose turn it is.
    Note: "col is not None" should never be False, but it is included as a safety net.

    Args:
        mouse_x - x coordinate of the mouse (int)

    Returns:
        None
    """
    col = get_column_when_clicked(mouse_x)
    # hovers a red piece if it is player 1's turn
    if player_turn == 1:
        if col is not None:
            red_rect.center = ((1+col)*100, 50)
        screen.blit(red_surf, red_rect)
    # hovers a yellow piece if it is player 2's turn
    elif player_turn == 2:
        if col is not None:
            yellow_rect.center = ((1+col)*100, 50)
        screen.blit(yellow_surf, yellow_rect)


def valid_drop(board:list, column:int):
    """
    Checks whether the specified column has room for another piece (i.e. isn't full)

    Args:
        board - the current board state (2D list)
        column - the column to drop the piece

    Returns:
        Boolean - True if there is space to play in that column, False if not
    """
    return board[0][column] == "-"


def drop_piece(board:list, column:int, player:int):
    """
    Drops a red or yellow piece (depending on the player) in the specified column. The piece is dropped in the lowest row that currently doesn't contain a piece.
    Also updates the global variable last_move to [row, column] of the piece just placed.

    Args:
        board - the current board state (2D list)
        column - the column the piece will be dropped into
        player - the number of player whose turn it is (1 or 2)

    Returns:
        board - the new updated board with the piece placed
    """
    for i in range(board_height-1,-1,-1):
        if board[i][column] == "-":
            board[i][column] = player_colour[player]
            global last_move
            last_move = [i, column]
            return board


def draw_check(board:list):
    """
    Checks whether the current board is full (i.e. the game is drawn)

    Args:
        board - the current board state (2D list)

    Returns:
        Boolean - True if the board is full and the game is tied, False if the board is not full and the game can continue
    """
    for i in range(0,board_width,1):
        if valid_drop(board, i):
            return False
    return True


def vertical_check(board:list, last_move:list, player:int):
    """
    Checks whether a connect 4 has been made vertically, i.e. there are four pieces of the same colour stacked on top of each other.

    Args:
        board - the current board state (2D list)
        last_move - coordinates of the last move played as a list [row,column]
        player - the player who played the last move (1 or 2)

    Returns:
        Boolean - True if there is a vertical connect 4, False otherwise
    """
    # checks if the last move was in row 0, 1 or 2,
    # since you cannot make a vertical connect 4 from playing in rows 3, 4 or 5 (the bottom 3 rows)
    if last_move[0] in [0, 1, 2]:
        # checks if the three pieces below the one just played match the player's colour
        for i in range(last_move[0] + 1, last_move[0] + 4, 1):
            if board[i][last_move[1]] != player_colour[player]:
                return False
        return True
    else:
        return False


def horizontal_check(board:list, last_move:list, player:int):
    """
    Checks whether a connect 4 has been made horizontally, i.e. there are four pieces of the same colour in a horizontal row.

    Args:
        board - the current board state (2D list)
        last_move - coordinates of the last move played as a list [row,column]
        player - the player who played the last move (1 or 2)

    Returns:
        Boolean - True if there is a horizontal connect 4, False otherwise
    """
    count = 0 # initialise counting variable
    # scans across the whole row for the last player's colour, counting consecutive matches
    # resets the count when a non-matching piece is found
    for i in range(0,len(board[0]),1):
        if board[last_move[0]][i] == player_colour[player]:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    return False


def negative_diagonal_check(board:list, last_move:list, player:int):
    """
    Checks whether a connect 4 has been made on the negative diagonal (i.e. in the NW to SE direction).
    This will be called a "negative diagonal connect 4".

    Args:
        board - the current board state (2D list)
        last_move - coordinates of the last move played as a list [row,column]
        player - the player who played the last move (1 or 2)

    Returns:
        Boolean - True if there is a negative diagonal connect 4, False otherwise
    """
    current_point = last_move[:] # copies last_move to a pointer variable
    # moves the pointer variable to the furthest North-West point on the board from the last_move coordinate
    while current_point[0] > 0 and current_point[1] > 0:
        current_point[0] -= 1
        current_point[1] -= 1

    count = 0 # initialise counter variable
    # scans across the negative diagonal for the last player's colour, counting consecutive matches
    # resets the count when a non-matching piece is found
    while current_point[0] < board_height and current_point[1] < board_width:
        if board[current_point[0]][current_point[1]] == player_colour[player]:
            count += 1
            if count == 4:
                return True
            else:
                current_point[0] += 1
                current_point[1] += 1
        else:
            count = 0
            current_point[0] += 1
            current_point[1] += 1
    return False


def positive_diagonal_check(board:list, last_move:list, player:int):
    """
    Checks whether a connect 4 has been made on the positive diagonal (i.e. in the SW to NE direction).
    This will be called a "positive diagonal connect 4".

    Args:
        board - the current board state (2D list)
        last_move - coordinates of the last move played as a list [row,column]
        player - the player who played the last move (1 or 2)

    Returns:
        Boolean - True if there is a positive diagonal connect 4, False otherwise
    """
    current_point = last_move[:] # copies last_move to a pointer variable
    # moves the pointer variable to the furthest South-West point on the board from the last_move coordinate
    while current_point[0] < board_height - 1 and current_point[1] > 0:
        current_point[0] += 1
        current_point[1] -= 1

    count = 0 # initialise counter variable
    # scans across the positive diagonal for the last player's colour, counting consecutive matches
    # resets the count when a non-matching piece is found
    while current_point[0] >= 0 and current_point[1] < board_width:
        if board[current_point[0]][current_point[1]] == player_colour[player]:
            count += 1

            if count == 4:
                return True
            else:
                current_point[0] -= 1
                current_point[1] += 1
        else:
            count = 0
            current_point[0] -= 1
            current_point[1] += 1

    return False


def total_check(board:list, last_move:list, player:int):
    """
    Checks whether there is a connect 4 in any direction (vertically, horizontally, negative diagonally, positive diagonally)

    Args:
        board - the current board state (2D list)
        last_move - coordinates of the last move played as a list [row,column]
        player - the player who played the last move (1 or 2)

    Returns:
        Boolean - True if any win conditions are met, False otherwise
    """
    return vertical_check(board, last_move, player) or horizontal_check(board, last_move, player) or negative_diagonal_check(board, last_move, player) or positive_diagonal_check(board, last_move, player)


def display_game_end_overlay():
    """
    Draws a black rectangle with a white border.
    Only used after a game ends.

    Args:
        None

    Returns:
        None
    """
    pygame.draw.rect(screen, "Black", game_end_rect)
    pygame.draw.rect(screen, "White", game_end_rect, width = 3)


def update_stats_display():
    """
    Called whenever the stats screen is entered. Updates the text surfaces that display the current stats based on the updated global stats variables.

    Args:
        None

    Returns:
        None
    """
    global stats_total_games_played_surface, stats_total_games_played_rect
    global stats_player_1_wins_surface, stats_player_1_wins_rect
    global stats_player_2_wins_surface, stats_player_2_wins_rect
    global stats_draws_surface, stats_draws_rect
    global stats_average_moves_surface, stats_average_moves_rect
    global stats_shortest_game_surface, stats_shortest_game_rect
    global stats_longest_game_surface, stats_longest_game_rect


    stats_total_games_played_surface = medium_font.render(f"TOTAL GAMES PLAYED: {games_played}", True, "White")
    stats_total_games_played_rect = stats_total_games_played_surface.get_rect(center = (stats_rect.centerx, stats_rect.centery - 150))

    stats_player_1_wins_surface = medium_font.render(f"RED WINS: {player1_wins}", True, "White")
    stats_player_1_wins_rect = stats_player_1_wins_surface.get_rect(center = (stats_rect.centerx, stats_rect.centery - 100))

    stats_player_2_wins_surface = medium_font.render(f"YELLOW WINS: {player2_wins}", True, "White")
    stats_player_2_wins_rect = stats_player_2_wins_surface.get_rect(center = (stats_rect.centerx, stats_rect.centery - 50))

    stats_draws_surface = medium_font.render(f"DRAWS: {draws}", True, "White")
    stats_draws_rect = stats_draws_surface.get_rect(center = (stats_rect.centerx, stats_rect.centery))

    # only updates if a game has been played to avoid a /0 error
    if len(move_counts) != 0:

        stats_average_moves_surface = medium_font.render(f"AVERAGE MOVES: {sum(move_counts)/len(move_counts):.2f}", True, "White")
        stats_average_moves_rect = stats_average_moves_surface.get_rect(center = (stats_rect.centerx, stats_rect.centery + 50))

        stats_shortest_game_surface = medium_font.render(f"SHORTEST GAME: {min(move_counts)} MOVES", True, "White")
        stats_shortest_game_rect = stats_shortest_game_surface.get_rect(center = (stats_rect.centerx, stats_rect.centery + 100))

        stats_longest_game_surface = medium_font.render(f"LONGEST GAME: {max(move_counts)} MOVES", True, "White")
        stats_longest_game_rect = stats_longest_game_surface.get_rect(center = (stats_rect.centerx, stats_rect.centery + 150))


def start_new_game():
    """
    Resets all the per-game (not overall-stats) variables ready for a fresh game of Connect 4.
    Replaces the old "entering play_game()" step now that play has no loop of its own.

    Args:
        None

    Returns:
        None
    """
    global board, game_ended, draw_occurred, local_move_count
    board = create_board()
    game_ended = False
    draw_occurred = False
    local_move_count = 0


# ---------------------------------------------------------------------------
# Everything below here used to be three separate functions (main_menu(),
# play_game(), view_stats()) each with their own "while True:" loop, calling
# each other directly. That meant every trip back to the main menu nested a
# brand new loop inside the previous one instead of actually returning - the
# call stack only ever grew, it never shrank.
#
# Now there is ONE loop, and a "state" variable decides what to check for
# clicks on and what to draw each frame. Going back to the menu is just
# `state = "main_menu"` - a plain variable change, not a new function call.
# This also lets us "await asyncio.sleep(0)" once per frame, which is what
# lets the browser (via pygbag) breathe between frames instead of freezing.
# ---------------------------------------------------------------------------

state = "main_menu"

# per-game variables, initialised properly the first time start_new_game() runs
board = create_board()
game_ended = False
draw_occurred = False
local_move_count = 0
end_time = 0
game_end_text_surface = None
game_end_text_rect = None


async def main():
    global state, player_turn, player1_wins, player2_wins, draws, games_played, move_counts
    global board, game_ended, draw_occurred, local_move_count, end_time
    global game_end_text_surface, game_end_text_rect

    running = True

    while running:

        mouse_x, mouse_y = pygame.mouse.get_pos()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:

                # --- MAIN MENU clicks ---
                if state == "main_menu":
                    if title_new_game_rect.collidepoint(mouse_x, mouse_y):
                        start_new_game()
                        state = "play"
                    elif title_view_stats_rect.collidepoint(mouse_x, mouse_y):
                        update_stats_display()
                        state = "stats"
                    

                # --- PLAY clicks ---
                elif state == "play":
                    if not game_ended:
                        column = get_column_when_clicked(mouse_x)
                        # do nothing if the column is None (safety net) or the column is full
                        if column is not None and valid_drop(board, column):

                            drop_piece(board, column, player_turn)
                            local_move_count += 1

                            # check if the last move made a connect 4
                            if total_check(board, last_move, player_turn):
                                if player_turn == 1:
                                    who_win_or_draw = 1
                                    player1_wins += 1
                                elif player_turn == 2:
                                    who_win_or_draw = 2
                                    player2_wins += 1

                                games_played += 1
                                move_counts.append(local_move_count)

                                game_ended = True
                                end_time = pygame.time.get_ticks()

                                game_end_text_surface = small_font.render(game_end_dict[who_win_or_draw], True, "White")
                                game_end_text_rect = game_end_text_surface.get_rect(center = (game_end_rect.centerx, game_end_rect.centery - 20))

                            # check if the last move filled the board (i.e. the game is drawn)
                            elif draw_check(board):
                                who_win_or_draw = 3

                                games_played += 1
                                draws += 1
                                move_counts.append(local_move_count)

                                game_ended = True
                                draw_occurred = True
                                end_time = pygame.time.get_ticks()

                                game_end_text_surface = small_font.render(game_end_dict[who_win_or_draw], True, "White")
                                game_end_text_rect = game_end_text_surface.get_rect(center = (game_end_rect.centerx, game_end_rect.centery - 20))

                            # swaps whose turn it is to play next (1 <--> 2)
                            if not draw_occurred:
                                if player_turn == 1:
                                    player_turn = 2
                                elif player_turn == 2:
                                    player_turn = 1

                    # sends the user back to the main menu after the winning overlay has appeared
                    if game_ended and pygame.time.get_ticks() - end_time >= game_end_delay:
                        if game_end_main_menu_rect.collidepoint(mouse_x, mouse_y):
                            state = "main_menu"

                # --- STATS clicks ---
                elif state == "stats":
                    if stats_main_menu_rect.collidepoint(mouse_x, mouse_y):
                        state = "main_menu"

        # ------------------------- drawing -------------------------
        screen.fill("Black")

        if state == "main_menu":
            screen.blit(title_text_surface, title_text_rect)

            if title_new_game_rect.collidepoint(mouse_x, mouse_y):
                screen.blit(title_new_game_surface_hover, title_new_game_rect)
            else:
                screen.blit(title_new_game_surface, title_new_game_rect)

            if title_view_stats_rect.collidepoint(mouse_x, mouse_y):
                screen.blit(title_view_stats_surface_hover, title_view_stats_rect)
            else:
                screen.blit(title_view_stats_surface, title_view_stats_rect)


        elif state == "play":
            display_board(board)

            if game_ended:
                if pygame.time.get_ticks() - end_time >= game_end_delay:
                    display_game_end_overlay()
                    screen.blit(game_end_text_surface, game_end_text_rect)
                    if game_end_main_menu_rect.collidepoint(mouse_x, mouse_y):
                        screen.blit(game_end_main_menu_surface_hover, game_end_main_menu_rect)
                    else:
                        screen.blit(game_end_main_menu_surface, game_end_main_menu_rect)
            else:
                display_hovering_piece(mouse_x)

        elif state == "stats":
            screen.blit(stats_header_surface, stats_header_rect)
            screen.blit(stats_total_games_played_surface, stats_total_games_played_rect)
            screen.blit(stats_player_1_wins_surface, stats_player_1_wins_rect)
            screen.blit(stats_player_2_wins_surface, stats_player_2_wins_rect)
            screen.blit(stats_draws_surface, stats_draws_rect)

            if len(move_counts) != 0:
                screen.blit(stats_average_moves_surface, stats_average_moves_rect)
                screen.blit(stats_shortest_game_surface, stats_shortest_game_rect)
                screen.blit(stats_longest_game_surface, stats_longest_game_rect)

            if stats_main_menu_rect.collidepoint(mouse_x, mouse_y):
                screen.blit(stats_main_menu_surface_hover, stats_main_menu_rect)
            else:
                screen.blit(stats_main_menu_surface, stats_main_menu_rect)

        pygame.display.update()
        clock.tick(60)

        # hands control back to the browser each frame - this is the pygbag-critical line
        await asyncio.sleep(0)

    pygame.quit()


asyncio.run(main())
