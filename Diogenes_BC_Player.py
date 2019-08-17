"""Jaskeerat Sethi (sethij), Graham Still (gstill)
CSE 415 Autumn 2017
Instructor: Steve Tanimoto
Assignment 5
Baroque Chess Agent"""

# Python library imports
from math import inf
import time

# Provided assignment code imports
from BC_state_etc import BC_state

# Project module imports
from Diogenes_BC_module_state import DiogenesState
from Diogenes_BC_module_constants import *
from Diogenes_BC_module_operator import OPERATORS


# Caches
stateValues = {}  # Calculated evaluations of states
stateDepths = {}  # Depths the search used when calculating the evaluations

deadline = 0  # The time at which search should end


def introduce():
    return """Greetings! I am Diogenes of Sinope. I have been resurrected in thought by Jaskeerat Sethi (sethij)
and Graham Still (gstill) to beat you in Baroque Chess. I am a citizen of the world and what I
like to drink most is wine that belongs to others."""


def nickname():
    return "Diogenes"


def prepare(opponentNickname):
    pass


def makeMove(currentState, currentRemark, timeLimit=10000):
    """
    Finds the best move given the current state

    :param currentState:      The current state of the game
    :param str currentRemark: The last comment made by the opponent
    :param int timeLimit:     The amount of time, in seconds, Diogenes has to calculate and return his next move
    :return: A tuple, where the first value is a tuple consisting of the move and the next state, and the second is
             Diogenes' remark
    """
    global deadline
    deadline = (time.time() + timeLimit) * 1000 - TIME_BUFFER  # Set the time at which processing should end
    currentState = DiogenesState(currentState.board, currentState.whose_move)  # Use the custom BCState subclass
    newRemark = "I believe I have no legal moves."

    newState, move = itrDeep(currentState)

    if move is not None:
        newRemark = "Here is my move."

    return (move, BC_state(newState.board, newState.whose_move)), newRemark


def staticEval(state):
    """
    Static access to a state's eval function

    The actual routines are found in Diogenes_BC_module_eval

    :param state: A state of the game
    :return: A real number score for the state, where positive means good for white, and negative is good for black
    """
    return state.eval()



def itrDeep(currentState):
    """
    Finds the best move from the current state, using iterative deepening

    :param BCState currentState: The current state
    :return: A tuple consisting of the best state and the move required to get there
    """
    depth = 0
    newState = None
    depthBestMoveFound = 0
    move = None
    player = currentState.getPlayer()

    if player == WHITE:
        bestValue = -inf
    else:
        bestValue = inf

    while True:
        bestValueForDepth = None
        bestStateForDepth = None
        bestMoveForDepth = None

        for operator in OPERATORS:
            if operator.is_applicable(currentState):
                for nextState in operator.apply(currentState):
                    value = alphaBeta(nextState, depth)

                    if outOfTime():
                        break

                    # If the move that was thought to be the best is seen again in a different depth, update its value,
                    # since we have more information now
                    if operator.move == move and depthBestMoveFound < depth:
                        bestValue = value

                    if bestValueForDepth is None or (player == WHITE and value > bestValueForDepth) or (player == BLACK and value < bestValueForDepth):
                        bestValueForDepth = value
                        bestStateForDepth = nextState
                        bestMoveForDepth = operator.move
                        depthBestMoveFound = depth

            if outOfTime():
                break

        if outOfTime():
            # If the best move is near the end of the list of moves, the algorithm may have found it in an earlier
            # depth but not in a later depth if it timed out. Only use the value from the current depth if it was
            # definitely better than the one from the last depth.
            if bestValueForDepth is not None and ((player == WHITE and bestValueForDepth > bestValue) or (player == BLACK and bestValueForDepth < bestValue)):
                newState = bestStateForDepth
                move = bestMoveForDepth
                bestValue = bestValueForDepth
            break

        # If all of the moves for this depth were examined, update the best move
        bestValue = bestValueForDepth
        newState = bestStateForDepth
        move = bestMoveForDepth

        depth += 1

    return newState, move


def alphaBeta(currentState, depth, alpha=-inf, beta=inf):
    """
    Runs a search using alpha beta pruning for the best move from the current state
    :param BCState currentState: The current state
    :param int depth:            How many subsequent plies to search
    :param int alpha:            The current worst-case evaluation
    :param int beta:             The current best-case evaluation
    :return: The value of the current state
    """
    global stateValues, stateDepths
    player = currentState.getPlayer()

    if outOfTime():
        if player == WHITE:
            return -inf
        else:
            return inf

    # If the state has already been evaluated, just use the pre-calculated result
    if currentState in stateValues and stateDepths[currentState] >= depth:
        return stateValues[currentState]

    # If this is a leaf node, evaluate this state
    if depth == 0 or len(currentState.findPieces('KING')) < 2:
        bestValue = currentState.eval()
    else:
        if player == WHITE:
            bestValue = alpha
            for nextState, move in currentState.children():
                if outOfTime():
                    break
                bestValue = max(bestValue, alphaBeta(nextState, depth - 1, bestValue, beta))
                if bestValue >= beta:
                    break
        else:
            bestValue = beta
            for nextState, move in currentState.children():
                if outOfTime():
                    break
                bestValue = min(bestValue, alphaBeta(nextState, depth - 1, alpha, bestValue))
                if alpha >= bestValue:
                    break

    if -inf < bestValue < inf and (currentState not in stateDepths or stateDepths[currentState] < depth):
        stateValues[currentState] = bestValue
        stateDepths[currentState] = depth

    return bestValue


def outOfTime():
    """
    Determines whether the time has passed the deadline

    :return: True if the current time has passed the deadline, and False otherwise
    """
    global deadline
    if deadline == 0: return True

    rc = time.time() * 1000 >= deadline
    if rc: deadline = 0
    return rc
