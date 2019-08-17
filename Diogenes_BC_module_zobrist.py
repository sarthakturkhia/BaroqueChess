"""
Diogenes_BC_module_zobrist.py

Contains the Zobrist class, which implements Zobrist hashing on a two dimensional list

:author: Jaskeerat Sethi and Graham Still
"""
from random import randint


class Zobrist:
    def __init__(self, w, h, p, conversion):
        """
        Initializes the hasher

        :param int w: The width of the boards to be hashed
        :param int h: The height of the boards to be hashed
        :param in p:  The number of pieces
        :param func conversion: A function to map values in the board to array indices
        """
        self.conversion = conversion
        self.h = h
        self.w = w
        self.numbers = [[[0]*p for i in range(h)] for j in range(w)]

        for i in range(w):
            for j in range(h):
                for k in range(p):
                    self.numbers[i][j][k] = randint(0, 4294967296)

    def hash(self, board):
        """
        Hashes a board

        :param list board: The board to hash
        :return:           An int hash key
        """
        val = 0
        for i in range(self.h):
            for j in range(self.w):
                piece = self.conversion(board[i][j])

                if piece >= 0:
                    val ^= self.numbers[i][j][piece]
        return val
