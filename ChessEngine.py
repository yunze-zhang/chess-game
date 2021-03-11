'''
Class maintaining current state of board.
'''
class GameState():

    '''
    Initiating function for gamestate class. Sets up board and boolean variables
    '''
    def __init__(self):

        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]

        self.whiteToMove = True
        self.whiteKingMoved = False
        self.whiteARookMoved = False
        self.whiteHRookMoved = False
        self.blackKingMoved = False
        self.blackARookMoved = False
        self.blackHRookMoved = False

    '''
    Function to check if row and column are within bounds of chess board
    '''
    def checkBounds(self, row, col):
        if 0 <= row <= 7 and 0 <= col <= 7:
            return True
        else:
            return False

    '''
    Function to check if square provided by parameters is occupied by a piece or not
    '''
    def checkEmpty(self, row, col):
        if self.board[row][col][0] == "-":
            return True
        else:
            return False

    '''
    Function to check validity of possible move for Knight or King
    '''
    def checkPossibleMoves(self, color, possibleMoves, validMoves):

        for r, c in possibleMoves:
            #Check Bounds
            if self.checkBounds(r, c):
                #Square is empty
                if self.checkEmpty(r, c):
                    validMoves.append((r, c))
                #Capture
                elif self.board[r][c][0] != color:
                    validMoves.append((r, c))

    '''
    Function to check validity of possible moves in pre-defined directions for rook bishop
    and queen.
    '''
    def checkPossibleDirections(self, row, col, color, directions, validMoves):

        for d in directions:
            for i in range(1, 7):
                newRow = row + d[0]*i
                newCol = col + d[1]*i
                if self.checkBounds(newRow, newCol): #Valid Bounds
                    newColor = self.board[newRow][newCol][0]
                    if newColor != color: #Possible Move
                        validMoves.append((newRow, newCol))
                        if newColor != "-": #Piece is blocked by enemy piece - break loop
                            break
                    else: #Piece is blocked by own piece - break loop
                        break
                else: #Off the Board
                    break

    '''
    Function to generate all valid moves for pawn.
    '''
    def getPawnMoves(self, row, col, color, validMoves):

        #White Pawn
        if color == "w":
            #Pawn hasnt moved yet - double move
            if row == 6 and self.checkEmpty(row-2, col) and self.checkEmpty(row-1, col):
                validMoves.append((row-2, col))
            #Single Move
            if row != 0 and self.checkEmpty(row-1, col):
                validMoves.append((row-1, col))
            #Captures
            for r, c in [(row-1, col-1), (row-1, col+1)]:
                if self.checkBounds(r, c) and self.board[r][c][0] == "b":
                    validMoves.append((r, c))

        #Black Pawn
        if color == "b":
            #Pawn hasnt moved yet - double move
            if row == 1 and self.checkEmpty(row+2, col) and self.checkEmpty(row+1, col):
                validMoves.append((row+2, col))
            #Single Move
            if row != 7 and self.checkEmpty(row+1, col):
                validMoves.append((row+1, col))
            #Captures
            for r, c in [(row+1, col-1), (row+1, col+1)]:
                if self.checkBounds(r, c) and self.board[r][c][0] == "w":
                    validMoves.append((r, c))

    '''
    Function to generate all valid moves for knight.
    '''
    def getKnightMoves(self, row, col, color, validMoves):

        possibleMoves = [(row+1, col+2), (row+1, col-2), (row-1, col+2), (row-1, col-2),
                         (row+2, col+1), (row+2, col-1), (row-2, col+1), (row-2, col-1)]
        self.checkPossibleMoves(color, possibleMoves, validMoves)

    '''
    Function to generate all valid moves for bishop.
    '''
    def getBishopMoves(self, row, col, color, validMoves):

        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        self.checkPossibleDirections(row, col, color, directions, validMoves)

    '''
    Function to generate all valid moves for rook.
    '''
    def getRookMoves(self, row, col, color, validMoves):

        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        self.checkPossibleDirections(row, col, color, directions, validMoves)

    '''
    Function to generate all valid moves for the Queen.
    '''
    def getQueenMoves(self, row, col, color, validMoves):

        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        self.checkPossibleDirections(row, col, color, directions, validMoves)

    '''
    Function to generate all valid moves for the King.
    '''
    def getKingMoves(self, row, col, color, validMoves):

        possibleMoves = [(row, col+1), (row, col-1), (row+1, col), (row-1, col),
                         (row+1, col+1), (row+1, col-1), (row-1, col+1), (row-1, col-1)]

        if self.shortCastlingAvailable():
            possibleMoves.append((row, col+2))
        if self.longCastlingAvailable():
            possibleMoves.append((row, col-2))

        self.checkPossibleMoves(color, possibleMoves, validMoves)

    '''
    Function to determine if shortside castling is available for current turn.
    '''
    def shortCastlingAvailable(self):

        if self.whiteToMove:
            if self.whiteKingMoved or self.whiteHRookMoved:
                return False
            if self.board[7][5] != "--" or self.board[7][6] != "--":
                return False

        else:
            if self.blackKingMoved or self.blackHRookMoved:
                return False
            if self.board[0][5] != "--" or self.board[0][6] != "--":
                return False

        return True

    '''
    Function to determine if longside castling is available for current turn.
    '''
    def longCastlingAvailable(self):

        if self.whiteToMove:
            if self.whiteKingMoved or self.whiteARookMoved:
                return False
            if self.board[7][1] != "--" or self.board[7][2] != "--" or self.board[7][2] != "--":
                return False

        else:
            if self.blackKingMoved or self.blackARookMoved:
                return False
            if self.board[0][1] != "--" or self.board[0][2] != "--" or self.board[0][3] != "--":
                return False

        return True

    '''
    Function to generate all valid moves for piece selected and return list of squares
    of these valid moves.
    '''
    def generateValidMoves(self, row, col):
        color = self.board[row][col][0]
        piece = self.board[row][col][1]
        validMoves = []

        if piece == "P": #Pawn moves
            self.getPawnMoves(row, col, color, validMoves)

        elif piece == "N": #Knight moves
            self.getKnightMoves(row, col, color, validMoves)

        elif piece == "B": #Bishop moves
            self.getBishopMoves(row, col, color, validMoves)

        elif piece == "R": #Rook moves
            self.getRookMoves(row, col, color, validMoves)

        elif piece == "Q": #Queen moves
            self.getQueenMoves(row, col, color, validMoves)

        elif piece == "K": #King moves
            self.getKingMoves(row, col, color, validMoves)

        return validMoves

    '''
    Function to check validity of move.
    '''
    def checkValidMove(self, move, validMoves):
        prevColor = self.board[move.prevRow][move.prevCol][0]
        newColor = self.board[move.newRow][move.newCol][0]

        # Clicked on empty square
        if prevColor == "-":
            return False

        # Wrong Turn
        if (prevColor == "w" and not self.whiteToMove) or (prevColor == "b" and self.whiteToMove):
            return False

        # Invalid Move
        if (move.newRow, move.newCol) not in validMoves:
            return False

        return True

    '''
    Function to check if the last move was to castle.
    Return Values:
        0 - No castle
        1 - Castled to the left
        2 - Castled to the right
    '''
    def moveWasCastle(self, move):
        if self.board[move.prevRow][move.prevCol][1] == "K":

            if move.newCol == move.prevCol - 2:
                return 1
            if move.newCol == move.prevCol + 2:
                return 2

        return 0

    '''
    Function to castle kingside or queenside depending on parameter given and current player's turn.
    '''
    def castle(self, castled):

        if castled == 1:
            if self.whiteToMove:
                self.board[7][2] = "wK"
                self.board[7][3] = "wR"
                self.board[7][0] = "--"
                self.board[7][4] = "--"
            else:
                self.board[0][2] = "bK"
                self.board[0][3] = "bR"
                self.board[0][0] = "--"
                self.board[0][4] = "--"

        elif castled == 2:
            if self.whiteToMove:
                self.board[7][6] = "wK"
                self.board[7][5] = "wR"
                self.board[7][7] = "--"
                self.board[7][4] = "--"
            else:
                self.board[0][6] = "bK"
                self.board[0][5] = "bR"
                self.board[0][7] = "--"
                self.board[0][4] = "--"

    '''
    Function to update if king and rook have moved for castling rights
    '''
    def updateKingRookMoves(self, move):

        piece = self.board[move.prevRow][move.prevCol]
        if piece == "wK":
            self.whiteKingMoved = True
        elif piece == "bK":
            self.blackKingMoved = True
        elif piece == "wR":
            if move.prevCol == 0:
                self.whiteARookMoved = True
            else:
                self.whiteHRookMoved = True
        elif piece == "bR":
            if move.prevCol == 0:
                self.blackARookMoved = True
            else:
                self.blackHRookMoved = True

    '''
    Function to determine if king at certain square is in check
    '''
    def isInCheck(self, row, col):
        enemyColor = ("b" if self.whiteToMove else "w")
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        for d in directions:
            for i in range(1, 7):
                square = (row + d[0]*i, col + d[1]*i)
                if i == 1:
                    if direction in ([1, 1]):
                        pass

    '''
    Function to make move and update boardstate.
    '''
    def makeMove(self, move):

        self.updateKingRookMoves(move)
        castled = self.moveWasCastle(move)

        if castled == 0:
            self.board[move.newRow][move.newCol] = self.board[move.prevRow][move.prevCol]
            self.board[move.prevRow][move.prevCol] = "--"

        else:
            self.castle(castled)

        self.whiteToMove = not self.whiteToMove


class Move():

    def __init__(self, prevRow, prevCol, newRow, newCol):

        self.prevRow = prevRow
        self.prevCol = prevCol
        self.newRow = newRow
        self.newCol = newCol
