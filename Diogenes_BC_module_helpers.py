"""
Diogenes_BC_module_helpers.py

Contains a collection of helper methods for basic linear algebra comparisons, like checking if coordinates are next
to each other.

:author: Graham Still
"""
from Diogenes_BC_module_constants import DIMENSION


def inLine(pos1, pos2):
    """
    Determines if two positions are in a straight (not diagonal) line with each other

    :param tuple pos1: The first coordinate
    :param tuple pos2: The second coordinate
    :return:           True if the two positions are in line with each other, and False otherwise
    """
    x1, y1 = pos1
    x2, y2 = pos2

    return x1 == x2 or y1 == y2


def inDiagonal(pos1, pos2):
    """
    Determines if two positions are in a diagonal line with each other

    :param tuple pos1: The first coordinate
    :param tuple pos2: The second coordinate
    :return:           True if the two positions are in a diagonal with each other, and False otherwise
    """
    x1, y1 = pos1
    x2, y2 = pos2

    return abs(x1 - x2) == abs(y1 - y2)


def isAdjacent(pos1, pos2):
    """
    Determines if two positions are next two each other (including diagonals)

    :param tuple pos1: The first coordinate
    :param tuple pos2: The second coordinate
    :return:           True if the two positions are next to each other, and False otherwise
    """
    x1, y1 = pos1
    x2, y2 = pos2

    return max(abs(x1 - x2), abs(y1 - y2)) == 1


def getPath(start, end):
    """
    Retrieves the positions between the start and end position

    :param tuple start: The starting coordinate
    :param tuple end:   The ending coordinate
    :return:            A list of positions that a piece would have to cross to get from the start to the end
    """
    x, y = start
    rise, run = getSlope(start, end)
    path = []

    x += rise
    y += run

    while not (x, y) == end:
        path.append((x, y))
        x += rise
        y += run

    return path


def getSlope(start, end):
    """
    Calculates the direction the line between two points is going

    :param tuple start: The starting coordinate
    :param tuple end:   The end coordinate
    :return:            A tuple of integers, where the first is what needs to be added to the start in the x direction
                        to get to the end, and the second is what needs to be added to the start in the y direction to
                        get to the end
    """
    x1, y1 = start
    x2, y2 = end

    rise = x2 - x1
    run = y2 - y1
    if rise != 0:
        rise = int(rise / abs(rise))
    if run != 0:
        run = int(run / abs(run))

    return rise, run


def ratioToOutside(x, y=None):
    if y is None:
        x, y = x

    return ratioToEnd(x) * ratioToEnd(y)


def ratioToInside(x, y=None):
    if y is None:
        x, y = x

    return ratioToCenter(x) * ratioToCenter(y)


def ratioToEnd(x):
    halfDimension = (DIMENSION - 1) / 2
    return abs((x - halfDimension) / halfDimension)


def ratioToCenter(x):
    return abs(1 - ratioToEnd(x))
