'''Kasaparov_BC_Player.py
The beginnings of an agent that might someday play Baroque Chess.
'''

import time
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

def makeMove(currentState, currentRemark, timelimit): #time limit in miliseconds
    # Compute the new state for a move.
    # This is a placeholder that just copies the current state.
    newState = BC.BC_state(currentState.board)

    # Fix up whose turn it will be.
    newState.whose_move = 1 - currentState.whose_move
    whoseMove = newState.whose_move

    board = newState.board
    startAt = time.time()
    bestrating = 0
    bestMove = []

    allStates = [[board]] #list of list of states
    while True:
        if time.time() - startAt> timelimit*0.97:
            break
        nextStates = []
        depthXrating = 100000 #reset rating to something big
        for listOfStates in allStates:
            lastboard = listOfStates[len(listOfStates)-1] #look at the last state in a list of states
            allMoves = getAllMoves(lastboard, whoseMove) #get all possible moves from that last state
            newlist = []
            #print(allMoves)
            #print(lastboard)
            if time.time() - startAt> timelimit*0.97:
                break
            for move in allMoves:
                #print(move)
                newlist.append(listOfStates + [getState(move, lastboard)])
                if time.time() - startAt> timelimit*0.97:
                    break
            #print(newlist)
            for listState in newlist:
                #print(listState)
                rating = ((-1)**newState.whose_move)*staticEval2(listState, len(allMoves), startAt, timelimit)
                #rating => the smaller, the better it is for US, THIS player
                #if we are white, whosemove=1, good move = big => -1**whosemove good move = small
                #if we are black, whosemove=0, good move = small => -1**whosemove good move = small
            #nextStates.append(newlist) #for all the generated moves, generate the new state, and append the new state to the previous list of states.     
                if rating < depthXrating:
                    #print(rating)
                    depthXrating = rating
                    bestrating = rating
                    bestMove = listState

            whoseMove = 1 - whoseMove
        
        if time.time() - startAt> timelimit*0.97:
            break

        allStates = nextStates

    #assumes time is close to up.
    #print(bestMove)
    move = getMoveBeforeAfter(bestMove[0],bestMove[1])
    newState.board = bestMove[1]
    newState.whose_move = 1- currentState.whose_move

    # Construct a representation of the move that goes from the
    # currentState to the newState.
    # Here is a placeholder in the right format but with made-up
    # numbers:
    #move = ((6, 4), (3, 4))

    # Make up a new remark
    newRemark = getRemark(bestrating)

    return [[move, newState], newRemark]

# takes a move and returns a new state of the complete board after the move was made
def getState(move, state):

    resultstate = [[0,0,0,0,0,0,0,0] for i in range(8)]
    for i in range(8):
        for j in range(8):
            resultstate[i][j] = state[i][j]
    #print(resultstate)
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
        if diffX != 0 :
            x = int(diffX/abs(diffX))
        else:
            x = 0
        if diffY != 0:
            y = int(diffY/abs(diffY))
        else:
            y=0            
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
    
    # withdrawer
    elif piece - color == 10:
        if len(kingHelper(intlLoc, state, opoColor)) != 0:
            dirY = intlLoc[0]-goalLoc[0]
            dirX = intlLoc[1]-goalLoc[1]
            if dirY != 0:
                dirY = dirY/abs(dirY)
            if dirX != 0:
                dirX = dirX/abs(dirX)
            opoY = int(intlLoc[0]-dirY)
            opoX = int(intlLoc[1]-dirX)
            if opoY in range(8) and opoX in range(8) and resultstate[opoY][opoX]%2 == opoColor:
                resultstate[opoY][opoX] = 0

    # imitator
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

def getRemark(score):
    if score > 500:
        return "uh oh."
    if score > 100:
        return "This is real bad."
    if score > 75:
        return "I'm getting a little worried here."
    if score > 50:
        return "This isn't over yet!"
    if score > 30:
        return "You got me."
    if score > 20:
        return "Nice move."
    if score > 10:
        return "Finally we're getting somewhere."
    if score > -5:
        return "This is going nowhere."
    if score > -15:
        return "Finally we're getting somewhere."
    if score > -25:
        return "Take that!"
    if score > -35:
        return "Having a little trouble there?"
    if score > -55:
        return "You're free to give up."
    if score > -75:
        return "I'd like to see how you would get out of that."
    if score > -100:
        return "Victory is in sight!"
    return "Good game."

def getMoveBeforeAfter(oldstate, newstate):
    move = [[-1,-1],[-1,-1]]
    for i in range(7):
        for j in range(7):
            if not oldstate[i][j] == newstate[i][j] and oldstate[i][j] == 0:
                move[1][0] = i
                move[1][1] = j
            elif not oldstate[i][j] == newstate[i][j] and newstate[i][j] == 0:
                move[0][0] = i
                move[0][1] = j
    return move

def getAllMoves(currentState, whose_move):
    moves = []
    for i in range(8):
        for j in range(8):
            current = currentState[i][j]
            if current != 0 and current%2 == whose_move:
                current = current - current%2
                if current == 2:
                    moves += [[[j,i],[x,y]] for [x,y] in pincer([j,i], currentState)]
                elif current == 6:
                    moves += [[[j,i],[x,y]] for [x,y] in knight([j,i], currentState)]
                elif current == 8:
                    moves += [[[j,i],[x,y]] for [x,y] in imitator([i,j], currentState)]
                elif current == 12:
                    moves += [[[j,i],[x,y]] for [x,y] in king([j,i], currentState)]
                else:
                    moves += [[[j,i],[x,y]] for [x,y] in other([j,i], currentState)]
    return moves # moves is a list of elements in the form of ((x,y),(x2,y2))
    
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
    # currentState = [[4, 6, 8, 10, 12, 8, 6, 14], [2, 2, 2, 2, 2, 2, 2, 2], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [3, 3, 3, 3, 3, 3, 3, 3], [15, 7, 9, 11, 13, 9, 7, 5]]
    # loc = [0, 1]
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
    if checkFreezer(loc, currentState): 
        return moves
    
    color = currentState[loc[1]][loc[0]] % 2
    opponCol = 1 - color #opponent's color

    passLeap = False

    #check west
    for i in range(7):
        x = loc[0] - (1+i)
        y = loc[1]
        if x >= 0:
            if currentState[x][y] == 6 + opponCol and ~passLeap: #opposing leaper
                passLeap = True
            elif currentState[x][y] != 0: #non-empty space, not leaper
                break
            else:
                moves.append((x,y))
        else:
            break
    passLeap = False

    #check east
    for i in range(7):
        x = loc[0] + (1+i)
        y = loc[1]
        if x <= 7:
            if currentState[x][y] == 6 + opponCol and ~passLeap: #opposing leaper
                passLeap = True
            elif currentState[x][y] != 0: #non-empty space, not leaper
                break
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
            if currentState[x][y] == 6 + opponCol and ~passLeap: #opposing leaper
                passLeap = True
            elif currentState[x][y] != 0: #non-empty space, not leaper
                break
            else:
                moves.append((x,y))
        else:
            break
    passLeap = False

    #check north
    for i in range(7):
        x = loc[0]
        y = loc[1] - (1+i)
        if y >= 0:
            if currentState[x][y] == 6 + opponCol and ~passLeap: #opposing leaper
                passLeap = True
            elif currentState[x][y] != 0: #non-empty space, not leaper
                break
            else:
                moves.append((x,y))
        else:
            break
    passLeap = False

    #check southwest
    for i in range(7):
        x = loc[0] - (1+i)
        y = loc[1] + (1+i)
        if x >= 0 and y <= 7:
            if currentState[x][y] == 6 + opponCol and ~passLeap: #opposing leaper
                passLeap = True
            elif currentState[x][y] != 0: #non-empty space, not leaper
                break
            else:
                moves.append((x,y))
        else:
            break
    passLeap = False

    #check northwest
    for i in range(7):
        x = loc[0] - (1+i)
        y = loc[1] - (1+i)
        if x >= 0 and y >= 0:
            if currentState[x][y] == 6 + opponCol and ~passLeap: #opposing leaper
                passLeap = True
            elif currentState[x][y] != 0: #non-empty space, not leaper
                break
            else:
                moves.append((x,y))
        else:
            break
    passLeap = False

    #check northeast
    for i in range(7):
        x = loc[0] + (1+i)
        y = loc[1] - (1+i)
        if x <= 7 and y >= 0:
            if currentState[x][y] == 6 + opponCol and ~passLeap: #opposing leaper
                passLeap = True
            elif currentState[x][y] != 0: #non-empty space, not leaper
                break
            else:
                moves.append((x,y))
        else:
            break
    passLeap = False

    #check southeast
    for i in range(7):
        x = loc[0] + (1+i)
        y = loc[1] + (1+i)
        if x <= 7 and y <= 7:
            if currentState[x][y] == 6 + opponCol and ~passLeap: #opposing leaper
                passLeap = True
            elif currentState[x][y] != 0: #non-empty space, not leaper
                break
            else:
                moves.append((x,y))
        else:
            break

    return moves



def other(loc, currentState):
    moves = []
    if checkFreezer(loc, currentState):
        return moves
    
    color = currentState[loc[1]][loc[0]] % 2
    opponCol = 1 - color #opponent's color

    #check west
    for i in range(7):
        x = loc[0] - (1+i)
        y = loc[1]
        if x >= 0:
            if currentState[y][x] != 0: #non-empty space, stop checking direction
                break;
            else:
                moves.append((x,y))
        else:
            break;
    
    #check east
    for i in range(7):
        x = loc[0] + (1+i)
        y = loc[1]
        if x <= 7:
            if currentState[y][x] != 0: #non-empty space, stop checking direction
                break;
            else:
                moves.append((x,y))
        else:
            break;
    
    #check south
    for i in range(7):
        x = loc[0] 
        y = loc[1] + (1+i)
        if y <= 7:
            if currentState[y][x] != 0: #non-empty space, stop checking direction
                break;
            else:
                moves.append((x,y))
        else:
            break;
    
    #check north
    for i in range(7):
        x = loc[0] 
        y = loc[1] - (1+i)
        if y >= 0:
            if currentState[y][x] != 0: #non-empty space, stop checking direction
                break;
            else:
                moves.append((x,y))
        else:
            break;
    
    #check southwest
    for i in range(7):
        x = loc[0] - (1+i)
        y = loc[1] + (1+i)
        if x >= 0 and y <= 7:
            if currentState[y][x] != 0: #non-empty space, stop checking direction
                break;
            else:
                moves.append((x,y))
        else:
            break;
    
    #check northwest
    for i in range(7):
        x = loc[0] - (1+i)
        y = loc[1] - (1+i)
        if x >= 0 and y >= 0:
            if currentState[y][x] != 0: #non-empty space, stop checking direction
                break;
            else:
                moves.append((x,y))
        else:
            break;
    
    #check northeast
    for i in range(7):
        x = loc[0] + (1+i)
        y = loc[1] - (1+i)
        if x <= 7 and y >= 0:
            if currentState[y][x] != 0: #non-empty space, stop checking direction
                break;
            else:
                moves.append((x,y))
        else:
            break;
    
    #check southeast
    for i in range(7):
        x = loc[0] + (1+i)
        y = loc[1] + (1+i)
        if x <= 7 and y <= 7:
            if currentState[y][x] != 0: #non-empty space, stop checking direction
                break;
            else:
                moves.append((x,y))
        else:
            break;
    return moves

#returns true if there is an opponent's freezer in any of the 8 directions, else returns false
def checkFreezer(loc, currentState):
    color = currentState[loc[0]][loc[1]] % 2
    opponCol = 1 - color #opponent's color
    if loc[0] > 0:
        if currentState[loc[0]-1][loc[1]] == 8 + opponCol:
            return checkFreezer((loc[0]-1, loc[1]), currentState)
        elif currentState[loc[0]-1][loc[1]] == 14 + opponCol:
            return True
        if loc [1] > 0:
            if currentState[loc[0]-1][loc[1]-1] == 14 + opponCol:
                return True
            elif currentState[loc[0]-1][loc[1]-1] == 8 + opponCol:
                return checkFreezer((loc[0]-1, loc[1]-1), currentState)
        if loc [1] < 7:
            if currentState[loc[0]-1][loc[1]+1] == 14 + opponCol:
                return True
            elif currentState[loc[0]-1][loc[1]+1] == 8 + opponCol:
                return checkFreezer((loc[0]+1, loc[1]), currentState)
    if loc[0] < 7:
        if currentState[loc[0]+1][loc[1]] == 8 + opponCol:
            return checkFreezer((loc[0]+1, loc[1]), currentState)
        elif currentState[loc[0]+1][loc[1]] == 14 + opponCol:
            return True
        if loc [1] > 0:
            if currentState[loc[0]+1][loc[1]-1] == 14 + opponCol:
                return True
            elif currentState[loc[0]+1][loc[1]-1] == 8 + opponCol:
                return checkFreezer((loc[0]+1, loc[1]-1), currentState)
        if loc [1] < 7:
            if currentState[loc[0]+1][loc[1]+1] == 14 + opponCol:
                return True
            elif currentState[loc[0]+1][loc[1]+1] == 8 + opponCol:
                return checkFreezer((loc[0]+1, loc[1]+1), currentState)
    if loc [1] > 0:
        if currentState[loc[0]][loc[1]-1] == 14 + opponCol:
            return True
        elif currentState[loc[0]][loc[1]-1] == 8 + opponCol:
            return checkFreezer((loc[0], loc[1]-1), currentState)
    if loc [1] < 7:
        if currentState[loc[0]][loc[1]+1] == 14 + opponCol:
            return True
        elif currentState[loc[0]][loc[1]+1] == 8 + opponCol:
            return checkFreezer((loc[0], loc[1]+1), currentState)

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
    # print(state)
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

def staticEval2(states, nMoves, startTime, timelimit): #accepts a list of states and also the number of moves
    total = 0
    #print(states)
    for state in states:
        #print(state)
        if time.time() - startTime> timelimit*0.97:
            break
        total += staticEval(state)
    return total / len(states)