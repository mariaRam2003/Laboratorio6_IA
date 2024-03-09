import numpy as np

class ConnectFour:
    def __init__(self):
        self.board = np.full((6, 7), None)  # Tablero 6x7
        self.players = {1: 'X', -1: 'O'}  # Jugador 1: X (IA), Jugador -1: O (Usuario)
        self.winning_positions = [
            [(i, j) for j in range(4)] for i in range(6)  # horizontal
        ] + [
            [(i, j) for i in range(3)] for j in range(7)  # vertical
        ] + [
            [(i, j) for i in range(3) for j in range(4)]  # diagonal \
        ] + [
            [(i, j) for i in range(3, 6) for j in range(3, 7)]  # diagonal /
        ]


        
    def is_valid_move(self, col):
        return self.board[0][col] is None
    
    def make_move(self, col, player):
        for row in range(5, -1, -1):
            if self.board[row][col] is None:
                self.board[row][col] = player
                return True
        return False
    
    def check_winner(self):
        for pos in self.winning_positions:
            values = [self.board[i][j] for i, j in pos]
            if all(v == 1 for v in values):
                return 1
            elif all(v == -1 for v in values):
                return -1
        return 0
    
    def minimax(self, depth, alpha, beta, maximizing_player):
        winner = self.check_winner()
        if depth == 0 or winner != 0:
            return winner, None
        
        if maximizing_player:
            max_eval = float('-inf')
            best_move = None
            for col in range(7):
                if self.is_valid_move(col):
                    self.make_move(col, 1)
                    eval, _ = self.minimax(depth - 1, alpha, beta, False)
                    self.board[np.where(self.board[:, col] != None)[0][-1], col] = None
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
                    if max_eval == eval:
                        best_move = col
            return max_eval, best_move
        else:
            min_eval = float('inf')
            for col in range(7):
                if self.is_valid_move(col):
                    self.make_move(col, -1)
                    eval, _ = self.minimax(depth - 1, alpha, beta, True)
                    self.board[np.where(self.board[:, col] != None)[0][-1], col] = None
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
            return min_eval, None
        
    def get_ai_move(self, depth, alpha_beta=True):
        _, move = self.minimax(depth, float('-inf'), float('inf'), True) if alpha_beta else self.minimax(depth, float('-inf'), float('inf'), True)
        return move
    
    def print_board(self):
        for row in self.board:
            print(' | '.join(map(lambda x: self.players.get(x, '_'), row)))  # Muestra 'X' para la IA y 'O' para el usuario
            print('-' * 23)

# Ejemplo de uso
game = ConnectFour()
game.print_board()

# Juego humano vs IA
while game.check_winner() == 0:
    human_move = int(input("Ingrese la columna donde desea colocar su ficha (0-6): "))
    if game.is_valid_move(human_move):
        game.make_move(human_move, -1)  # El usuario es 'O'
        game.print_board()
        if game.check_winner() != 0:
            print("¡Has ganado!")
            break
        ai_move = game.get_ai_move(depth=3, alpha_beta=True)
        game.make_move(ai_move, 1)  # La IA es 'X'
        game.print_board()
        if game.check_winner() != 0:
            print("¡La IA ha ganado!")
            break
    else:
        print("Movimiento inválido, por favor intenta de nuevo.")
