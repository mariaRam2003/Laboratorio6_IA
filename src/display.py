import pygame

# Define colors for the game in RGB code
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Board dimensions for Connect Four game
ROW_COUNT = 6
COLUMN_COUNT = 7

class BoardDisplay:
    """
    A class that represents the display of the Connect Four game board.

    Attributes:
    - square_size (int): The size of each square on the board.
    - width (int): The width of the board.
    - height (int): The height of the board.
    - size (tuple): The size of the board (width, height).
    - radius (int): The radius of the circles representing the game pieces.
    - screen (pygame.Surface): The surface where the game is displayed.
    - font (pygame.font.Font): The font used for displaying the winner message.

    Methods:
    - draw_board(board): Draws the game board on the screen.
    - display_winner(player): Displays the winner message on the screen.
    """

    def __init__(self):
        """
        Initializes the BoardDisplay object.

        It sets up the pygame module, initializes the attributes, and creates the game screen.
        """
        pygame.init()
        self.square_size = 100
        self.width = COLUMN_COUNT * self.square_size
        self.height = (ROW_COUNT + 1) * self.square_size
        self.size = (self.width, self.height)
        self.radius = int(self.square_size / 2 - 5)
        self.screen = pygame.display.set_mode(self.size)
        self.font = pygame.font.SysFont("monospace", 75)

    def draw_board(self, board):
        """
        Draws the game board on the screen.

        Args:
        - board (list): A 2D list representing the game board.

        Each square on the board is drawn as a rectangle with a circle representing the game piece.
        The color of the circles depends on the player's piece (1 for red, 2 for yellow).
        """
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT):
                pygame.draw.rect(self.screen, BLUE, (c * self.square_size, r * self.square_size + self.square_size, self.square_size, self.square_size))
                pygame.draw.circle(self.screen, BLACK, (int(c * self.square_size + self.square_size / 2), int(r * self.square_size + self.square_size + self.square_size / 2)), self.radius)
        
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT):
                if board[r][c] == 1:
                    pygame.draw.circle(self.screen, RED, (int(c * self.square_size + self.square_size / 2), self.height - int(r * self.square_size + self.square_size / 2)), self.radius)
                elif board[r][c] == 2: 
                    pygame.draw.circle(self.screen, YELLOW, (int(c * self.square_size + self.square_size / 2), self.height - int(r * self.square_size + self.square_size / 2)), self.radius)
        pygame.display.update()

    def display_winner(self, player):
        """
        Displays the winner message on the screen.

        Args:
        - player (int): The player number (1 or 2) who won the game.

        The winner message is displayed at the top of the screen with the corresponding player's color.
        """
        color = RED if player == 1 else YELLOW
        label = self.font.render(f"Player {player} wins!!", 1, color)
        self.screen.blit(label, (40, 10))
        pygame.display.update()

    def draw_hover_piece(self, posx, player):
        """
        Draws a hovering piece on the screen.

        Parameters:
        - posx (int): The x-coordinate of the center of the circle.
        - player (int): The player number (1 or 2).

        Returns:
        None
        """
        color = RED if player == 1 else YELLOW
        pygame.draw.rect(self.screen, BLACK, (0, 0, self.width, self.square_size))
        pygame.draw.circle(self.screen, color, (posx, int(self.square_size / 2)), self.radius)
        pygame.display.update()

    def draw_blank(self): 
        """
        Draws a blank screen.

        Returns:
        None
        """
        self.screen.fill(BLACK)
        pygame.draw.rect(self.screen, BLACK, (0, 0, self.width, self.square_size))