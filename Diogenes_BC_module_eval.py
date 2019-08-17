"""
Diogenes_BC_module_eval.py

Contains the code for evaluating a state. The actual evaluation function is evaluate(); all other methods are called by
it to generate the evaluation.

:author: Graham Still
"""
from Diogenes_BC_module_constants import *
from Diogenes_BC_module_helpers import ratioToOutside, ratioToInside


def evaluate(state):
    """
    Assigns a float score to a state, based on the board

    The score consists of the value of each piece on the board and the distance of each piece from the center..

    :param DiogenesState state: The state to examine
    :return: A float indicating a value for the state
    """
    value, blackPieces, whitePieces = evalPieces(state)
    value += evalPositions(state, whitePieces, blackPieces)

    return value


def evalPieces(state):
    """
    Assigns a score to a state based on the number of pieces present

    :param DiogenesState state: The state to examine
    :return: A tuple consisting of the value of the pieces on the board, the number of black pieces, and the number of
             white pieces
    """
    value = 0
    blackPieces = 0
    whitePieces = 0

    for x in range(DIMENSION):
        for y in range(DIMENSION):
            piece = state.access(x, y)

            if piece > 0:
                val = evalPiece(piece)
                if piece % 2 == 1:
                    value += val
                    whitePieces += 1
                else:
                    value -= val
                    blackPieces += 1

    return value, blackPieces, whitePieces


def evalPiece(code):
    """
    Gives a value for a piece

    :param int code:  The code for the piece
    :return:          The value assigned to the piece
    """
    if code == WHITE_PINCER or code == BLACK_PINCER:
        return VALUES['PINCER']
    if code == WHITE_KING or code == BLACK_KING:
        return VALUES['KING']
    return VALUES['OTHER']


def evalPositions(state, blackPieces, whitePieces):
    """
    Assigns a score to a state based on the distance from each piece to the center

    :param DiogenesState state: The state to examine
    :param int blackPieces:     The number of black pieces on the board
    :param int whitePieces:     The number of white pieces on the board
    :return: A score for the positions of the pieces on the board
    """
    value = 0

    for x in range(DIMENSION):
        for y in range(DIMENSION):
            piece = state.access(x, y)

            if piece > 0:
                val = evalPosition(piece, x, y, whitePieces, blackPieces)
                if piece % 2 == 1:
                    value += val
                else:
                    value -= val

    return value


def evalPosition(piece, x, y, whitePieces, blackPieces):
    """
    Gives a value from 0 to 1 based on two coordinates

    For all pieces except for the king, the value is greater the closer the coordinates are to the center. The value is
    greater if the king is closer to the center only if the opponent has a small number of pieces (i.e. it is an end-
    game scenario); otherwise, the value is greater for the king if it is closer to the edge.

    :param int x: The x coordinate
    :param int y: The y coordinate
    :return:      The value assigned to the coordinates
    """
    if (piece == WHITE_KING and not blackPieces > END_GAME_NUM) or (piece == BLACK_KING and not whitePieces > END_GAME_NUM):
        return ratioToOutside(x, y)
    else:
        return ratioToInside(x, y)
