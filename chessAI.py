import math
import copy
import numpy as np

"""
Functionality equation modified for AI Chessboard representation
"""

def all_spaces(chessboard, piece):
    """
    Get all actions. Takes input of chess coordinates
    """

    spot = chessboard.convertToChessIndex(piece.spot)

    letters = 'abcdefgh'
    all_list = []

    if piece.piece == 'pawn':
        if piece.color == 'black':
            if piece.runcount == 1:
                piece.moves = [['D2'], ['Y1'], ['Z1']]
            else:
                piece.moves = [['D1'], ['Y1'], ['Z1']]
        elif piece.color == 'white':
            if piece.runcount > 1:
                piece.moves = [['U1'], ['W1'], ['X1']]

    for possibility in piece.moves:
        sublist = []
        
        splitspot = list(spot)
        splitspot[1] = int(splitspot[1])
        for move in possibility:
            lstrindex = letters.find(spot[0])
            for i in range(int(move[1])):
                if move[0] == 'U':
                    if splitspot[1] > 7:
                        break
                    splitspot[1] += 1
                elif move[0] == 'D':
                    if splitspot[1] < 2:
                        break
                    splitspot[1] -= 1
                elif move[0] == 'L':
                    lstrindex -= 1
                    if lstrindex == -1:
                        break
                    splitspot[0] = letters[lstrindex]
                elif move[0] == 'R':
                    lstrindex += 1
                    if lstrindex == 8:
                        break
                    splitspot[0] = letters[lstrindex]
                elif move[0] == 'W':
                    lstrindex -= 1
                    if splitspot[1] > 7 or lstrindex == -1:
                        break
                    splitspot[1] += 1
                    splitspot[0] = letters[lstrindex]
                elif move[0] == 'X':
                    lstrindex += 1
                    if splitspot[1] > 7 or lstrindex == 8:
                        break
                    splitspot[1] += 1
                    splitspot[0] = letters[lstrindex]
                elif move[0] == 'Y':
                    lstrindex += 1
                    if splitspot[1] < 2 or lstrindex == 8:
                        break
                    splitspot[1] -= 1
                    splitspot[0] = letters[lstrindex]
                elif move[0] == 'Z':
                    lstrindex -= 1
                    if splitspot[1] < 2 or lstrindex == -1:
                        break
                    splitspot[1] -= 1
                    splitspot[0] = letters[lstrindex]
                sublist.append(''.join(str(c) for c in splitspot))
        if len(sublist) > 0:
            all_list.append(sublist)

    if piece.piece == 'knight':
        temp_list = []
        for minilist in all_list:
            if len(minilist) == 3:
                temp_list.append([minilist[-1]])

        return temp_list

    # Returns list of moves in chessIndex form
    return all_list

def possible_spaces(chessboard, piece):
    """
    Returns potential spaces for a given piece.\
    Modified version of chess.poss_spaces(). piece.spot is boardIndex
    """

    # Returns all possible moves for a given piece in chess coordinates
    all = all_spaces(chessboard, piece)
    potenspaces = []
    sublistcount = 0

    # Iterate each possible position
    for sublist in all:
        sublistcount += 1
        for place in sublist:
            
            # Change to (i, j) coordinates
            place = chessboard.convertToBoardIndex(place)

            # White moves
            if piece.color == 'white':

                # Pawn mechanics
                if piece.piece == 'pawn':

                    # Check diagonal movements
                    if sublistcount > 1:

                        # If we can take a black piece diagonally
                        if place in chessboard.black_places and place not in chessboard.white_places:
                            potenspaces.append(chessboard.convertToBoardIndex(place))

                    # Check if coordinate is void of pieces
                    elif place not in chessboard.white_places and place not in chessboard.black_places:
                        potenspaces.append(chessboard.convertToBoardIndex(place))
                    else:
                        break
                
                # Check if given coordinate is void of other white pieces
                elif place not in chessboard.white_places:
                    potenspaces.append(chessboard.convertToBoardIndex(place))

                    # Check for black pieces to take
                    if place in chessboard.black_places:
                        break
                else:
                    break

            # Black moves
            elif piece.color == 'black':

                # Pawn mechanics
                if piece.piece == 'pawn':
                    if sublistcount > 1:

                        # Take diagonally
                        if place in chessboard.white_places and place not in chessboard.black_places:
                            potenspaces.append(chessboard.convertToBoardIndex(place))

                    # If forward movement is not blocked by any piece, move forward
                    elif place not in chessboard.white_places and place not in chessboard.black_places:
                        potenspaces.append(chessboard.convertToBoardIndex(place))
                    else:
                        break

                # Check given coordinate is void of other black pieces
                elif place not in chessboard.black_places:
                    potenspaces.append(chessboard.convertToBoardIndex(place))

                    # Check if white piece is blocking
                    if place in chessboard.white_places:
                        break
                else:
                    break

    # Returns list of moves in boardIndex form
    return potenspaces

def validify_moves(chessboard, piece):
    """
    Returns final list of moves for a given piece
    """

    possible_moves = possible_spaces(chessboard, piece)
    moves = []
    for move in possible_moves:

        if not move_cause_check(chessboard, piece, move):
            moves.append(move)

    return moves

def ischeck(chessboard, kingobj):
    """
    Returns boolean if the given king object is in check
    """

    # Check if white king is in check
    if kingobj.color == 'white':
        for piece in chessboard.blacks:
            all = possible_spaces(chessboard, piece)
            if kingobj.spot in all:
                return True

    # Check if black king is in check
    else:
        for piece in chessboard.whites:
            all = possible_spaces(chessboard, piece)
            if kingobj.spot in all:
                return True

    return False

def ischeckmate(chess, king):
    """
    Returns True if either king is in checkmate
    """

    # If WK not checkmate, return False
    if king.color == 'white':
        for piece in chess.whites:
            if validify_moves(chess, piece) != []:
                return False
                break
    # If BK not checkmate, return False
    else:
        for piece in chess.blacks:
            if validify_moves(chess, piece) != []:
                return False
                break
    return True


def move_cause_check(chessboard, piece, move):
    """
    Checks if a given move causes a check. Returns boolean. Must be in boardIndex form
    """
    oldspot = chessboard.convertToBoardIndex(piece.spot)
    move = chessboard.convertToBoardIndex(move)

    # Check white check
    if piece.color == 'white':
        index = chessboard.white_places.index(oldspot)
        chessboard.white_places[index] = move
        piece.spot = move

        
        # First get the king object
        for item in chessboard.whites:
            if item.piece == "king":
                ki1 = item
                break

        # Check if white king is in check
        istherecheck = ischeck(chessboard, ki1)
        if move in chessboard.black_places:
            for ins in chessboard.blacks:
                if ins.spot == move:
                    chessboard.black_places.remove(ins.spot)
                    chessboard.blacks.remove(ins)

                    istherecheck = ischeck(chessboard, ki1)

                    chessboard.black_places.append(ins.spot)
                    chessboard.blacks.append(ins)
                    break
        chessboard.white_places[index] = oldspot
        piece.spot = oldspot
        return istherecheck

    # Check black check
    elif piece.color == 'black':
        index = chessboard.black_places.index(oldspot)
        chessboard.black_places[index] = move
        piece.spot = move

        # Get king object
        for item in chessboard.blacks:
            if item.piece == "king":
                ki2 = item
                break

        # If check, move
        istherecheck = ischeck(chessboard, ki2)
        if move in chessboard.white_places:
            for ins in chessboard.whites:
                if ins.spot == move:
                    chessboard.white_places.remove(ins.spot)
                    chessboard.whites.remove(ins)

                    istherecheck = ischeck(chessboard, ki2)

                    chessboard.white_places.append(ins.spot)
                    chessboard.whites.append(ins)
                    break
        chessboard.black_places[index] = oldspot
        piece.spot = oldspot
        return istherecheck


"""
AI functions required for minimax algorithm
"""
def actions(chess, AIColor):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    actions = []

    # If player is black, iterate moves per black piece and append to actions
    if AIColor == "black":
        for black in chess.blacks:
            black_cpy = copy.deepcopy(black)
            black_cpy.spot = chess.convertToChessIndex(black_cpy.spot)
            for move in validify_moves(chess, black_cpy):
                actions.append((black, move))

    # If player is white, iterate moves per white piece and append to actions
    if AIColor == "white":
        for white in chess.whites:
            white_cpy = copy.deepcopy(white)
            white_cpy.spot = chess.convertToChessIndex(white_cpy.spot)
            for move in validify_moves(chess, white_cpy):
                actions.append((white, move))

    return actions

def result(chess, action):
    """
    Returns resulted board created via the given action
    """

    # Make deep copy and initialize new piece position
    chess_cpy = copy.deepcopy(chess)
    action_cpy = copy.deepcopy(action)
    piece, move = action_cpy
        
    # Init coordinates to access piece's new position in board
    boardCoords = chess_cpy.convertToBoardIndex(move)
    row, col = boardCoords




    # Check white move
    if piece.color == "white":

        # Get item index for modification of whites and white_places
        for i in range(len(chess_cpy.whites)):
            if piece.spot == chess_cpy.whites[i].spot and piece.name == chess_cpy.whites[i].name:
                break
        indexWhites = i
        boardIndex = chess_cpy.convertToBoardIndex(piece.spot)
        indexWhitePlaces = chess_cpy.white_places.index(boardIndex)

        # Update temporary piece with new information
        piece.spot = boardCoords
        # Pawn exception
        if piece.piece == "pawn":
            piece.runcount += 1

        # Remove from board
        x, y = chess_cpy.whites[indexWhites].spot
        chess_cpy.board[x][y] = '[ ]'

        # Update white piece in whites list
        chess_cpy.whites[indexWhites] = piece

        # Update white piece in white_places
        chess_cpy.white_places[indexWhitePlaces] = chess_cpy.convertToBoardIndex(piece.spot)

        # Check if opponent piece there
        if not isinstance(chess_cpy.board[row][col], str):
            # Remove opponent's piece from board if taken
            chess_cpy.blacks.remove(chess_cpy.board[row][col])

        # Update board
        chess_cpy.board[row][col] = piece
    

    # Check black move
    else:

        # Get item index for modification of blacks and black_places
        for i in range(len(chess_cpy.blacks)):
            if piece.spot == chess_cpy.blacks[i].spot and piece.name == chess_cpy.blacks[i].name:
                break
        indexBlacks = i
        boardIndex = chess_cpy.convertToBoardIndex(piece.spot)
        indexBlackPlaces = chess_cpy.black_places.index(boardIndex)

        # Update temporary piece with new information
        piece.spot = boardCoords
        # Pawn exception
        if piece.piece == "pawn":
            piece.runcount += 1

        # Retrieve coordinates and remove piece from original position
        old_chessIndex = chess_cpy.blacks[indexBlacks].spot
        x, y = chess_cpy.convertToBoardIndex(old_chessIndex)
        chess_cpy.board[x][y] = '[ ]'

        # Update white piece in whites list
        chess_cpy.blacks[indexBlacks] = piece

        # Update white piece in white_places
        chess_cpy.black_places[indexBlackPlaces] = chess_cpy.convertToBoardIndex(piece.spot)

        # Check if opponent piece there
        if not isinstance(chess_cpy.board[row][col], str):
            # Remove opponent's piece from board if taken
            chess_cpy.whites.remove(chess_cpy.board[row][col])

        # Update board
        chess_cpy.board[row][col] = piece

    return chess_cpy

def terminal(chess):
    """
    Returns True if game is over or depth has been reached, False otherwise.
    """
    # Check winner
    if winner(chess):
        return True
    return False

def winner(chess):
    """
    Determines winner of chess game
    """

    # Retrieve king objects and determine checkmate
    for piece in chess.whites:
        if piece.name == "WK":
            if ischeckmate(chess, piece):
                return "white"
            break

    for piece in chess.blacks:
        if piece.name == "BK":
            if ischeckmate(chess, piece):
                return "black"
            break

    return None

def material_score(chess):
    """
    Returns total score of pieces per color
    """

    # Determines factor of how far we are into game
    total_pieces = len(chess.whites) + len(chess.blacks)
    phaseFactor = 1 + ((32 - total_pieces) / 32)

    score = 0

    # As we enter late game, rooks are more valuable
    piece_values = {
        "pawn": 1,
        "rook": phaseFactor * 80,
        "knight": 60,
        "bishop": 60,
        "queen": 200
    }
    pieces = piece_values.keys()

    # Evaluate white misses
    for piece in chess.whites:
        if piece.piece in pieces:
            value = piece_values[piece.piece]
            score += value

    # Evaluate white misses
    for piece in chess.blacks:
        if piece.piece in pieces:
            value = piece_values[piece.piece]
            score -= value

    return score


def var_MD_score(chess):
    """
    Returns total score based on square values per piece
    """

    boards = {
        # Pawn's require flip for white
        "pawn" : [
            [  0,  50,  10,   5,   0,   5,   5,   0],
            [  0,  50,  10,   5,   0,  -5,  10,   0],
            [  0,  50,  20,  10,   0, -10,  10,   0],
            [  0,  50,  30,  25,  20,   0, -20,   0],
            [  0,  50,  30,  25,  20,   0, -20,   0],
            [  0,  50,  20,  10,   0, -10,  10,   0],
            [  0,  50,  10,   5,   0,  -5,  10,   0],
            [  0,  50,  10,   5,   0,   5,   5,   0]
            ],

        # Knights are uniform, no need for flip on white
        "knight" : [
            [-50, -40, -30, -30, -30, -30, -40, -50],
            [-40, -20,   0,   5,   0,   5, -20, -40],
            [-30,   0,  10,  15,  15,  10,   0, -30],
            [-30,   0,  15,  20,  20,  15,   5, -30],
            [-30,   0,  15,  20,  20,  15,   5, -30],
            [-30,   0,  10,  15,  15,  10,   0, -30],
            [-40, -20,   0,   5,   0,   5, -20, -40],
            [-50, -40, -30, -30, -30, -30, -40, -50]
        ],

        # Bishops require flip for white
        "bishop" : [
            [-20, -10, -10, -10, -10, -10, -10, -20],
            [-10,   0,   0,   5,   0,  10,   5, -10],
            [-10,   0,   5,   5,  10,  10,   0, -10],
            [-10,   0,  10,  10,  10,  10,   0, -10],
            [-10,   0,  10,  10,  10,  10,   0, -10],
            [-10,   0,   5,   5,  10,  10,   0, -10],
            [-10,   0,   0,   5,   0,  10,   5, -10],
            [-20, -10, -10, -10, -10, -10, -10, -20]
        ],

        # Rooks require flip for white
        "rook" : [
            [ 0,  5, -5, -5, -5, -5, -5,  0],
            [ 0, 10,  0,  0,  0,  0,  0,  0],
            [ 0, 10,  0,  0,  0,  0,  0,  0],
            [ 0, 10,  0,  0,  0,  0,  0,  5],
            [ 0, 10,  0,  0,  0,  0,  0,  5],
            [ 0, 10,  0,  0,  0,  0,  0,  0],
            [ 0, 10,  0,  0,  0,  0,  0,  0],
            [ 0,  5, -5, -5, -5, -5, -5,  0]
        ],

        # Queen requires flip for white
        "queen" : [
            [-20, -10, -10,  -5,  -5, -10, -10, -20],
            [-10,   0,   0,   0,   0,   0,   0, -10],
            [-10,   0,   5,   5,   5,   5,   0, -10],
            [ -5,   0,   5,   5,   5,   5,   0,  -5],
            [ -5,   0,   5,   5,   5,   5,   0,  -5],
            [-10,   0,   5,   5,   5,   5,   5, -10],
            [-10,   0,   0,   0,   0,   5,   0, -10],
            [-20, -10, -10,  -5,   0, -10, -10, -20]
        ],

        # King requires flip for white
        "king1" : [
            [-30, -30, -30, -30, -20, -10,  20,  20],
            [-40, -40, -40, -40, -30, -20,  20,  30],
            [-40, -40, -40, -40, -30, -20,   0,  10],
            [-50, -50, -50, -50, -40, -20,   0,   0],
            [-50, -50, -50, -50, -40, -20,   0,   0],
            [-40, -40, -40, -40, -30, -20,   0,  10],
            [-40, -40, -40, -40, -30, -20,  20,  30],
            [-30, -30, -30, -30, -20, -10,  20,  20]
        ],

        # King requires flip for white
        "king2" : [
            [-50, -30, -30, -30, -30, -30, -30, -50],
            [-40, -20, -10, -10, -10, -10, -30, -30],
            [-30, -10,  20,  30,  30,  20,   0, -30],
            [-20,   0,  30,  40,  40,  30,   0, -30],
            [-20,   0,  30,  40,  40,  30,   0, -30],
            [-30, -10,  20,  30,  30,  20,   0, -30],
            [-40, -20, -10, -10, -10, -10, -30, -30],
            [-50, -30, -30, -30, -30, -30, -30, -50]
        ]
    }

    # Determines factor of how far we are into game
    total_pieces = len(chess.whites) + len(chess.blacks)
    phaseFactor = (32 - total_pieces) / 32

    # MidGame, remove both boards and keep king1
    if phaseFactor < 0.66:
        boardKing = boards["king1"]
        boards.pop("king1")
        boards.pop("king2")
        boards["king"] = boardKing
    # Late game, only keep king2
    else:
        boardKing = boards["king2"]
        boards.pop("king1")
        boards.pop("king2")
        boards["king"] = boardKing


    # Iterate boards for all pieces but kings
    boardkeys = list(boards.keys())
    black_score = 0
    white_score = 0
    for board in boardkeys[:5]:

        # Find value per black piece
        for black in chess.blacks:
            # If we have the correct piece, get piece coords and find value
            if black.piece == board:
                x, y = black.spot
                value = boards[board][x][y]
                black_score += value

        # Flip board for white
        for row in boards[board]:
            row = row[::-1]


        # Find value per white piece
        for white in chess.whites:
            # If we have the correct piece, get piece coords and find value
            if white.piece == board:
                x, y = white.spot
                value = boards[board][x][y]
                white_score += value




    return white_score - black_score

def utility(chess):
    """
    Returns value heuristic of current game state
    """

    score = 0

    player = winner(chess)
    # Winner recieves 100 points reward
    if player == "black":
        return -1000
    elif player == "white":
        return 1000

    

    # Heuristic
    score += (var_MD_score(chess) + material_score(chess))


    return score



# Node Class for value and corresponding action
class choice:
    def __init__(self, value, move):
        self.value = value
        self.move = move

def minimax(chess, AIColor, depth):
    """
    Returns the optimal action for the current player on the board.\
    Conditioned for Alpha-Beta Pruning
    """
    

    # Max-Value Function
    def max_value(s, a, b, depth):
        
        # Check if we've reached final state
        if terminal(s) or depth == 0:
            return choice(utility(s), None)

        # Max will choose the first option
        v = choice(-10000, None)

        # Iterate through actions and find what min would do
        for action in actions(s, "white"):
            
            # Display for debug
            #print("\nWhite needs to make a turn. Max-Value")
            #s.display()
            
            # Get child action and value
            child = choice(min_value(result(s, action), a, b, depth - 1).value, action)           

            # Determine update for values
            if (child.value > v.value):
                v = child

            # Check pruning
            if (child.value >= b):
                return v

            # Update new alpha
            if (child.value > a):
                a = child.value

        # Return to min or to runner.py
        return v

    # Min-Value Function
    def min_value(s, a, b, depth):

        # Check terminal condition
        if terminal(s) or depth == 0:
            return choice(utility(s), None)

        # Min will always get smaller
        v = choice(10000, None)

        # Iterate through actions, determine what max would do
        for action in actions(s, "black"):
            
            # Display for debug
            #print("\nBlack needs to make a turn. Min-Value")
            #s.display()

            # Get child action and value
            child = choice(max_value(result(s, action), a, b, depth - 1).value, action)

            # Update value
            if (child.value < v.value):
                v = child

            # Check prune
            if (child.value <= a):
                return v

            # Update beta
            if (child.value < b):
                b = child.value

        # Return to max or runner.py
        return v

    # Choose best action from all possible actions & ratings given the symbol of AI
    if (AIColor == "white"):
        return max_value(chess, -10000, 10000, depth).move
    else:
        return min_value(chess, -10000, 10000, depth).move