"""
Diogenes_BC_module_state.py

Contains an extension of the BC_state found in BC_state_etc to allow the state to be interacted with in an object
oriented way.

:author: Graham Still
"""
from BC_state_etc import BC_state, INITIAL
from Diogenes_BC_module_constants import *
from Diogenes_BC_module_helpers import getPath, ratioToOutside, ratioToInside
from Diogenes_BC_module_constraints import CONSTRAINTS
from Diogenes_BC_module_capture import CAPTURES
from Diogenes_BC_module_zobrist import Zobrist as Hasher
from Diogenes_BC_module_operator import OPERATORS
from Diogenes_BC_module_eval import evaluate

hasher = Hasher(DIMENSION, DIMENSION, NUM_PIECES, lambda n: n - 2)
childCache = {}


class DiogenesState(BC_state):
    def __init__(self, old_board=INITIAL, whose_move=WHITE):
        self.hash = None
        super().__init__(old_board, whose_move)

    def __hash__(self):
        """
        Diogenes uses zobrist hashing, which is relatively computationally expensive. When a hash is required, cache
        the hash value so that it only needs to be done once. This cache will be dumped if the board is ever changed
        (by using alter()).
        """
        if self.hash is None:
            self.hash = hasher.hash(self.board)
        return self.hash

    def access(self, x, y=None):
        """
        Accesses the board using either a pair of coordinates or a tuple

        :param x: The x coordinate, or a tuple of coordinates
        :param y: The y coordinate, or None if x is a tuple
        :return:  The value of whatever exists at that position on the board
        """
        if y is None:
            return self.board[x[0]][x[1]]
        else:
            return self.board[x][y]

    def alter(self, x, y, val=None):
        """
        Modifies the board using either a pair of coordinates or a tuple

        :param x:   The x coordinate, or a tuple of coordinates
        :param y:   The y coordinate, or the value to store if x is a tuple
        :param val: The value to store at the coordinates, or None if x is a tuple
        """
        self.hash = None  # If there was a previously cached hash, it is now invalid

        if val is None:
            self.board[x[0]][x[1]] = y
        else:
            self.board[x][y] = val

    def nextMove(self):
        """
        Advances the move counter
        """
        self.whose_move = 1 - self.whose_move

    def clone(self):
        """
        :return: A deep copy of the state
        """
        return DiogenesState(self.board, self.whose_move)

    def canMove(self, start, end):
        """
        Determines if a move from one coordinate to another is a legal move

        :param tuple start: The starting coordinate
        :param tuple end:   The end coordinate
        :return:            True if it is legal to move from the start position to the end position, and false otherwise
        """
        rc = False

        # Make sure the constraints that apply to all pieces are satisfied before moving on to the more specific ones
        if CONSTRAINTS['GENERAL'].isSatisfied(self, start, end):

            # Check if the constraints on the specific piece are satisfied
            for piece, constraint in CONSTRAINTS.items():
                if self.squareIsPiece(piece, start):
                    rc = constraint.isSatisfied(self, start, end)
                    break

        return rc

    def move(self, start, end):
        """
        Transforms the state by moving whatever is at the start coordinate to the end coordinate, and replacing the
        original start coordinate with an empty space. Removes any pieces that are caught by the moved piece's capture
        routine. Because the imitator can only mimick one piece at a time, this function returns a list of states,
        instead of just one.

        :param tuple start: The starting coordinate
        :param tuple end:   The end coordinate
        :return:            A list of transformed BC_states
        """
        outputStates = []
        newState = self.clone()

        # Make the move
        newState.alter(start, EMPTY)
        newState.alter(end, self.access(start))
        newState.nextMove()

        # Execute the appropriate capture routine
        for piece, captureRoutine in CAPTURES.items():
            if self.squareIsPiece(piece, start):
                captureSet = captureRoutine(self, start, end)

                if len(captureSet) > 0:
                    for captures in captureSet:
                        captureState = newState.clone()
                        for position in captures:
                            captureState.alter(position, EMPTY)
                        outputStates.append(captureState)
                break

        if len(outputStates) == 0:
            outputStates.append(newState)

        return outputStates

    def eval(self):
        return evaluate(self)

    def children(self):
        global childCache
        if self in childCache:
            return childCache[self]

        children = []
        for operator in OPERATORS:
            if operator.is_applicable(self):
                for nextState in operator.apply(self):
                    children.append((nextState, operator.move))

        childCache[self] = children
        return children

    def getPlayer(self):
        """
        :return: The code for the player whose turn it is
        """
        return self.whose_move % 2

    def getOpponent(self):
        """
        :return: The code for the player whose turn it is not
        """
        return (self.whose_move + 1) % 2

    def squareIsEmpty(self, x, y=None):
        """
        Determines if a set of coordinates correspond to the empty symbol on the board

        :param x: The x coordinate, or a tuple of coordinates
        :param y: The y coordinate, or None if x is a tuple
        :return:  True if the square is empty, and False otherwise
        """
        return self.access(x, y) == EMPTY

    def squareIsPiece(self, piece, x, y=None):
        """
        Determines if a code corresponds to a particular type of piece, regardless of owner

        :param str piece: The name of the piece to check
        :param x:         The x coordinate, or a tuple of coordinates
        :param y:         The y coordinate, or None if x is a tuple
        :return:          True if the code matches the piece name, and False otherwise
        """
        square = self.access(x, y)

        return globals().get('BLACK_' + piece) == square or globals().get('WHITE_' + piece) == square

    def squareBelongsTo(self, player, x, y=None):
        """
        Determines if a square is occupied by a given player

        :param player: Either a string giving the name of the player's pieces, or an int giving the player's code
        :param x:      The x coordinate, or a tuple of coordinates
        :param y:      The y coordinate, or None if x is a tuple
        :return:       True if the square belongs to the player, and False otherwise
        """
        if isinstance(player, str):
            player = globals()[player]

        square = self.access(x, y)

        return square > EMPTY and square % 2 == player

    def getPiecesAt(self, coordinates):
        """
        Retrieves the pieces from a list of coordinates

        :param coordinates: The coordinates to access
        :return:            A list of the pieces (or empty spaces) at the coordinates
        """
        pieces = []

        for coordinate in coordinates:
            pieces.append(self.access(coordinate))

        return pieces

    def findPieces(self, piece, player=None):
        """
        Finds all of the pieces of a given type, optionally of a given player

        :param str piece: The name of the piece to look for
        :param player:    The code for the player to restrict the search to, or None if not required
        :return:          A list of tuples corresponding to the coordinates of the matching pieces
        """
        pieces = []

        for x in range(DIMENSION):
            for y in range(DIMENSION):
                if self.squareIsPiece(piece, x, y) and (player is None or self.squareBelongsTo(player, x, y)):
                    pieces.append((x, y))

        return pieces

    def piecesBetween(self, pos1, pos2):
        """
        Counts the number of pieces between the coordinates

        :param tuple pos1: The first coordinate
        :param tuple pos2: The second coordinate
        :return:           The number of pieces between the two positions
        """
        positions = getPath(pos1, pos2)
        squares = self.getPiecesAt(positions)

        return len(squares) - squares.count(EMPTY)
