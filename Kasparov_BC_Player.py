'''Kasaparov_BC_Player.py
The beginnings of an agent that might someday play Baroque Chess.

'''

import BC_state_etc as BC


def makeMove(currentState, currentRemark, timelimit):
    # Compute the new state for a move.
    # This is a placeholder that just copies the current state.
    newState = BC.BC_state(currentState.board)

    # Fix up whose turn it will be.
    newState.whose_move = 1 - currentState.whose_move

    # Construct a representation of the move that goes from the
    # currentState to the newState.
    # Here is a placeholder in the right format but with made-up
    # numbers:
    move = ((6, 4), (3, 4))

    # Make up a new remark
    newRemark = "I'll think harder in some future game. Here's my move"

    return [[move, newState], newRemark]

# takes a move and returns a new state of the complete board after the move was made
def getState(move):


#If our king is on check this method makes the moves to protect the king.
def ifonCheck():

# IF our piece is already checking the opponents king then try to finish the game.
def ifattacking():

# These functions should take a position as a parameter and return a list of all possible positions of that piece
def king():

def pincer():

def Knight():

def imitator():

def other():

def nickname():
    return "Kasper"


def introduce():
    return "I'm Kasparov a Russian Baroque Chess agent."


def prepare(player2Nickname):
    pass

# Mathematical sum of all the pieces we have based on a point system. + the position index in comparision to opponents
# pieces and our pieces in the kings diagonals, verticals and horizontals. subtract the same for our opponent from this sum.
def staticEval(state):
    return 0

