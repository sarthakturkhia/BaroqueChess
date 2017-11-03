
'''BaroqueGameMaster.py
Formerly TimedGameMaster.py which was based on GameMaster.py which in turn is 
 based on code from RunKInARow.py

S. Tanimoto, October 30, 2017.
 Status: Works with the "PlayerSkeleton" agents.
 Has support for validation of moves, when that module becomes available.
 
'''
VERSION = '0.8-BETA'

# Get names of players and time limit from the command line.

import sys
TIME_PER_MOVE = 0.5 # default time limit is half a second.
TURN_LIMIT = 5   # Good for testing.
#TURN_LIMIT = 100 # Terminates runaway games.
if len(sys.argv) > 1:
    import importlib    
    player1 = importlib.import_module(sys.argv[1])
    player2 = importlib.import_module(sys.argv[2])
    if len(sys.argv) > 3:
        TIME_PER_MOVE = float(sys.argv[3])
else:
    import PlayerSkeletonA as player1
    import PlayerSkeletonB as player2

import BC_state_etc as BC

VALIDATE_MOVES = False # If players are trusted not to cheat, this could be turned off to save time.
if VALIDATE_MOVES: import bc_move_validator as V

from winTester import winTester

CURRENT_PLAYER = BC.WHITE


FINISHED = False
def runGame():
    # Set up for the match, and report on its details: 
    currentState = BC.BC_state()
    print('**** Baroque Chess Gamemaster v'+VERSION+' *****')
    print('The Gamemaster says, "Players, introduce yourselves."')
    print(' (Playing WHITE:) '+player1.introduce())
    print(' (Playing BLACK:) '+player2.introduce())

    try:
        p1comment = player1.prepare(player2.nickname())
    except:
        report = 'Player 1 ('+player1.nickname()+' failed to prepare, and loses by default.'
        print(report)
        report = 'Congratulations to Player 2 ('+player2.nickname()+')!'
        print(report)
        return
    try:
        p2comment = player2.prepare(player1.nickname())
    except:
        report = 'Player 2 ('+player2.nickname()+' failed to prepare, and loses by default.'
        print(report)
        report = 'Congratulations to Player 1 ('+player1.nickname()+')!'
        print(report)
        return
    
    print('\nThe Gamemaster says, "Let\'s Play!"\n')
    print('The initial state is...')

    currentRemark = "The game is starting."

    WHITEsTurn = True
    name = None
    global FINISHED
    FINISHED = False
    WINNER = "not yet known"
    turnCount = 1
    print(currentState)
    while not FINISHED:
        # Whoever's turn it is, well, move!
        who = currentState.whose_move
        if who==BC.WHITE:
            side = 'WHITE'; other_side='BLACK'
        else: side = 'BLACK'; other_side='WHITE'
        global CURRENT_PLAYER
        CURRENT_PLAYER = who
        if WHITEsTurn:
            move_fn = player1.makeMove
            name = player1.nickname()
        else:
            move_fn = player2.makeMove
            name = player2.nickname()
        playerResult = timeout(move_fn,args=(currentState, currentRemark, TIME_PER_MOVE), kwargs={}, timeout_duration=TIME_PER_MOVE, default=(None,"I give up!"));
        WHITEsTurn = not WHITEsTurn

        # Let's analyze the response of the player.
        moveAndState, currentRemark = playerResult
        if moveAndState==None:
            print("No move returned by "+side+".")
            WINNER = other_side
            FINISHED = True; break
        # First we handle a special case where there might be a draw, due to
        # no legal moves available to the current player.
        # The player has to return a specific string if it can't find a legal move.
        if currentRemark == "I believe I have no legal moves.":
            if VALIDATE_MOVES:
                (isDraw, newState) = V.any_legal_move(currentState)
                if isDraw:
                    FINISHED=True
                    print("Stalemate: "+side+" has no moves!"); break
                else:
                    print("You claim there are no legal moves,")
                    print("but you COULD go here: ")
                    print(newState.__repr__())
                    print("Game over. "+side+" loses.")
                    WINNER = other_side
                    FINISHED=True
                    break;
            else:
                print("Player "+side+" is requesting a draw. With move validation off,")
                print("we need a human umpire to OK this.")
                answer = input("Enter Y to declare a draw, or N to disallow the draw: ")
                if answer.lower()=='y': WINNER='DRAW'
                else: WINNER=other_side
                FINISHED = True; break
                
        # Some move was returned, so let's find out if it was valid.
        try:
          move, newState = moveAndState
          startsq, endsq = move
          i,j=startsq
          ii,jj=endsq
        except Exception as e:
           print("The moveAndState value did not have the proper form of [move, newState] or")
           print("the move did not have the proper form such as ((3, 7), (5, 7)).")
           WINNER = other_side
           FINISHED = True;
        print(side+"'s move: the "+BC.CODE_TO_INIT[currentState.board[i][j]]+\
              " at ("+str(i)+", "+str(j)+") to ("+str(ii)+", "+str(jj)+").")
        
        if VALIDATE_MOVES:
            (status, result)=V.validate(move, currentState, newState)
            
            if not status:
                print("Illegal move by "+side)  # Returned state is:\n" + str(currentState))
                print(result)

                print(side+"'s proposed, new state is: ")
                print(newState.__repr__())
                WINNER = other_side
                FINISHED=True
                break
            else:
                print("valid move")
                print(result)

        moveReport = "Turn "+str(turnCount)+": Move is by "+side
        print(moveReport)
        utteranceReport = name +' says: '+currentRemark
        print(utteranceReport)
        currentState = newState
        possibleWin = winTester(currentState)
        if possibleWin != "No win":
            WINNER = side
            FINISHED = True
            print(currentState)
            print(possibleWin)
            break
        print(currentState)
        turnCount += 1
        if turnCount > TURN_LIMIT:
            FINISHED=True
            print("TURN_LIMIT exceeded! ("+str(TURN_LIMIT)+")")
            break

    print("Game over.")
    if (WINNER=="not yet known") or (WINNER == "DRAW"):
      print("The outcome is a DRAW.  Nobody wins.")
    else:
      print("Congratulations to the winner: "+WINNER)


import sys
import time
def timeout(func, args=(), kwargs={}, timeout_duration=1, default=None):
    '''This function will spawn a thread and run the given function using the args, kwargs and 
    return the given default value if the timeout_duration is exceeded 
    ''' 
    import threading
    class PlayerThread(threading.Thread):
        def __init__(self):
            threading.Thread.__init__(self)
            self.result = default
        def run(self):
            try:
                self.result = func(*args, **kwargs)
            except Exception as e:
                print("Seems there was an exception during play by "+CURRENT_PLAYER+":\n"+str(e))
                print(sys.exc_info())
                self.result = default

    pt = PlayerThread()
    pt.start()
    started_at = time.time()
    pt.join(timeout_duration)
    ended_at = time.time()
    diff = ended_at - started_at
    print("Time used in makeMove: %0.4f seconds out of " % diff, timeout_duration)
    if pt.isAlive():
        print("Took too long.")
        print("We are now terminating the game.")
        print("Player "+CURRENT_PLAYER+" loses.")
        if USE_HTML: gameToHTML.reportResult("Player "+CURRENT_PLAYER+" took too long (%04f seconds) and thus loses." % diff)
        if USE_HTML: gameToHTML.endHTML()
        exit()
    else:
        #print("Within the time limit -- nice!")
        return pt.result

runGame()
