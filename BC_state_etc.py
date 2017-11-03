'''BC_state_etc.py
S. Tanimoto, October 30, 2017

This file includes functions to support building agents
that play Baroque Chess.  It should be imported by
Python files that implement move generation,
static evaluation, holding matches between players,
etc.

We use 2 alternative representations of states:
 R1. ASCII, for display and initialization.
 R2. A class BC_state that contains a representation of the
     board consisting of an array (implemented as alist of lists).

 To go from R1 to R2, use function: parse to get a board array,
    and then we construct an instance of BC_state.
 To go from R2 to R1, use function: __repr__ (or cast to str).

Within R1, pieces are represented using initials; e.g., 'c', 'C', 'p', etc.
Within R2, pieces are represented using integers 1 through 14.

We are following these rules:
 
  No leaper double jumps.
      SOME PEOPLE CONSIDER IT DETRIMENTAL TO THE GAME TO ALLOW A LEAPER
      TO MAKE MORE THAN ONE JUMP IN ONE TURN, AND IT INCREASES THE
      BRANCHING FACTOR IN THE GAME TREE, WHICH IS ALREADY LARGE.

  No altering the initial symmetries of the board, although Wikipedia suggests this is allowed.

  No "suicide" moves allowed.

  Pincers can pinch using any friendly piece as their partners, not just other pincers.

  An imitator can imitate at most one piece during a move.
 
'''
BLACK = 0
WHITE = 1
NORTH = 0; SOUTH = 1; WEST = 2; EAST = 3; NW = 4; NE = 5; SW = 6; SE = 7

# Used in parsing the initial state and in testing:

INIT_TO_CODE = {'p':2, 'P':3, 'c':4, 'C':5, 'l':6, 'L':7, 'i':8, 'I':9,
  'w':10, 'W':11, 'k':12, 'K':13, 'f':14, 'F':15, '-':0}

# Used in printing out states:

CODE_TO_INIT = {0:'-',2:'p',3:'P',4:'c',5:'C',6:'l',7:'L',8:'i',9:'I',
  10:'w',11:'W',12:'k',13:'K',14:'f',15:'F'}

# Global variables representing the various types of pieces on the board:

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


def who(piece): return piece % 2  # BLACK's pieces are even; WHITE's are odd.

def parse(bs): # bs is board string
  '''Translate a board string into the list of lists representation.'''
  b = [[0,0,0,0,0,0,0,0] for r in range(8)]
  rs9 = bs.split("\n")
  rs8 = rs9[1:] # eliminate the empty first item.
  for iy in range(8):
    rss = rs8[iy].split(' ');
    for jx in range(8):
      b[iy][jx] = INIT_TO_CODE[rss[jx]]
  return b

INITIAL = parse('''
c l i w k i l f
p p p p p p p p
- - - - - - - -
- - - - - - - -
- - - - - - - -
- - - - - - - -
P P P P P P P P
F L I W K I L C
''')

class BC_state:
    def __init__(self, old_board=INITIAL, whose_move=WHITE):
        new_board = [r[:] for r in old_board]  # Deeply copy the board.
        self.board = new_board
        self.whose_move = whose_move;

    def __repr__(self): # Produce an ASCII display of the state.
        s = ''
        for r in range(8):
            for c in range(8):
                s += CODE_TO_INIT[self.board[r][c]] + " "
            s += "\n"
        if self.whose_move==WHITE: s += "WHITE's move"
        else: s += "BLACK's move"
        s += "\n"
        return s

    def __eq__(self, other):
      if not (type(other)==type(self)): return False
      if self.whose_move != other.whose_move: return False
      try:
        b1 = self.board
        b2 = other.board
        for i in range(8):
          for j in range(8):
            if b1[i][j] != b2[i][j]: return False
        return True
      except Exception as e:
        return False
      
def test_starting_board():
  init_state = BC_state(INITIAL, WHITE)
  print(init_state)


if __name__ == "__main__":
  test_starting_board()
