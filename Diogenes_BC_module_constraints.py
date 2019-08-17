"""
Diogenes_BC_module_constraints.py

Contains all of the constraints on moving for the pieces in Baroque Chess. The constraints are found near the end of the
file, and are packaged together in the constant CONSTRAINTS.

:author: Graham Still
"""
from collections import OrderedDict
from Diogenes_BC_module_helpers import *
from Diogenes_BC_module_constants import *


class ConstraintSet:
    """
    Stores a set of functions returning booleans, and checks if those functions have been satisfied
    """
    def __init__(self, constraints):
        """
        Initializes the ConstraintSet

        :param list constraints: A list of None values, or functions returning booleans
        """
        self.constraints = constraints

    def isSatisfied(self, state, start, end):
        """
        Checks if the constraints have been satisfied

        :param BC_state state: The current state
        :param tuple start:    The coordinates for where a piece is starting from
        :param tuple end:      The coordinates for where the piece would end
        :return:               True if all of the constraints return True, and False otherwise
        """
        rc = True

        for constraint in self.constraints:
            if constraint is not None and not constraint(state, start, end):
                rc = False
                break

        return rc


class MovementConstraintSet(ConstraintSet):
    """
    Subclass of ConstraintSet for piece movement which takes a dictionary of constraints, and includes defaults
    """
    def __init__(self, constraints=None):
        """
        Initializes the MovementConstraintSet

        :param dict constraints: Constraints to add to the set. If any constraint has the same key as one in the
                                 default set, the default will be overridden.
        """
        # Initialize the default constraints
        defaultConstraints = OrderedDict([
            # Moves must be in straight lines or diagonals
            ('direction', lambda state, start, end: inLine(start, end) or inDiagonal(start, end)),
            # The destination must be empty
            ('destination', lambda state, start, end: state.squareIsEmpty(end)),
            # There can't be anything in the way
            ('interception', lambda state, start, end: state.piecesBetween(start, end) == 0)
        ])

        # Override the default constraints as necessary
        if constraints is not None:
            for name, constraint in constraints.items():
                defaultConstraints[name] = constraint

        # Save the list of constraints (throw away the keys)
        super().__init__(defaultConstraints.values())


def leaperInterception(state, start, end, piece=None):
    """
    The leaper's interception rule is more complicated than the other pieces, so it is defined here instead of in a
    lambda.
    """
    path = getPath(start, end)
    piecesInPath = state.getPiecesAt(path)
    blocking = len(piecesInPath) - piecesInPath.count(EMPTY)
    rc = blocking == 0

    if blocking == 1:
        rc = state.squareBelongsTo(state.getOpponent(), path[-1])\
             and (piece is None or state.squareIsPiece(piece, path[-1]))

    return rc


def isFrozen(board, position, recurse=True):
    """
    Determines if a piece is being frozen by an enemy freezer or imitator

    :param list board:     The list to access
    :param tuple position: The indices of the piece in question
    :param bool recurse:   Whether or not the function should recurse in case of finding an imitator
    :return:               True if the piece is frozen and False otherwise
    """
    x, y = position
    opponent = (board[x][y] + 1) % 2

    for i in range(x-1, x+2):
        if 0 <= i < DIMENSION:
            for j in range(y-1, y+2):
                if 0 <= j < DIMENSION and not (i, j) == position:
                    target = board[i][j]
                    if target == BLACK_FREEZER + opponent:
                        return True
                    if recurse and target == BLACK_IMITATOR + opponent and isFrozen(board, (i, j), False):
                        return True

    return False


# Constraints that apply to all moves
GENERAL_CONSTRAINTS = ConstraintSet([
    # A piece can't move while staying where it is
    lambda state, start, end: start != end,
    # A piece has to move - not an empty space
    lambda state, start, end: not state.squareIsEmpty(start),
    # The piece has to belong to the current player
    lambda state, start, end: state.squareBelongsTo(state.getPlayer(), start),
    # The piece cannot move if it is next to an enemy freezer
    lambda state, start, end: not isFrozen(state.board, start)
])

# Constraints that apply only to king movement
KING_CONSTRAINTS = MovementConstraintSet({
    # Only adjacent squares (in any direction) are allowed
    'direction': lambda state, start, end: isAdjacent(start, end),
    # The goal can be any square that isn't occupied by one of the king's own pieces
    'destination': lambda state, start, end: not state.squareBelongsTo(state.getPlayer(), end),
    # The direction constraint means that interception is impossible - don't bother checking it
    'interception': None
})

LEAPER_CONSTRAINTS = MovementConstraintSet({
    # The leaper can jump over an enemy right before the end of its move
    'interception': lambda state, start, end: leaperInterception(state, start, end)
})

IMITATOR_CONSTRAINTS = MovementConstraintSet({
    # Normal destination constraints, except an adjacent enemy king can also be captured
    'destination': lambda state, start, end: state.squareIsEmpty(end) or (isAdjacent(start, end)
                        and state.squareIsPiece('KING', end) and not state.squareBelongsTo(state.getPlayer(), end)),
    # The imitator can jump over an enemy leaper right before the end of its move
    'interception': lambda state, start, end: leaperInterception(state, start, end, 'LEAPER')
})

# Constraints that apply only to pincer movement
PINCER_CONSTRAINTS = MovementConstraintSet({
    # Pincers can only travel in straight lines
    'direction': lambda state, start, end: inLine(start, end)
})

# Constraints that apply to everything else
DEFAULT_CONSTRAINTS = MovementConstraintSet()

CONSTRAINTS = {
    'KING':        KING_CONSTRAINTS,
    'PINCER':      PINCER_CONSTRAINTS,
    'LEAPER':      LEAPER_CONSTRAINTS,
    'IMITATOR':    IMITATOR_CONSTRAINTS,
    'WITHDRAWER':  DEFAULT_CONSTRAINTS,
    'COORDINATOR': DEFAULT_CONSTRAINTS,
    'FREEZER':     DEFAULT_CONSTRAINTS,

    'GENERAL':     GENERAL_CONSTRAINTS
}
