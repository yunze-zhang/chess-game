import pygame as p
import ChessEngine

WIDTH = HEIGHT = 480
DIMENSION = 8
SQ_SIZE = WIDTH // DIMENSION
IMAGES = {}

'''
Function to load required images into game
'''
def loadImages():
    pieces = ["wP", "wN", "wB", "wR", "wQ", "wK", "bP", "bN", "bB", "bR", "bQ", "bK"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))

'''
Main Function
'''
def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    loadImages()
    running = True
    selectedSq = ()
    playerClicks = []
    validMoves = []
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False

            if e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                selectedSq = (row, col)
                playerClicks.append((row, col))
                if len(playerClicks) == 1:
                    if gs.board[row][col][0] == ("w" if gs.whiteToMove else "b"): #Valid selection
                        validMoves = gs.generateValidMoves(row, col)
                    else:
                        playerClicks = []

                elif len(playerClicks) == 2:
                    move = ChessEngine.Move(playerClicks[0][0], playerClicks[0][1], row, col)
                    if gs.checkValidMove(move, validMoves):
                        gs.makeMove(move)
                    playerClicks = []

        drawGameState(screen, gs, selectedSq, validMoves)
        p.display.flip()

'''
Function to draw pieces of current game state onto board
'''
def drawGameState(screen, gs, selectedSq, validMoves):
    drawBoard(screen)
    highlightPossibleMoves(screen, gs, selectedSq, validMoves)
    drawPieces(screen, gs.board)

'''
Function to draw checkered background of board onto screen
'''
def drawBoard(screen):
    colors = [p.Color(240, 217, 181), p.Color(181, 136, 98)]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r+c)%2]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

'''
Function to draw current pieces onto screen
'''
def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range (DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

'''
Function to highlight possible moves of currently clicked piece onto screen
'''
def highlightPossibleMoves(screen, gs, selectedSq, validMoves):

    if len(selectedSq) == 0: return
    row, col = selectedSq
    if gs.board[row][col][0] == ("w" if gs.whiteToMove else "b"): #Valid selection

        #Highlight selected square
        s = p.Surface((SQ_SIZE, SQ_SIZE))
        s.set_alpha(100)
        s.fill(p.Color("blue"))
        screen.blit(s, (col*SQ_SIZE, row*SQ_SIZE))

        #Highlight squares of valid moves
        s.fill(p.Color("yellow"))
        for r, c in validMoves:
            screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))

if __name__ == "__main__":
    main()
