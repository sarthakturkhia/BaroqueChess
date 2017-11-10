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
def getState(move, state):
    resultstate = state
    intlLoc = move[0]
    goalLoc = move[1]
    piece = state[intlLoc[1]][intlLoc[0]]
    # assumes the initial location won't be 0 in state
    color = state[intlLoc[1]][intlLoc[0]] % 2
    opoColor = 1 - color
    # pincer
    if piece - color ==  2:
        if len(kingHelper(goalLoc, state, opoColor)) != 0:
            # +x east
            x = min(goalLoc[0] + 1, 7)
            if state[goalLoc[1]][x] % 2 != color:
                x1 = state[goalLoc[1]][min(x + 1, 7)]
                if x1 % 2 == color and x1 != 0:
                    resultstate[goalLoc[1]][x] = 0
            # -x west
            x = max(goalLoc[0] - 1, 0)
            if state[goalLoc[1]][x] % 2 != color:
                x1 = state[goalLoc[1]][max(x - 1, 0)]
                if x1 % 2 == color and x1 != 0:
                    resultstate[goalLoc[1]][x] = 0
            # +y north
            x = min(goalLoc[1] + 1, 7)
            if state[x][goalLoc[0]] % 2 == opoColor:
                x1 = state[min(x + 1, 7)][goalLoc[0]]
                if x1 % 2 == color and x1 != 0:
                    resultstate[x][goalLoc[0]] = 0
            # -y south
            x = max(goalLoc[0] - 1, 0)
            if state[x][goalLoc[0]] % 2 != color:
                x1 = state[max(x - 1, 0)][goalLoc[1]]
                if x1 % 2 == color and x1 != 0:
                    resultstate[x][goalLoc[0]] = 0
    # Leaper
    elif piece - color ==  6:
        diffX = goalLoc[0] - intlLoc[0]
        diffY = goalLoc[1] - intlLoc[1]
        x = diffX/abs(diffX)
        y = diffY/abs(diffY)
        for i in range(abs(diffX)):
            resultstate[intlLoc[1]+(i*y)][intlLoc[0]+(i*x)] = 0
    # coordinator
    elif piece - color == 4:
        kingsLoc = [-1, -1]
        for i in range(8):
            for j in range(8):
                if state[j][i] == 12 + color:
                    kingsLoc = [j,i]
                    break
            if kingsLoc[0] != -1:
                break

        if state[goalLoc[1]][kingsLoc[0]] % 2 == opoColor:
            resultstate[goalLoc[1]][kingsLoc[0]] = 0

        if state[kingsLoc[1]][goalLoc[0]] % 2 == opoColor:
            resultstate[kingsLoc[1]][goalLoc[0]] = 0

    elif piece - color == 8:
        # knight
        resultstate[intlLoc[1]][intlLoc[0]] = 6 + color
        resultstate = getState(move, resultstate)
        # cordinator
        resultstate[intlLoc[1]][intlLoc[0]] = 4 + color
        resultstate = getState(move, resultstate)
        # pincer
        resultstate[intlLoc[1]][intlLoc[0]] = 2 + color
        resultstate = getState(move, resultstate)
        # withdrawer
        resultstate[intlLoc[1]][intlLoc[0]] = 10 + color
        resultstate = getState(move, resultstate)

    resultstate[intlLoc[1]][intlLoc[0]] = 0
    resultstate[goalLoc[1]][goalLoc[0]] = piece
    return resultstate


# These functions should take a position as a parameter and return a list of all possible positions of that piece
def king(loc, currentState):
    result = []
    color = currentState[loc[1]][loc[0]] % 2
    opponCol = 1 - color  # opponent's color
    if checkFreezer(loc, currentState):
        return result
    else:
        x = [min(loc[0] + 1, 7), loc[1]]
        if currentState[x[1]][x[0]] == 0 or currentState[x[1]][x[0]] % 2 == opponCol:
            result.append(x)
        x = [min(loc[0] + 1, 7), min(loc[1] + 1, 7)]
        if currentState[x[1]][x[0]] == 0 or currentState[x[1]][x[0]] % 2 == opponCol:
            result.append(x)
        x = [min(loc[0] + 1, 7), max(loc[1] - 1, 0)]
        if currentState[x[1]][x[0]] == 0 or currentState[x[1]][x[0]] % 2 == opponCol:
            result.append(x)
        x = [max(loc[0] - 1, 0), max(loc[1] - 1, 0)]
        if currentState[x[1]][x[0]] == 0 or currentState[x[1]][x[0]] % 2 == opponCol:
            result.append(x)
        x = [max(loc[0] - 1, 0), min(loc[1] + 1, 7)]
        if currentState[x[1]][x[0]] == 0 or currentState[x[1]][x[0]] % 2 == opponCol:
            result.append(x)
        x = [max(loc[0] - 1, 0), loc[1]]
        if currentState[x[1]][x[0]] == 0 or currentState[x[1]][x[0]] % 2 == opponCol:
            result.append(x)
        x = [loc[0], min(loc[1] + 1, 7)]
        if currentState[x[1]][x[0]] == 0 or currentState[x[1]][x[0]] % 2 == opponCol:
            result.append(x)
        x = [loc[0], max(loc[1] - 1, 0)]
        if currentState[x[1]][x[0]] == 0 or currentState[x[1]][x[0]] % 2 == opponCol:
            result.append(x)
        return result

# returns a list of opposition pieces around a loc
def kingHelper(x, currentState, opoCol):
    result = []
    y1 = min(x[1] + 1, 7)
    x1 = min(x[0] + 1, 7)
    y2 = max(x[1] - 1, 0)
    x2 = max(x[0] - 1, 0)
    if currentState[y1][x1] % 2 == opoCol and currentState[y1][x1] != 0:
        result.append(currentState[y1][x1])
    if currentState[y2][x1] % 2 == opoCol and currentState[y1][x1] != 0:
        result.append(currentState[y2][x1])
    if currentState[y1][x2] % 2 == opoCol and currentState[y1][x1] != 0:
        result.append(currentState[y1][x2])
    if currentState[y2][x2] % 2 == opoCol and currentState[y1][x1] != 0:
        result.append(currentState[y2][x2])
    if currentState[y1][x[0]] % 2 == opoCol and currentState[y1][x1] != 0:
        result.append(currentState[y1][x[0]])
    if currentState[y2][x[0]] % 2 == opoCol and currentState[y1][x1] != 0:
        result.append(currentState[y2][x[0]])
    if currentState[x[1]][x1] % 2 == opoCol and currentState[y1][x1] != 0:
        result.append(currentState[x[1]][x1])
    if currentState[x[1]][x2] % 2 == opoCol and currentState[y1][x1] != 0:
        result.append(currentState[x[1]][x2])
    return result

def pincer(loc, currentState):
    result = []
    if checkFreezer(loc, currentState):
        return result
    else:
        # +x direction
        for i in range(1,7):
            x = min(loc[0] + i, 7)
            box1 = currentState[loc[1]][x]
            if box1 != 0 : break
            else : result.append([x, loc[1]])
            if x == 7 : break
        # -x direction
        for i in range(1,7):
            x = max(loc[0] - i, 0)
            box2 = currentState[loc[1]][x]
            if box2 != 0 : break
            else : result.append([x, loc[1]])
            if x == 0 : break
        # +y direction
        for i in range(1,7):
            y = min(loc[1] + i, 7)
            box3 = currentState[y][loc[0]]
            if box3 != 0 : break
            else:result.append([loc[0], y])
            if y == 7 : break
        # -y direction
        for i in range(1,7):
            y = max(loc[1] - i, 0)
            box4 = currentState[y][loc[0]]
            if box4 != 0 : break
            else : result.append([loc[0], y])
            if y == 0 : break
        return result

# The leaper
def knight(loc, currentState):
    moves = []
    if checkFreezer(loc, currentState):
        return moves
    color = currentState[loc[1]][loc[0]] % 2
    found = False
    # check west
    for i in range(7):
        x = loc[0] - (1 + i)
        y = loc[1]
        if x >= 0:
            if currentState[y][x] != 0:  # non-empty space
                if currentState[y][x] % 2 == color: break
                elif not found: found = True
                else: break
            else:
                moves.append((x, y))
        else:
            break

    found = False
    # check east
    for i in range(7):
        x = loc[0] + (1 + i)
        y = loc[1]
        if x <= 7:
            if currentState[y][x] != 0:  # non-empty space
                if currentState[y][x] % 2 == color: break
                elif not found: found = True
                else: break
            else:
                moves.append((x, y))
        else:
            break

    found = False
    # check south
    for i in range(7):
        x = loc[0]
        y = loc[1] + (1 + i)
        if y <= 7:
            if currentState[y][x] != 0:  # non-empty space
                if currentState[y][x] % 2 == color: break
                elif not found: found = True
                else: break
            else:
                moves.append((x, y))
        else:
            break

    found = False
    # check north
    for i in range(7):
        x = loc[0]
        y = loc[1] - (1 + i)
        if y >= 0:
            if currentState[y][x] != 0:  # non-empty space
                if currentState[y][x] % 2 == color: break
                elif not found: found = True
                else: break
            else:
                moves.append((x, y))
        else:
            break

    found = False
    # check southwest
    for i in range(7):
        x = loc[0] - (1 + i)
        y = loc[1] + (1 + i)
        if x >= 0 and y <= 7:
            if currentState[y][x] != 0:  # non-empty space
                if currentState[y][x] % 2 == color: break
                elif not found: found = True
                else: break
            else:
                moves.append((x, y))
        else:
            break

    found = False
    # check northwest
    for i in range(7):
        x = loc[0] - (1 + i)
        y = loc[1] - (1 + i)
        if x >= 0 and y >= 0:
            if currentState[y][x] != 0:  # non-empty space
                if currentState[y][x] % 2 == color: break
                elif not found: found = True
                else: break
            else:
                moves.append((x, y))
        else:
            break;

    found = False
    # check northeast
    for i in range(7):
        x = loc[0] + (1 + i)
        y = loc[1] - (1 + i)
        if x <= 7 and y >= 0:
            if currentState[y][x] != 0:  # non-empty space
                if currentState[y][x] % 2 == color: break
                elif not found: found = True
                else: break
            else:
                moves.append((x, y))
        else:
            break;

    found = False
    # check southeast
    for i in range(7):
        x = loc[0] + (1 + i)
        y = loc[1] + (1 + i)
        if x <= 7 and y <= 7:
            if currentState[y][x] != 0:  # non-empty space
                if currentState[y][x] % 2 == color: break
                elif not found: found = True
                else: break
            else:
                moves.append((x, y))
        else:
            break
    return moves

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
            break
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
        if x >= 0 and y <= 7:
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
        if x >= 0 and y >= 0:
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
        if x <= 7 and y >= 0:
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
        if x <= 7 and y <= 7:
            if currentState[x][y] == 6 + opponCol & ~passLeap: #opposing leaper
                passLeap = True
            elif currentState[x][y] != 0: #non-empty space, not leaper
                break;
            else:
                moves.append((x,y))
        else:
            break;

    return moves

# def other():

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
    if loc[0] < 7:
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

# Mathematical sum of all the pieces we have based on a point system.
# the position index in comparision to opponents
# pieces and our pieces in the kings diagonals, verticals and horizontals.
def staticEval(state):
    sum = 0
    for i in range(8):
        for j in range(8):
            x = state[i][j]
            if x != 0:
                if i < 2 and x % 2 == 1:
                    sum += 1
                if i > 5 and x % 2 == 0:
                    sum -= 1
                # checks the number of opponents the freezer has trapped
                if x == 14:
                    sum -= (len(kingHelper([j,i], state, 1)) * 3)
                if x == 15:
                    sum += (len(kingHelper([j, i], state, 0)) * 3)
                # when piece is king checks surrounding places for opponents
                if x == 12:
                    sum -= 1000
                    sum += len(kingHelper([j,i], state, 1))
                elif x == 13:
                    sum += 1000
                    sum -= len(kingHelper([j, i], state, 0))
                # pincers
                elif x == 2:
                    sum -= 2
                elif x == 3:
                    sum += 2
                # all others
                elif x % 2 == 0:
                    sum -= 4
                elif x % 2 == 1:
                    sum += 4
            # Check the middle squares
            if i == 3 or i == 4:
                if j == 3 or j == 4:
                    blackP = kingHelper([j,i], state, 1)
                    whiteP = kingHelper([j,i], state, 0)
                    sum += len(blackP)
                    sum -= len(whiteP)
    return sum


