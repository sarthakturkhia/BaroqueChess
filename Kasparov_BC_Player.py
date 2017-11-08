'''Kasaparov_BC_Player.py
The beginnings of an agent that might someday play Baroque Chess.

'''

import time
import BC_state_etc as BC
from priorityq2 import PriorityQ

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
    board = newState.board
    priQ = PriorityQ()
    startAt = time.time()

    allStates = [[board]] #list of list of states
    while True:
        if time.time() - startAt < timelimit*0.97:
            break
        nextStates = []
        nextPQ = PriorityQ()
        for listOfStates in allStates:
            lastboard = listOfStates[len(listOfStates)-1] #look at the last state in a list of states
            allMoves = getAllMoves(lastboard, whoseMov) #get all possible moves from that last state

            if time.time() - startAt < timelimit*0.97:
                break

            for move in allMoves:
                newlist = listOfStates.append(getState(lastboard, move))
                nextStates.append(newlist) #for all the generated moves, generate the new state, and append the new state to the previous list of states.     
                nextPQ.insert(newlist, ((-1)**newState.whose_move)*staticEval(newlist, len(allMoves), startAt, timelimit))

                if time.time() - startAt < timelimit*0.97:
                    break
        
        if time.time() - startAt < timelimit*0.97:
            break

        priQ = nextPQ
        allStates = nextStates

    #assumes time is close to up.
    
    bestMove = priQ.deletemin()[0]
    move = getMoveBeforeAfter(bestMove[0],bestMove[1])
    newState = bestMove[1]

    # Construct a representation of the move that goes from the
    # currentState to the newState.
    # Here is a placeholder in the right format but with made-up
    # numbers:
    #move = ((6, 4), (3, 4))

    # Make up a new remark
    newRemark = "I'll think harder in some future game. Here's my move"

    return [[move, newState], newRemark]

def getMoveBeforeAfter(oldstate, newstate):
    move = ((-1,-1),(-1,-1))
    for i in range(7):
        for j in range(7):
            if not oldstate[i][j] == newstate[i][j] & oldstate[i][j] == 0:
                move[1][0] = i
                move[1][1] = j
            elif not oldstate[i][j] == newstate[i][j] & newstate[i][j] == 0:
                move[0][0] = i
                move[0][1] = j
    return move

def getAllMoves(currentState, whose_move):
    moves = []
    for i in range(7):
        for j in range(7):
            current = currentState[i][j]
            if current%2 == whose_move:
                current = current - current%2
                if current == 2:
                    moves.append([((i,j),(x,y)) for (x,y) in pincer([i,j], currentState)])
                elif current == 6:
                    moves.append([((i,j),(x,y)) for (x,y) in Knight([i,j], currentState)])
                elif current == 8:
                    moves.append([((i,j),(x,y)) for (x,y) in imitator([i,j], currentState)])
                elif current == 12:
                    moves.append([((i,j),(x,y)) for (x,y) in king([i,j], currentState)])
                else:
                    moves.append([((i,j),(x,y)) for (x,y) in other([i,j], currentState)])
    return moves # moves is a list of elements in the form of ((x,y),(x2,y2))

# takes a move and returns a new state of the complete board after the move was made
def getState(currentstate, move): #(move: ((x,y),(x2,y2)) ) #pass in individual moves instead of list
    

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
        if x >= 0 & y <= 7:
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
        if x >= 0 & y >= 0:
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
        if x <= 7 & y >= 0:
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
        if x <= 7 & y <= 7:
            if currentState[x][y] == 6 + opponCol & ~passLeap: #opposing leaper
                passLeap = True
            elif currentState[x][y] != 0: #non-empty space, not leaper
                break;
            else:
                moves.append((x,y))
        else:
            break;
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
            if currentState[x][y] != 0: #non-empty space, stop checking direction
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
            if currentState[x][y] != 0: #non-empty space, stop checking direction
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
            if currentState[x][y] != 0: #non-empty space, stop checking direction
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
            if currentState[x][y] != 0: #non-empty space, stop checking direction
                break;
            else:
                moves.append((x,y))
        else:
            break;
    
    #check southwest
    for i in range(7):
        x = loc[0] - (1+i)
        y = loc[1] + (1+i)
        if x >= 0 & y <= 7:
            if currentState[x][y] != 0: #non-empty space, stop checking direction
                break;
            else:
                moves.append((x,y))
        else:
            break;
    
    #check northwest
    for i in range(7):
        x = loc[0] - (1+i)
        y = loc[1] - (1+i)
        if x >= 0 & y >= 0:
            if currentState[x][y] != 0: #non-empty space, stop checking direction
                break;
            else:
                moves.append((x,y))
        else:
            break;
    
    #check northeast
    for i in range(7):
        x = loc[0] + (1+i)
        y = loc[1] - (1+i)
        if x <= 7 & y >= 0:
            if currentState[x][y] != 0: #non-empty space, stop checking direction
                break;
            else:
                moves.append((x,y))
        else:
            break;
    
    #check southeast
    for i in range(7):
        x = loc[0] + (1+i)
        y = loc[1] + (1+i)
        if x <= 7 & y <= 7:
            if currentState[x][y] != 0: #non-empty space, stop checking direction
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

def staticEval(states, nMoves, startTime, timelimit): #accepts a list of states and also the number of moves
    total = 0
    for state in states:
        if time.time() - startAt < timelimit*0.97:
            break
        total += staticEval(state)
    return total / len(states)

# Mathematical sum of all the pieces we have based on a point system. + the position index in comparision to opponents
# pieces and our pieces in the kings diagonals, verticals and horizontals. subtract the same for our opponent from this sum.
def staticEval(states):
    return 