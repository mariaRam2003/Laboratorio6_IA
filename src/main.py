import sys
import pygame
import math
from connect4 import ConnectFour
from display import BoardDisplay

# This program is a modularized version of the Connect Four game found at:
# https://github.com/KeithGalli/Connect4-Python


def main():
    """
    The main function that runs the Connect Four game.
    """
    game = ConnectFour()
    display = BoardDisplay()
    display.draw_board(game.board)

    while not game.game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            
            if event.type == pygame.MOUSEMOTION:
                posx = event.pos[0]
                player = 1 if game.turn == 0 else 2
                display.draw_hover_piece(posx, player)

            if event.type == pygame.MOUSEBUTTONDOWN:
                display.draw_blank()
                posx = event.pos[0]
                col = int(math.floor(posx / display.square_size))

                # Determine the player and piece to be dropped
                if game.turn == 0:  # Player 1
                    piece = 1
                else:  # Player 2
                    piece = 2

                # Play the turn and check for a win
                if game.play_turn(col, piece):
                    display.display_winner(game.turn + 1)
                    game.game_over = True

                # Update the display
                display.draw_board(game.board)

                # Switch turns
                game.turn = (game.turn + 1) % 2

                if game.game_over:
                    pygame.time.wait(3000)

if __name__ == "__main__":
    main()