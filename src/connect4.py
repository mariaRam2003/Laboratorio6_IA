import numpy as np

# Board dimensions for Connect Four game
ROW_COUNT = 6
COLUMN_COUNT = 7

class ConnectFour:
    """
    Connect Four game class.
    """

    def __init__(self):
        """
        Initializes the Connect Four game.
        """
        self.board = np.zeros((ROW_COUNT,COLUMN_COUNT))
        self.game_over = False
        self.turn = 0
        
        
    def drop_piece(self, row, col, piece):
        """
        Drops a game piece on the board.

        Args:
            row (int): The row index of the board.
            col (int): The column index of the board.
            piece (int): The game piece to be dropped.

        Returns:
            None
        """
        self.board[row][col] = piece
		

    def is_valid_location(self, col):
        """
        Checks if a column is a valid location to drop a game piece.

        Args:
            col (int): The column index of the board.

        Returns:
            bool: True if the column is a valid location, False otherwise.
        """
        return self.board[ROW_COUNT-1][col] == 0
	

    def get_next_open_row(self, col):
        """
        Gets the next open row in a column.

        Args:
            col (int): The column index of the board.

        Returns:
            int: The row index of the next open row.
        """
        for r in range(ROW_COUNT):
            if self.board[r][col] == 0:
                return r


    def winning_move(self, piece):
        """
        Checks if a player has won the game.

        Args:
            piece (int): The game piece to check for a win.

        Returns:
            bool: True if the player has won, False otherwise.
        """
        # Check horizontal locations for win
        for c in range(COLUMN_COUNT-3):
            for r in range(ROW_COUNT):
                if self.board[r][c] == piece and self.board[r][c+1] == piece and self.board[r][c+2] == piece and self.board[r][c+3] == piece:
                    return True

        # Check vertical locations for win
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT-3):
                if self.board[r][c] == piece and self.board[r+1][c] == piece and self.board[r+2][c] == piece and self.board[r+3][c] == piece:
                    return True

        # Check positively sloped diaganols
        for c in range(COLUMN_COUNT-3):
            for r in range(ROW_COUNT-3):
                if self.board[r][c] == piece and self.board[r+1][c+1] == piece and self.board[r+2][c+2] == piece and self.board[r+3][c+3] == piece:
                    return True

        # Check negatively sloped diaganols
        for c in range(COLUMN_COUNT-3):
            for r in range(3, ROW_COUNT):
                if self.board[r][c] == piece and self.board[r-1][c+1] == piece and self.board[r-2][c+2] == piece and self.board[r-3][c+3] == piece:
                    return True


    def play_turn(self, col, piece):
        """
        Plays a turn in the game.

        Args:
            col (int): The column index of the board.
            piece (int): The game piece to be dropped.

        Returns:
            bool: True if the player has won, False otherwise.
        """
        if self.is_valid_location(col):
            row = self.get_next_open_row(col)
            self.drop_piece(row, col, piece)
            if self.winning_move(piece):
                self.game_over = True
                return True
        return False
				
