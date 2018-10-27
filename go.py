from search import *
from utils import *
import math

# TAI content
def c_peg ():
	return "O"

def c_empty ():
	return "_"

def c_blocked ():
	return "X"

def is_empty (e):
	return e == c_empty()

def is_peg (e):
	return e == c_peg()

def is_blocked (e):
	return e == c_blocked()

# TAI pos
# Tuplo (l, c)
def make_pos (l, c):
	return (l, c)

def pos_l (pos):
	return pos[0]

def pos_c (pos):
	return pos[1]


# TAI move
# Lista [p_initial, p_final]
def make_move (i, f):
	return [i, f]

def move_initial (move):
	return move[0]

def move_final (move):
	return move[1]

# TAI board
# Lista de listas

def board_moves(board):
	result = []
	for i in range(0, len(board)):
		for j in range(0, len(board[i])):

			if not is_empty(board[i][j]) or is_blocked(board[i][j]):
				continue

			else:
				if i < len(board) - 2:
					#verifica abaixo
					if is_peg(board[i+1][j]) and is_peg(board[i+2][j]):
						result+= [make_move(make_pos(i +2,j), make_pos(i,j))]



				if i > 1:
					#verifica acima
					if is_peg(board[i-1][j]) and is_peg(board[i-2][j]):
						result+= [make_move(make_pos(i - 2,j), make_pos(i,j))]


				if j > 1:
					#verifica esquerda
					if is_peg(board[i][j - 1]) and is_peg(board[i][j - 2]):
						result+= [make_move(make_pos(i,j - 2), make_pos(i,j))]


				if j < len(board[i]) - 2:
					#verifica direita
					if is_peg(board[i][j + 1]) and is_peg(board[i][j + 2]):
						result+= [make_move(make_pos(i,j + 2), make_pos(i,j))]

	return result


def board_perform_move(board, move):
	new_board = board.copy()

	for i in range(0, len(board)):
		new_board[i] = board[i].copy()



	new_board[pos_l(move_initial(move))][pos_c(move_initial(move))] = c_empty()
	new_board[pos_l(move_final(move))][pos_c(move_final(move))] = c_peg()

	if(pos_l(move_initial(move)) == pos_l(move_final(move))):
		new_board[pos_l(move_initial(move))][(pos_c(move_initial(move)) + pos_c(move_final(move))) // 2] = c_empty()

	elif(pos_c(move_initial(move)) == pos_c(move_final(move))):
		new_board[(pos_l(move_initial(move)) + pos_l(move_final(move))) // 2][pos_c(move_initial(move))] = c_empty()

	return new_board


class sol_state:

	def __init__(self, board, h = -1):

		self.board = board

		#h e o numero de pecas
		self.h = h

		self.moves = board_moves(self.board)

		if(h == -1):
			self.h = 0
			for i in range(0, len(board)):
				for j in range(0, len(board[i])):

					if is_peg(self.board[i][j]):
						self.h+= 1

	def __lt__(self, other_state):
		if (self.h > other_state.h ):
			return True
		else:
			return False


class solitaire(Problem):
	"""Models a Solitaire problem as a satisfaction problem.
	A solution cannot have more than 1 peg left on the board."""
	def __init__(self, board):
		self.initial = sol_state(board)


	def actions(self, state): #fazer iterador?

		return state.moves


	def result(self, state, action):


		return sol_state(board_perform_move(state.board, action), state.h - 1)


	def goal_test(self, state):

		return state.h == 1


	def path_cost(self, c, state1, action, state2):
		#caminhos nao tem custo
		return 0

	def h(self, node):
		"""Needed for informed search."""

		return node.state.h - len(node.state.moves)
