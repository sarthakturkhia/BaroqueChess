"""
Diogenes_BC_module_capture.py

Contains a series of functions corresponding to how pieces capture. Each function must adhere to the following
interface: it must accept a state, a start tuple, and an end tuple as arguments, and it must return a list of tuple
lists, where each tuple corresponds to a position that would be captured by the move. The state that is accepted is
the STARTING state, not the end state; this is to enable the imitator's function to see if the king was taken. The
functions are packaged together into a constant dict at the bottom of the file, called CAPTURES.

:author: Graham Still
"""
from Diogenes_BC_module_constants import DIMENSION
from Diogenes_BC_module_helpers import getSlope


def pincer(state, start, end):
    """
    The pincer captures by pinning an opposing piece between itself and a friendly non-pincer.
    """
    x, y = end
    captures = []

    for i in range(-1, 2):
        captureX = x + i
        allyX = x + (i * 2)
        if 0 <= allyX < DIMENSION:
            for j in range(-1, 2):
                captureY = y + j
                allyY = y + (j * 2)
                if 0 <= allyY < DIMENSION:

                    # If the ally is on the board, then the capture square must also be.
                    # If the ally is on the same team as the pincer and is not a pincer itself,
                    # and the capture square is occupied by an enemy, remove that enemy.
                    if state.squareBelongsTo(state.getPlayer(), allyX, allyY)\
                            and state.squareBelongsTo(state.getOpponent(), captureX, captureY)\
                            and not state.squareIsPiece('PINCER', allyX, allyY):
                        captures.append((captureX, captureY))

    return [captures]


def coordinator(state, start, end):
    """
    The coordinator captures enemy pieces that are in the corners that make up the square between the coordinator and
    its friendly king.
    """
    player = state.getPlayer()
    opponent = state.getOpponent()
    captures = []

    # Find the coordinates of the corresponding king
    kingPosition = state.findPieces('KING', player)
    if len(kingPosition) == 0:
        # If the king is missing, the coordinator cannot capture
        return [[]]

    coordX, coordY = end
    kingX, kingY = kingPosition[0]

    # Remove any opponents that occupy the square the king and coordinator's positions form
    if state.squareBelongsTo(opponent, coordX, kingY):
        captures.append((coordX, kingY))
    if state.squareBelongsTo(opponent, kingX, coordY):
        captures.append((kingX, coordY))

    return [captures]


def withdrawer(state, start, end):
    """
    The withdrawer captures an opposing piece that it moved directly away from
    """
    x, y = start
    rise, run = getSlope(start, end)
    captures = []

    # Get the coordinates of the previous square
    x -= rise
    y -= run

    # If the square is on the board and occupied by an enemy, get rid of it
    if 0 <= x < DIMENSION and 0 <= y < DIMENSION and state.squareBelongsTo(state.getOpponent(), x, y):
        captures.append((x, y))

    return [captures]


def leaper(state, start, end):
    """
    The leaper captures the piece it jumped over, if any. The piece must have been directly before the end space for
    it to have been able to jump at all.
    """
    x, y = end
    rise, run = getSlope(start, end)
    captures = []

    # Get the coordinates of the previous square
    x -= rise
    y -= run

    # If the square is occupied by an enemy, get rid of it
    if state.squareBelongsTo(state.getOpponent(), x, y):
        captures.append((x, y))

    return [captures]


def imitator(state, start, end):
    """
    The imitator captures an opposing piece if the opposing piece would have captured had the imitator been it. The
    imitator is only allowed to imitate one piece per move, so it may return multiple lists of captures.
    """
    captures = []

    # If the end position wasn't empty, it means that the imitator moved like a king, and has therefore already
    # captured
    if state.squareIsEmpty(end):
        # If there are possible leaper captures, it means that the imitator moved like a leaper, and is therefore only
        # allowed to capture like a leaper.
        leaperCaptures = CAPTURES['LEAPER'](state, start, end)

        if len(leaperCaptures[0]) > 0:
            captures = leaperCaptures
        else:
            for pieceName, func in CAPTURES.items():
                # Don't let the imitator check to see if an imitator could capture
                if pieceName == 'IMITATOR' or pieceName == 'LEAPER':
                    continue

                currCaptures = []
                for position in func(state, start, end)[0]:
                    # If the piece that would get captured moves in the way the capture would be done,
                    # add it to the list
                    if state.squareIsPiece(pieceName, position):
                        currCaptures.append(position)

                if len(currCaptures) > 0:
                    captures.append(currCaptures)

    return captures


CAPTURES = {
    'PINCER':      pincer,
    'COORDINATOR': coordinator,
    'WITHDRAWER':  withdrawer,
    'LEAPER':      leaper,
    'IMITATOR':    imitator
}
