import math
import sys
from tabnanny import check
from xmlrpc.client import boolean

import pygame

pygame.init()

is_human_turn = True
grid_size = [6,7]
screen_size = (800, 700)
screen = pygame.display.set_mode(screen_size)

grid_coords = []
board = []


for i in range(7):
    board.append([])
    for j in range(6):
        board[i].append('n')

def is_draw(b):
    for i in range(7):
        for j in range(6):
            if b[i][j] == 'n':
                return False
    return True

def check_win(b):

    for i in range(4):
        for j in range(6):
            if b[i][j] == b[i+1][j] and b[i][j] == b[i+2][j] and b[i][j] == b[i+3][j] and b[i][j] != 'n':
                return b[i][j]

    for i in range(7):
        for j in range(3):
            if b[i][j] == b[i][j+1] and b[i][j] == b[i][j+2] and b[i][j] == b[i][j+3] and b[i][j] != 'n':
                return b[i][j]

    for i in range(4):
        for j in range(3):
            if b[i][j] == b[i + 1][j + 1] and b[i][j] == b[i + 2][j + 2] and b[i][j] == b[i + 3][j + 3] and b[i][j] != 'n':
                return b[i][j]
            if b[6-i][j] == b[(6 - i) - 1][j + 1] and b[6-i][j] == b[(6-i) - 2][j + 2] and b[6-i][j] == b[(6-i) - 3][j + 3] and b[6-i][j] != 'n':
                return b[6-i][j]
    return 'n'

def place_piece(color,column):
    for i in range(6):
        if(board[column][5-i] == 'n'):
            board[column][5-i] = color
            break

def draw_board(board):
    screen.fill((75, 75, 200))
    for i in range(len(board)):
        for j in range(len(board[0])):

            if board[i][j] == 'y':
                pygame.draw.circle(screen,(255,255,0),(i*(screen_size[0]/7)+screen_size[0]/14,j*(screen_size[1]/6)+screen_size[1]/12),screen_size[0]/14-10)

            if board[i][j] == 'n':
                pygame.draw.circle(screen,(50,50,50),(i*(screen_size[0]/7)+screen_size[0]/14,j*(screen_size[1]/6)+screen_size[1]/12),screen_size[0]/14-10)

            if board[i][j] == 'r':
                pygame.draw.circle(screen, (255, 0, 0), (i*(screen_size[0]/7)+screen_size[0]/14,j*(screen_size[1]/6)+screen_size[1]/12),screen_size[0]/14-10)

    pygame.display.flip()

def evaluate_board(b):
    score = 0
    if check_win(b) == 'r':
        score = -1
    elif check_win(b) == 'y':
        score = 1
    return score

def get_valid_moves(b):
    valid_moves = []

    for i in range(7):
        if b[i][0] == 'n':
            valid_moves.append(i)

    return valid_moves

def simulate_move(board, column, piece):
    temp_board = [row[:] for row in board]
    for i in range(6):
        if temp_board[column][5 - i] == 'n':
            temp_board[column][5 - i] = piece
            break
    return temp_board

def minimax(b, depth, maximizing_player):
    # Check for terminal states (win, lose, draw) or depth limit
    if depth == 0 or check_win(b) != 'n' or is_draw(b):
        return evaluate_board(b)

    valid_moves = get_valid_moves(b)

    if maximizing_player:  # AI's turn (red, for example)
        max_eval = -math.inf
        for move in valid_moves:
            temp_board = simulate_move(b, move, 'y')
            eval = minimax(temp_board, depth - 1, False)
            max_eval = max(max_eval, eval)
        return max_eval

    else:  # Opponent's turn (yellow, for example)
        min_eval = math.inf
        for move in valid_moves:
            temp_board = simulate_move(b, move, 'r')
            eval = minimax(temp_board, depth - 1, True)
            min_eval = min(min_eval, eval)
        return min_eval

def get_best_move(b, depth):
    best_score = -math.inf
    best_move = None
    valid_moves = get_valid_moves(b)
    for move in valid_moves:
        temp_board = simulate_move(b, move, 'y')  # Simulate the AI move
        score = minimax(temp_board, depth-1, False)  # Opponent's turn
        print(str(move) + " " +str(score))
        if score >= best_score:
            best_score = score
            best_move = move
    return best_move
running = True
while running:
    if check_win(board) == 'y':
        print("OPPONENT WINS")
        running = False
    elif check_win(board) == 'r':
        print("YOU WIN")
        running = False
    elif is_draw(board):
        print("ITS A TIE")
        running = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and is_human_turn:
            column = math.floor(pygame.mouse.get_pos()[0]/(screen_size[0]/7))
            if(board[column][0] == 'n'):
                place_piece('r',column)
                is_human_turn = False
    draw_board(board)
    pygame.display.flip()
    if not is_human_turn:
        best_move = get_best_move(board, 6)
        place_piece('y', best_move)
        is_human_turn = True