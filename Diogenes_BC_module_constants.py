"""
Diogenes_BC_module_constants.py

Unchanging values used by the Diogenes program
"""
DIMENSION = 8  # The length and width of the board

# Player codes
BLACK = 0
WHITE = 1

EMPTY = 0  # The code for an empty square

# Piece codes
BLACK_PINCER      = 2
BLACK_COORDINATOR = 4
BLACK_LEAPER      = 6
BLACK_IMITATOR    = 8
BLACK_WITHDRAWER  = 10
BLACK_KING        = 12
BLACK_FREEZER     = 14

WHITE_PINCER      = 3
WHITE_COORDINATOR = 5
WHITE_LEAPER      = 7
WHITE_IMITATOR    = 9
WHITE_WITHDRAWER  = 11
WHITE_KING        = 13
WHITE_FREEZER     = 15

# The values given to each piece
VALUES = {'KING': 1000000, 'PINCER': 2, 'OTHER': 4}

NUM_PIECES = 14  # the number of piece types
END_GAME_NUM = 5  # Below this number, a player is considered to be in the end game

# The time, in milliseconds, required to get out of the search and return a move
# Required buffer may vary depending on the processing power of the machine
TIME_BUFFER = 100
