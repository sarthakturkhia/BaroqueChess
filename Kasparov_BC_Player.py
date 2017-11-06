'''Kasaparov_BC_Player.py
The beginnings of an agent that might someday play Baroque Chess.

'''

import BC_state_etc as BC

#for reference
BLACK = 0
WHITE = 1

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

def makeMove(currentState, currentRemark, timelimit):
    # Compute the new state for a move.
    # This is a placeholder that just copies the current state.
    newState = BC.BC_state(currentState.board)

    # Fix up whose turn it will be.
    newState.whose_move = 1 - currentState.whose_move

    # Construct a representation of the move that goes from the
    # currentState to the newState.
    # Here is a placeholder in the right format but with made-up
    # numbers:
    move = ((6, 4), (3, 4))

    # Make up a new remark
    newRemark = "I'll think harder in some future game. Here's my move"

    return [[move, newState], newRemark]

# takes a move and returns a new state of the complete board after the move was made
def getState(move):


#If our king is on check this method makes the moves to protect the king.
def ifonCheck():

# IF our piece is already checking the opponents king then try to finish the game.
def ifattacking():

# These functions should take a position as a parameter and return a list of all possible positions of that piece
def king():

def pincer():

def Knight():

def imitator(loc, currentState):
    moves = []
    if checkFreezer(loc, currentState): return moves
    
    color = currentState[loc[0]][loc[1]] % 2
    opponCol = 1 - color #opponent's color

    passLeap = False

    #check west
    for i in range(7):
        x = loc[0] - (1+i)
        y = loc[1]
        if x >= 0:
            if currentState[x][y] == 6 + opponCol & ~passLeap: #opposing leaper
                passLeap = True
            elif currentState[x][y] != 0: #non-empty space, not leaper
                break;
            else:
                moves.append((x,y))
        else:
            break;
    passLeap = False

    #check east
    for i in range(7):
        x = loc[0] + (1+i)
        y = loc[1]
        if x <= 7:
            if currentState[x][y] == 6 + opponCol & ~passLeap: #opposing leaper
                passLeap = True
            elif currentState[x][y] != 0: #non-empty space, not leaper
                break;
            else:
                moves.append((x,y))
        else:
            break;
    passLeap = False

    #check south
    for i in range(7):
        x = loc[0] 
        y = loc[1] + (1+i)
        if y <= 7:
            if currentState[x][y] == 6 + opponCol & ~passLeap: #opposing leaper
                passLeap = True
            elif currentState[x][y] != 0: #non-empty space, not leaper
                break;
            else:
                moves.append((x,y))
        else:
            break;
    passLeap = False

    #check north
    for i in range(7):
        x = loc[0] 
        y = loc[1] - (1+i)
        if y >= 0:
            if currentState[x][y] == 6 + opponCol & ~passLeap: #opposing leaper
                passLeap = True
            elif currentState[x][y] != 0: #non-empty space, not leaper
                break;
            else:
                moves.append((x,y))
        else:
            break;
    passLeap = False

    #check southwest
    for i in range(7):
        x = loc[0] - (1+i)
        y = loc[1] + (1+i)
        if x >= 0 & if y <= 7:
            if currentState[x][y] == 6 + opponCol & ~passLeap: #opposing leaper
                passLeap = True
            elif currentState[x][y] != 0: #non-empty space, not leaper
                break;
            else:
                moves.append((x,y))
        else:
            break;
    passLeap = False

    #check northwest
    for i in range(7):
        x = loc[0] - (1+i)
        y = loc[1] - (1+i)
        if x >= 0 & if y >= 0:
            if currentState[x][y] == 6 + opponCol & ~passLeap: #opposing leaper
                passLeap = True
            elif currentState[x][y] != 0: #non-empty space, not leaper
                break;
            else:
                moves.append((x,y))
        else:
            break;
    passLeap = False

    #check northeast
    for i in range(7):
        x = loc[0] + (1+i)
        y = loc[1] - (1+i)
        if x <= 7 & if y >= 0:
            if currentState[x][y] == 6 + opponCol & ~passLeap: #opposing leaper
                passLeap = True
            elif currentState[x][y] != 0: #non-empty space, not leaper
                break;
            else:
                moves.append((x,y))
        else:
            break;
    passLeap = False

    #check southeast
    for i in range(7):
        x = loc[0] + (1+i)
        y = loc[1] + (1+i)
        if x <= 7 & if y <= 7:
            if currentState[x][y] == 6 + opponCol & ~passLeap: #opposing leaper
                passLeap = True
            elif currentState[x][y] != 0: #non-empty space, not leaper
                break;
            else:
                moves.append((x,y))
        else:
            break;
    
    return moves

def other():

#returns true if there is an opponent's freezer in any of the 8 directions, else returns false
def checkFreezer(loc, currentState):
    color = currentState[loc[0]][loc[1]] % 2
    opponCol = 1 - color #opponent's color
    if loc[0] > 0:
        if currentState[loc[0]-1][loc[1]] == 14 + opponCol:
            return True
        if loc [1] > 0 and currentState[loc[0]-1][loc[1]-1] == 14 + opponCol:
            return True
        if loc [1] < 7 and currentState[loc[0]-1][loc[1]+1] == 14 + opponCol:
            return True
    if loc[0] < 7
        if currentState[loc[0]+1][loc[1]] == 14 + opponCol:
            return True
        if loc [1] > 0 and currentState[loc[0]+1][loc[1]-1] == 14 + opponCol:
            return True
        if loc [1] < 7 and currentState[loc[0]+1][loc[1]+1] == 14 + opponCol:
            return True
    if loc [1] > 0 and currentState[loc[0]][loc[1]-1] == 14 + opponCol:
        return True
    if loc [1] < 7 and currentState[loc[0]][loc[1]+1] == 14 + opponCol:
        return True

    return False

def nickname():
    return "Kasper"


def introduce():
    return "I'm Kasparov a Russian Baroque Chess agent."


def prepare(player2Nickname):
    pass

# Mathematical sum of all the pieces we have based on a point system. + the position index in comparision to opponents
# pieces and our pieces in the kings diagonals, verticals and horizontals. subtract the same for our opponent from this sum.
def staticEval(state):
    return 0

