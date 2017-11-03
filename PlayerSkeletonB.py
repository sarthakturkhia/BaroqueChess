'''PlayerSkeletonB.py
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
    move = ((1, 2), (3, 2))

    # Make up a new remark
    newRemark = "I'm not very good at this game yet. I am not moving, which isn't legal, but... whatever."
    return [[move, newState], newRemark]

def nickname():
    return "Cheetie"

def introduce():
    return "I'm Cheetie Playah.  I haven't learned the rules of Baroque Chess yet."

def prepare(player2Nickname):
    pass


