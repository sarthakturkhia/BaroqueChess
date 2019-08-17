"""
Diogenes_BC_module_operator.py

Contains all of the possible moves in a game of Baroque Chess

:author: Graham Still and Steve Tanimoto
"""
from Diogenes_BC_module_constants import DIMENSION


class Operator:
    """ Adapted from TowersOfHanoi.py by S. Tanimoto """
    def __init__(self, name, move, precond, state_transf):
        self.name = name
        self.move = move
        self.precond = precond
        self.state_transf = state_transf

    def is_applicable(self, s):
        return self.precond(s)

    def apply(self, s):
        return self.state_transf(s)

POSITIONS = [(x, y) for x in range(DIMENSION) for y in range(DIMENSION)]
OPERATORS = [Operator(
    "Move from " + str(start_position) + " to " + str(end_position) + ".",
    (start_position, end_position),
    lambda state, start=start_position, end=end_position: state.canMove(start, end),
    lambda state, start=start_position, end=end_position: state.move(start, end)
) for start_position in POSITIONS for end_position in POSITIONS]
