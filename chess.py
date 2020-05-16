import copy
import chessAI


class ChessBoard:
    """
    ChessBoard Object with list of Blacks, Whites, and coordinates
    """

    def __init__(self, whitelist, blacklist, board=[]):
        self.whites = []
        self.blacks = []
        self.white_places = []
        self.black_places = []

        # Convert to board
        self.board = self.make_board(whitelist, blacklist)

        # Create list of Black and White pieces
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if isinstance(self.board[i][j], Chesspiece):
                    if self.board[i][j].name[0] == "W":
                        self.whites.append(self.board[i][j])
                        self.white_places.append(self.board[i][j].spot)

                    else:
                        self.blacks.append(self.board[i][j])
                        self.black_places.append(self.board[i][j].spot)


    def convertAllToBoardIndex(self, whitelist, blacklist):
        """
        Converts chess coordinates to board index (i, j)
        """

        # Iterate each list and convert to indexes
        whites = copy.deepcopy(whitelist)
        blacks = copy.deepcopy(blacklist)
        for square in whites:
            if not isinstance(square, tuple):
                square.spot = square.spot.upper()
                square.spot = (ord(square.spot[0]) - 65, int(square.spot[1]) - 1)
        for square in blacks:
            if not isinstance(square, tuple):
                square.spot = square.spot.upper()
                square.spot = (ord(square.spot[0]) - 65, int(square.spot[1]) - 1)

        return whites, blacks

    def convertToBoardIndex(self, chess_coordinate):
        """
        Converts singular chess coordinate (letter, number) to (i, j)
        """
        if isinstance(chess_coordinate[0], str):
            return ord(chess_coordinate[0].upper()) - 65, int(chess_coordinate[1]) - 1
        else:
            return chess_coordinate

    def convertToChessIndex(self, coordinate):
        """
        Converts board index (i, j) to chess index (letter, j)
        """

        letters = "abcdefgh"
        if not isinstance(coordinate[0], str):
            return (letters[coordinate[0]] + str(coordinate[1] + 1))
        else:
            return coordinate

    def make_board(self, whitelist, blacklist):
        """
        Returns board given a list of white and black pieces
        """

        # Retrieve edited board pieces with coordinates
        whites, blacks = self.convertAllToBoardIndex(whitelist, blacklist)

        board = []
        # Iterate through board cells and check if pieces lie there
        for i in range(8):
            board.append([])
            for j in range(8):
                board[i].append('[ ]')

                # Iterate white pieces, check if spot == coordinate
                for item in whites:
                    item.whiteobjlist = []
                    item.whitespotlist = []
                    item.blackobjlist = []
                    item.blackspotlist = []
                    item.spots = []

                    if item.spot == (i, j):
                        # Change to item.name for display
                        board[i][j] = item

                # Iterate white pieces, check if spot == coordinate
                for item in blacks:
                    if item.spot == (i, j):
                        # Change to item.name for display
                        board[i][j] = item

        return board

    def display(self):
        """
        Displays the chessboard to terminal
        """

        board_cpy = copy.deepcopy(self.board)

        for i in range(len(board_cpy)):
            for j in range(len(board_cpy[i])):
                if isinstance(board_cpy[i][j], Chesspiece):
                    board_cpy[i][j] = board_cpy[i][j].name

        # Print board to terminal
        print('    1      2      3      4      5      6      7      8')
        letters = 'abcdefgh'
        for i in range(8):
            print(letters[i], board_cpy[i])

class Chesspiece:

    spots = [a + str(i) for i in range(1, 9) for a in 'abcdefgh']
    whitespotlist = []
    blackspotlist = []
    whiteobjlist = []
    blackobjlist = []

    def __init__(self, color, piece, spot, name):
        self.color = color
        self.piece = piece
        self.spot = spot
        self.name = name
        if color == 'white':
            Chesspiece.whitespotlist.append(self.spot)
            Chesspiece.whiteobjlist.append(self)
        else:
            Chesspiece.blackspotlist.append(self.spot)
            Chesspiece.blackobjlist.append(self)
        if piece == 'pawn':
            self.moves = [['U2'], ['W1'], ['X1']]
            self.runcount = 1
        elif piece == 'knight':
            self.moves = [['U2', 'L1'], ['U2', 'R1'], ['R2', 'U1'], ['R2', 'D1'],
            ['D2', 'R1'], ['D2', 'L1'], ['L2', 'D1'], ['L2', 'U1']]
        elif piece == 'rook':
            self.moves = [['U7'], ['D7'], ['L7'], ['R7']]
        elif piece == 'bishop':
            self.moves = [['W7'], ['X7'], ['Y7'], ['Z7']]
        elif piece == 'queen':
            self.moves = [['U7'], ['D7'], ['L7'], ['R7'], ['W7'], ['X7'], ['Y7'], ['Z7']]
        elif piece == 'king':
            self.moves = [['U1'], ['D1'], ['L1'], ['R1'], ['W1'], ['X1'], ['Y1'], ['Z1']]

    def all_spaces(self):
        """
        Get all actions
        """


        letters = 'abcdefgh'
        all_list = []

        if self.piece == 'pawn':
            if self.color == 'black':
                if self.runcount == 1:
                    self.moves = [['D2'], ['Y1'], ['Z1']]
                else:
                    self.moves = [['D1'], ['Y1'], ['Z1']]
            elif self.color == 'white':
                if self.runcount > 1:
                    self.moves = [['U1'], ['W1'], ['X1']]

        for possibility in self.moves:
            sublist = []
            
            splitspot = list(self.spot)
            splitspot[1] = int(splitspot[1])
            for move in possibility:
                lstrindex = letters.find(self.spot[0])
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

        if self.piece == 'knight':
            temp_list = []
            for minilist in all_list:
                if len(minilist) == 3:
                    temp_list.append([minilist[-1]])
            return temp_list

        return all_list

    def poss_spaces(self):
        all = self.all_spaces()
        potenspaces = []
        sublistcount = 0

        # Iterate each possible position
        for sublist in all:
            sublistcount += 1
            for place in sublist:

                # White moves
                if self.color == 'white':

                    # Pawn mechanics
                    if self.piece == 'pawn':
                        if sublistcount > 1:
                            if place in Chesspiece.blackspotlist:
                                potenspaces.append(place)

                        # Check if coordinate is void of pieces
                        elif place not in Chesspiece.whitespotlist and place not in Chesspiece.blackspotlist:
                            potenspaces.append(place)
                        else:
                            break
                    
                    # Check if given coordinate is void of other white pieces
                    elif place not in Chesspiece.whitespotlist:
                        potenspaces.append(place)

                        # Check for black pieces to take
                        if place in Chesspiece.blackspotlist:
                            break
                    else:
                        break

                # Black moves
                elif self.color == 'black':

                    # Pawn mechanics
                    if self.piece == 'pawn':
                        if sublistcount > 1:
                            if place in Chesspiece.whitespotlist:
                                potenspaces.append(place)


                        elif place not in Chesspiece.whitespotlist and place not in Chesspiece.blackspotlist:
                            potenspaces.append(place)
                        else:
                            break

                    # Check given coordinate is void of other black pieces
                    elif place not in Chesspiece.blackspotlist:
                        potenspaces.append(place)

                        # Check if white piece can be taken
                        if place in Chesspiece.whitespotlist:
                            break
                    else:
                        break

        return potenspaces

    def actual_poss_spaces(self):
        possmoves = self.poss_spaces()
        returnspaces = []
        for move in possmoves:
            if not self.moveforcheck(move):
                returnspaces.append(move)

        return returnspaces

    def movepiece(self, space):
        print(self.color.capitalize(), self.piece, 'moves to', space, end='.\n')
        if self.color == 'white':
            index = Chesspiece.whitespotlist.index(self.spot)
            Chesspiece.whitespotlist[index] = space
            if space in Chesspiece.blackspotlist:
                for ins in Chesspiece.blackobjlist:
                    if ins.spot == space:
                        print('White', self.piece, 'takes black', ins.piece, end='.\n')
                        Chesspiece.blackspotlist.remove(ins.spot)
                        Chesspiece.blackobjlist.remove(ins)
                        break
        elif self.color == 'black':
            index = Chesspiece.blackspotlist.index(self.spot)
            Chesspiece.blackspotlist[index] = space
            if space in Chesspiece.whitespotlist:
                for ins in Chesspiece.whiteobjlist:
                    if ins.spot == space:
                        print('Black', self.piece, 'takes white', ins.piece, end='.\n')
                        Chesspiece.whitespotlist.remove(ins.spot)
                        Chesspiece.whiteobjlist.remove(ins)
                        break
        if self.piece == 'pawn':
            self.runcount += 1

        self.spot = space

    def moveforcheck(self, space):
        oldspot = self.spot

        if self.color == 'white':
            index = Chesspiece.whitespotlist.index(self.spot)
            Chesspiece.whitespotlist[index] = space
            self.spot = space
            istherecheck = ischeck(ki1)
            if space in Chesspiece.blackspotlist:
                for ins in Chesspiece.blackobjlist:
                    if ins.spot == space:
                        Chesspiece.blackspotlist.remove(ins.spot)
                        Chesspiece.blackobjlist.remove(ins)

                        istherecheck = ischeck(ki1)

                        Chesspiece.blackspotlist.append(ins.spot)
                        Chesspiece.blackobjlist.append(ins)
                        break
            Chesspiece.whitespotlist[index] = oldspot
            self.spot = oldspot
            return istherecheck

        elif self.color == 'black':
            index = Chesspiece.blackspotlist.index(self.spot)
            Chesspiece.blackspotlist[index] = space
            self.spot = space
            istherecheck = ischeck(ki2)
            if space in Chesspiece.whitespotlist:
                for ins in Chesspiece.whiteobjlist:
                    if ins.spot == space:
                        Chesspiece.whitespotlist.remove(ins.spot)
                        Chesspiece.whiteobjlist.remove(ins)

                        istherecheck = ischeck(ki2)

                        Chesspiece.whitespotlist.append(ins.spot)
                        Chesspiece.whiteobjlist.append(ins)
                        break
            Chesspiece.blackspotlist[index] = oldspot
            self.spot = oldspot
            return istherecheck


def ischeck(kingobj):

    # Check if white king is in check
    if kingobj.color == 'white':
        for piece in Chesspiece.blackobjlist:
            all = piece.poss_spaces()
            if kingobj.spot in all:
                return True
                break

    # Check if black king is in check
    else:
        for piece in Chesspiece.whiteobjlist:
            all = piece.poss_spaces()
            if kingobj.spot in all:
                return True
                break

    return False


def ischeckmate(kingobj):
    if kingobj.color == 'white':
        for obj in Chesspiece.whiteobjlist:
            if obj.actual_poss_spaces() != []:
                return False
                break
    else:
        for obj in Chesspiece.blackobjlist:
            if obj.actual_poss_spaces() != []:
                return False
                break
    return True

        


pa1 = Chesspiece('white', 'pawn', 'a2', 'WP')
pa2 = Chesspiece('white', 'pawn', 'b2', 'WP')
pa2 = Chesspiece('white', 'pawn', 'b2', 'WP')
pa3 = Chesspiece('white', 'pawn', 'c2', 'WP')
pa4 = Chesspiece('white', 'pawn', 'd2', 'WP')
pa5 = Chesspiece('white', 'pawn', 'e2', 'WP')
pa6 = Chesspiece('white', 'pawn', 'f2', 'WP')
pa7 = Chesspiece('white', 'pawn', 'g2', 'WP')
pa8 = Chesspiece('white', 'pawn', 'h2', 'WP')
ro1 = Chesspiece('white', 'rook', 'a1', 'WR')
ro2 = Chesspiece('white', 'rook', 'h1', 'WR')
kn1 = Chesspiece('white', 'knight', 'b1', 'WKN')
kn2 = Chesspiece('white', 'knight', 'g1', 'WKN')
bi1 = Chesspiece('white', 'bishop', 'c1', 'WB')
bi2 = Chesspiece('white', 'bishop', 'f1', 'WB')
qu1 = Chesspiece('white', 'queen', 'd1', 'WQ')
ki1 = Chesspiece('white', 'king', 'e1', 'WK')

pa9 = Chesspiece('black', 'pawn', 'a7', 'BP')
pa10 = Chesspiece('black', 'pawn', 'b7', 'BP')
pa11 = Chesspiece('black', 'pawn', 'c7', 'BP')
pa12 = Chesspiece('black', 'pawn', 'd7', 'BP')
pa13 = Chesspiece('black', 'pawn', 'e7', 'BP')
pa14 = Chesspiece('black', 'pawn', 'f7', 'BP')
pa15 = Chesspiece('black', 'pawn', 'g7', 'BP')
pa16 = Chesspiece('black', 'pawn', 'h7', 'BP')
ro3 = Chesspiece('black', 'rook', 'a8', 'BR')
ro4 = Chesspiece('black', 'rook', 'h8', 'BR')
kn3 = Chesspiece('black', 'knight', 'b8', 'BKN')
kn4 = Chesspiece('black', 'knight', 'g8', 'BKN')
bi3 = Chesspiece('black', 'bishop', 'c8', 'BB')
bi4 = Chesspiece('black', 'bishop', 'f8', 'BB')
qu2 = Chesspiece('black', 'queen', 'd8', 'BQ')
ki2 = Chesspiece('black', 'king', 'e8', 'BK')







def main():

    # Intro
    counter = 0
    print("\nWelcome to playchess.py. Follow the program's instructions to move pieces.")
    print('After selecting the spot of the piece you would like to move, you may enter')
    input('"moves" to see the list all of possible moves. Press Enter to start the game: ')
    print()



    # Determine each player's color
    player = (input("Enter which color you would like to be: ")).lower()
    colors = ["white", "black"]
    if player not in colors:
        while True:
            player = (input("Invalid color, enter which color you would like to be: ")).lower()
            if player == "white":
                break
            elif player == "black":
                break

    if player == "white":
        AIColor = "black"
    elif player == "black":
        AIColor = "white"



    # Determine difficulty of AI (How far it will look into the future)
    depth = input("Enter the AI difficulty (1-5) - (Recommended is 3): ")
    if not depth.isdigit():
        while True:
            depth = input("Invalid option. Re-enter the AI difficulty (1-5): ")
            if depth.isdigit():
                if int(depth) > 0 and int(depth) < 6:
                    break
    elif int(depth) < 1 or int(depth) > 5:
        while True:
            depth = input("Invalid option. Re-enter the AI difficulty (1-5): ")
            if depth.isdigit():
                if int(depth) > 0 and int(depth) < 6:
                    break
    depth = int(depth)





    # While the game is unfinished
    while True:

        # Initialize board
        chessboard = ChessBoard(Chesspiece.whiteobjlist, Chesspiece.blackobjlist)
        print("\n")
        chessboard.display()
        print("\n")



        # WHITE MOVE
        if counter % 2 == 0:
            # Display for user

            
            

            # If AI is white, find best move
            if AIColor == "white":
                AIAction = chessAI.minimax(chessboard, AIColor, depth)
                piece, move  = AIAction
                for item in Chesspiece.whiteobjlist:
                    if item.spot == chessboard.convertToChessIndex(piece.spot):
                        break
                # Convert move to chessIndex
                move = chessboard.convertToChessIndex(move)
                item.movepiece(move)

            else:
                # Get data on given position
                userspot = input('White, enter spot of piece to move: ')
                if userspot in Chesspiece.whitespotlist:
                    for instance in Chesspiece.whiteobjlist:

                        # Find which piece the Chess coordinate refers to
                        if instance.spot == userspot:
                            allmoves = instance.poss_spaces()
                            noncheckmoves = instance.actual_poss_spaces()
                            break
                
                # Reprompt if position is invalid or no available moves
                while userspot not in Chesspiece.whitespotlist or allmoves == [] or noncheckmoves == []:
                    if userspot not in Chesspiece.whitespotlist:
                        print('No white piece is at ' + userspot + '. Try again:', end=' ')
                        print('Here is a list of all your pieces:', Chesspiece.whitespotlist)
                    elif allmoves == []:
                        print(instance.color.capitalize(), instance.piece, 'at', instance.spot, 'can not move anywhere. Try again:', end=' ')
                    else:
                        print('Any move', instance.color, instance.piece, 'at', instance.spot, 'can make will put',
                            instance.color, 'king in check. Try again:', end=' ')

                    userspot = input()

                    if userspot in Chesspiece.whitespotlist:
                        for instance in Chesspiece.whiteobjlist:
                            if instance.spot == userspot:
                                allmoves = instance.poss_spaces()
                                noncheckmoves = instance.actual_poss_spaces()
                                break



                # Prompt move for given piece
                for instance in Chesspiece.whiteobjlist:
                    if instance.spot == userspot:
                        print('Where would you like to move', instance.color, instance.piece, 'to?', end=' ')
                        usermove = input()

                        while True:
                            if usermove == 'moves':
                                print('Possible moves:', ', '.join(noncheckmoves))
                                print('Where would you like to move?', end=' ')
                            elif usermove not in instance.poss_spaces():
                                print(usermove, 'is not a possible spot. Try again:', end=' ')
                            elif instance.moveforcheck(usermove):
                                print('Moving to', usermove, 'will put', instance.color, 'king in check. Try again:', end=' ')
                            else:
                                break

                            usermove = input()




                        # Move piece
                        instance.movepiece(usermove)
                        v = ischeck(ki2)
                        x = ischeckmate(ki2)
                        if v and not x:
                            print('Black king is in check.')
                        break

                if x:
                    print('Checkmate. White wins!')
                    break



        # BLACK MOVE
        else:



            # If AI is black, find best move
            if AIColor == "black":
                AIAction = chessAI.minimax(chessboard, AIColor, depth)
                piece, move  = AIAction
                for item in Chesspiece.blackobjlist:
                    if item.spot == chessboard.convertToChessIndex(piece.spot):
                        break

                # Convert move to chessIndex
                move = chessboard.convertToChessIndex(move)
                item.movepiece(move)



            else:
                # Retrieve info on given position
                userspot = input('Black, enter spot of piece to move: ')
                if userspot in Chesspiece.blackspotlist:
                    for instance in Chesspiece.blackobjlist:
                        if instance.spot == userspot:
                            allmoves = instance.poss_spaces()
                            noncheckmoves = instance.actual_poss_spaces()
                            break

                # Reprompt if given position is invalid or no moves available
                while userspot not in Chesspiece.blackspotlist or allmoves == [] or noncheckmoves == []:
                    if userspot not in Chesspiece.blackspotlist:
                        print('No black piece is at ' + userspot + '. Try again:', end=' ')
                        print('Here is a list of all your pieces: ', Chesspiece.blackspotlist)
                    elif allmoves == []:
                        print(instance.color.capitalize(), instance.piece, 'at', instance.spot, 'can not move anywhere. Try again:', end=' ')
                    else:
                        print('Any move', instance.color, instance.piece, 'at', instance.spot, 'can make will put',
                            instance.color, 'king in check. Try again:', end=' ')

                    userspot = input()

                    if userspot in Chesspiece.blackspotlist:
                        for instance in Chesspiece.blackobjlist:
                            if instance.spot == userspot:
                                allmoves = instance.poss_spaces()
                                noncheckmoves = instance.actual_poss_spaces()
                                break

                # Prompt move for given piece
                for instance in Chesspiece.blackobjlist:
                    if instance.spot == userspot:

                        print('Where would you like to move', instance.color, instance.piece, 'to?', end=' ')
                        usermove = input()

                        while True:
                            if usermove == 'moves':
                                print('Possible moves:', ', '.join(noncheckmoves))
                                print('Where would you like to move?', end=' ')
                            elif usermove not in instance.poss_spaces():
                                print(usermove, 'is not a possible spot. Try again:', end=' ')
                            elif instance.moveforcheck(usermove):
                                print('Moving to', usermove, 'will put', instance.color, 'king in check. Try again:', end=' ')
                            else:
                                break

                            usermove = input()

                        instance.movepiece(usermove)
                        v = ischeck(ki1)
                        x = ischeckmate(ki1)
                        if v and not x:
                            print('White king is in check.')
                        break

                if x:
                    print('Checkmate. Black wins!')
                    break

        counter += 1


main()
