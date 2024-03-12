"""
Este programa es una versión modificada del juego Conecta Cuatro encontrado en:
https://github.com/KeithGalli/Connect4-Python
El programa original fue escrito por Keith Galli y se modificó para
permitir al jugador seleccionar el modo de juego y habilitar la poda alfa-beta.

El programa implementa el juego Conecta Cuatro utilizando la biblioteca pygame.
Incluye funciones para crear el tablero del juego, soltar piezas,
verificar un movimiento ganador, evaluar la puntuación de una posición,
y seleccionar el mejor movimiento utilizando un algoritmo minimax simple
o un algoritmo minimax más complejo con poda alfa-beta.

El juego se puede jugar en dos modos:
1. Jugador vs IA: El jugador puede jugar contra la IA.
2. IA vs IA: Se crean 2 IA que juegan contra ellas (una mas compleja que la otra).

Para iniciar el juego, ejecute el script y seleccione el modo de juego.
Si la poda alfa-beta está habilitada, la IA utilizará el algoritmo minimax más complejo.
De lo contrario, utilizará el algoritmo minimax simple.

Si el modo de juego es "Jugador vs IA", el jugador puede soltar una pieza haciendo clic en la columna deseada.
Si el modo de juego es "IA vs IA", el juego se ejecutará automáticamente y se mostrará el ganador al final.
    La IA más compleja siempre jugará primero. (color ROJO)
	La IA menos compleja siempre jugará segundo. (color AMARILLO)
"""
import numpy as np
import random
import pygame
import sys
import math

# Definición de colores en formato RGB
BLUE = (0,0,255)  # Azul
BLACK = (0,0,0)  # Negro
RED = (255,0,0)  # Rojo
YELLOW = (255,255,0)  # Amarillo

# Definición de las dimensiones del tablero de juego
ROW_COUNT = 6  # Número de filas
COLUMN_COUNT = 7  # Número de columnas

# Definición de los jugadores
PLAYER = 0 
AI = 1

# Definición de los estados de las celdas del tablero
EMPTY = 0  # Celda vacía
PLAYER_PIECE = 1  # Ficha del jugador
AI_PIECE = 2  # Ficha de la ia

# Definición de la longitud de la ventana de juego
WINDOW_LENGTH = 4 


def create_board():
	board = np.zeros((ROW_COUNT,COLUMN_COUNT))
	return board


def drop_piece(board, row, col, piece):
	board[row][col] = piece


def is_valid_location(board, col):
	return board[ROW_COUNT-1][col] == 0


def get_next_open_row(board, col):
	for r in range(ROW_COUNT):
		if board[r][col] == 0:
			return r


def print_board(board):
	print(np.flip(board, 0))


def winning_move(board, piece):
    # Verificar las ubicaciones horizontales para ganar
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT):
			if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
				return True

    # Verificar las ubicaciones verticales para ganar
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
				return True

    # Verificar las diagonales con pendiente positiva
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
				return True

    # Verificar las diagonales con pendiente negativa
	for c in range(COLUMN_COUNT-3):
		for r in range(3, ROW_COUNT):
			if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
				return True


def evaluate_window(window, piece):
	score = 0
	opp_piece = PLAYER_PIECE
	if piece == PLAYER_PIECE:
		opp_piece = AI_PIECE

	if window.count(piece) == 4:
		score += 100
	elif window.count(piece) == 3 and window.count(EMPTY) == 1:
		score += 5
	elif window.count(piece) == 2 and window.count(EMPTY) == 2:
		score += 2

	if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
		score -= 4

	return score


def score_position(board, piece):
	score = 0

    # Puntuar columna central
	center_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
	center_count = center_array.count(piece)
	score += center_count * 3

    # Puntuar Horizontalmente
	for r in range(ROW_COUNT):
		row_array = [int(i) for i in list(board[r,:])]
		for c in range(COLUMN_COUNT-3):
			window = row_array[c:c+WINDOW_LENGTH]
			score += evaluate_window(window, piece)

    # Puntuar Verticalmente
	for c in range(COLUMN_COUNT):
		col_array = [int(i) for i in list(board[:,c])]
		for r in range(ROW_COUNT-3):
			window = col_array[r:r+WINDOW_LENGTH]
			score += evaluate_window(window, piece)

    # Puntuar diagonal con pendiente positiva
	for r in range(ROW_COUNT-3):
		for c in range(COLUMN_COUNT-3):
			window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
			score += evaluate_window(window, piece)
			
    # Puntuar diagonal con pendiente negativa
	for r in range(ROW_COUNT-3):
		for c in range(COLUMN_COUNT-3):
			window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
			score += evaluate_window(window, piece)

	return score


def is_terminal_node(board):
	return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0


def complex_minimax(board, depth, alpha, beta, maximizingPlayer):
	valid_locations = get_valid_locations(board)
	is_terminal = is_terminal_node(board)
	if depth == 0 or is_terminal:
		if is_terminal:
			if winning_move(board, AI_PIECE):
				return (None, 100000000000000)
			elif winning_move(board, PLAYER_PIECE):
				return (None, -10000000000000)
			else:  # El juego ha terminado, no hay más movimientos válidos
				return (None, 0)
		else: # pofundidad es cero
			return (None, score_position(board, AI_PIECE))
	if maximizingPlayer:
		value = -math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = get_next_open_row(board, col)
			b_copy = board.copy()
			drop_piece(b_copy, row, col, AI_PIECE)
			new_score = complex_minimax(b_copy, depth-1, alpha, beta, False)[1]
			if new_score > value:
				value = new_score
				column = col
			alpha = max(alpha, value)
			if alpha >= beta:
				break
		return column, value

	else: # Minimizando al jugador
		value = math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = get_next_open_row(board, col)
			b_copy = board.copy()
			drop_piece(b_copy, row, col, PLAYER_PIECE)
			new_score = complex_minimax(b_copy, depth-1, alpha, beta, True)[1]
			if new_score < value:
				value = new_score
				column = col
			beta = min(beta, value)
			if alpha >= beta:
				break
		return column, value


def simple_minimax(board, depth, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PIECE):
                return (None, 100000000000000)
            elif winning_move(board, PLAYER_PIECE):
                return (None, -10000000000000)
            else:  # El juego ha terminado, no hay más movimientos válidos
                return (None, 0)
        else:  # pofundidad es cero
            return (None, score_position(board, AI_PIECE))
    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_PIECE)
            new_score = simple_minimax(b_copy, depth - 1, False)[1]
            if new_score > value:
                value = new_score
                column = col
        return column, value
    else:  # Minimizando al jugador
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            new_score = simple_minimax(b_copy, depth - 1, True)[1]
            if new_score < value:
                value = new_score
                column = col
        return column, value


def get_valid_locations(board):
	valid_locations = []
	for col in range(COLUMN_COUNT):
		if is_valid_location(board, col):
			valid_locations.append(col)
	return valid_locations


def pick_best_move(board, piece):

	valid_locations = get_valid_locations(board)
	best_score = -10000
	best_col = random.choice(valid_locations)
	for col in valid_locations:
		row = get_next_open_row(board, col)
		temp_board = board.copy()
		drop_piece(temp_board, row, col, piece)
		score = score_position(temp_board, piece)
		if score > best_score:
			best_score = score
			best_col = col

	return best_col


def draw_board(board):
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):
			pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
			pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
	
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):		
			if board[r][c] == PLAYER_PIECE:
				pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
			elif board[r][c] == AI_PIECE: 
				pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
	pygame.display.update()


def select_game_mode():
	print("Bienvenido a Conecta 4!")
	print("Modos de juego:")
	print("1. Jugador vs IA")
	print("2. IA vs IA")
	game_mode = input("Seleccione el modo de juego: (1|2)")
	while game_mode not in ["1", "2"]:
		print("Modo de juego no válido")
		game_mode = input("Seleccione el modo de juego: (1|2)")
	return game_mode


def enable_pruning():
	print("Desea habilitar la poda alfa-beta?")
	print("1. Sí")
	print("2. No")
	pruning = input("Seleccione la opción: (1|2)")
	while pruning not in ["1", "2"]:
		print("Opción no válida")
		pruning = input("Seleccione la opción: (1|2)")
	if pruning == "1":
		return True
	else:  
		return False


game_mode = select_game_mode()


if game_mode == "1":
    pruning_enabled = enable_pruning()
    board = create_board()
    print_board(board)
    game_over = False
    
    pygame.init()

    SQUARESIZE = 100

    width = COLUMN_COUNT * SQUARESIZE
    height = (ROW_COUNT+1) * SQUARESIZE

    size = (width, height)

    RADIUS = int(SQUARESIZE/2 - 5)

    screen = pygame.display.set_mode(size)
    draw_board(board)
    pygame.display.update()

    myfont = pygame.font.SysFont("monospace", 75)

    turn = random.randint(PLAYER, AI)

    while not game_over:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
                posx = event.pos[0]
                if turn == PLAYER:
                    pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)

            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
                # Solicitar entrada del jugador
                if turn == PLAYER:
                    posx = event.pos[0]
                    col = int(math.floor(posx/SQUARESIZE))

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, PLAYER_PIECE)

                        if winning_move(board, PLAYER_PIECE):
                            label = myfont.render("Player 1 wins!!", 1, RED)
                            screen.blit(label, (40,10))
                            game_over = True

                        turn += 1
                        turn = turn % 2

                        print_board(board)
                        draw_board(board)

        # Solicitar entrada de IA
        if turn == AI and not game_over:
			# Solicitar si habilitar la poda alfa-beta
            if pruning_enabled:
                col, minimax_score = complex_minimax(board, 5, -math.inf, math.inf, True)
            else:
                col, minimax_score = simple_minimax(board, 5, True)

            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, AI_PIECE)

                if winning_move(board, AI_PIECE):
                    label = myfont.render("Player 2 wins!!", 1, YELLOW)
                    screen.blit(label, (40,10))
                    game_over = True

                print_board(board)
                draw_board(board)

                turn += 1
                turn = turn % 2

        if game_over:
            pygame.time.wait(2000)
			
else:
	move_count = 0
	board = create_board()
	
	print_board(board)
	
	game_over = False
	pygame.init()
	
	SQUARESIZE = 100
	
	width = COLUMN_COUNT * SQUARESIZE
	height = (ROW_COUNT+1) * SQUARESIZE
	
	size = (width, height)
	
	RADIUS = int(SQUARESIZE/2 - 5)
	
	screen = pygame.display.set_mode(size)
	
	draw_board(board)
	pygame.display.update()
	
	myfont = pygame.font.SysFont("monospace", 75)
	turn = random.randint(PLAYER, AI)
	
	while not game_over:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
				
			pygame.display.update()
			
        # Solicitar entrada de IA con poda alfa-beta
		if turn == PLAYER:
			if move_count == 0:
				col = random.choice([0, 1, 2, 3, 4, 5, 6])
			else:
				col, minimax_score = complex_minimax(board, 5, -math.inf, math.inf, True)
				
			if is_valid_location(board, col):
				row = get_next_open_row(board, col)
				drop_piece(board, row, col, PLAYER_PIECE)
				move_count += 1
				
				if winning_move(board, PLAYER_PIECE):
					label = myfont.render("Player 1 wins!!", 1, RED)
					screen.blit(label, (40,10))
					game_over = True
					
				print_board(board)
				draw_board(board)
				
				turn += 1
				turn = turn % 2
				
				print_board(board)
				draw_board(board)
				
		# Solicitar entrada de IA sin poda alfa-beta
		if turn == AI and not game_over:
			col, minimax_score = simple_minimax(board, 5, False)
			
			if is_valid_location(board, col):
				row = get_next_open_row(board, col)
				drop_piece(board, row, col, AI_PIECE)
				
				if winning_move(board, AI_PIECE):
					label = myfont.render("Player 2 wins!!", 1, YELLOW)
					screen.blit(label, (40,10))
					game_over = True
					
				print_board(board)
				draw_board(board)
				
				turn += 1
				turn = turn % 2
				
		if game_over:
			pygame.time.wait(2000)