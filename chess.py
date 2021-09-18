import pygame
import cfg
from piece import Piece
from sys import exit
from util import get_closestCoord, get_selected_piece, coord2Pos
# Coordinate system
"""Top left square coordinate: (0,0), bottom right square: coordinate (7,7), right direction: x-axis, down direction: y-axis"""
"""To interept the coordinate tuple, (x, y) 0th index is the x coordinate, 1th index is the y coordinate"""

# Chess board symbol
"""0th index char: side, 1th index char: piece type, "o" for open square"""
"""side: "w" = white ; "b" = black"""
"""piece type: "r" = rook; "n" = knight; "b" = bishop; "q" = queen; "k" = king; "p" = pawn"""


def main():

    # initialize pygame
    pygame.init()
    clock = pygame.time.Clock()

    # initialize display window
    window = pygame.display.set_mode((cfg.WIDTH + cfg.UI_WIDTH, cfg.HEIGHT))
    chessboard = pygame.transform.smoothscale(pygame.image.load("Assets/cb_blue.png").convert_alpha(), (cfg.WIDTH, cfg.HEIGHT))

    # sound
    move_soundeffect = pygame.mixer.Sound("Assets/piecemove_sound.mp3")

    # font
    fontWin = pygame.font.Font("Assets/Pacifico.ttf", 100)
    blackWinImage = fontWin.render("Black Wins", True, "grey")
    whiteWinImage = fontWin.render("White Wins", True, "grey")

    # intro
    introImage = pygame.transform.smoothscale(pygame.image.load("Assets/INTRO.jpeg").convert_alpha(), (cfg.WIDTH + cfg.UI_WIDTH, cfg.HEIGHT))
    fonttitle = pygame.font.Font("Assets/Pacifico.ttf", 125)
    fontStart = pygame.font.Font("Assets/Pacifico.ttf", 75)
    titleImage = fonttitle.render("Pygame Chess", True, "YELLOW")
    startImage = fontStart.render("Click to Start", True, "WHITE")
    titlePos = (150, 50)
    startPos = (150, cfg.HEIGHT//2)

    # create pieces and add to sprite group
    create_pieces()
    addPieces2Group()

    SLT_PIECE = None
    SLT_PIECE_ORICOORD = (0, 0)
    # game Loop
    while True:
        if cfg.INTRO == False:
            for event in pygame.event.get():
                # exit game
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pos()[0] <= cfg.WIDTH:
                        mouseCoord = get_closestCoord(pygame.mouse.get_pos())
                        # get the selected piece instance if it exists
                        SLT_PIECE = get_selected_piece(mouseCoord)

                        # record the selected piece coordinate if it exists
                        if SLT_PIECE is not None:
                            SLT_PIECE.update_piece(SLT_PIECE_ORICOORD, move_soundeffect)
                            SLT_PIECE_ORICOORD = mouseCoord
                        else:
                            SLT_PIECE_ORICOORD = None

                    elif restartRect.collidepoint(pygame.mouse.get_pos()):
                        restart()

                elif event.type == pygame.MOUSEBUTTONUP:
                    if SLT_PIECE is not None:
                        # update the piece attributes after a piece is dropped
                        SLT_PIECE.update_piece(SLT_PIECE_ORICOORD, move_soundeffect)
                    SLT_PIECE = None  # reset

            # drag the selected piece
            if SLT_PIECE is not None:
                SLT_PIECE.rect.center = pygame.mouse.get_pos()

            # draw chessboard
            window.blit(chessboard, (0, 0))

            # draw hint dots
            if SLT_PIECE is not None:
                for coord in SLT_PIECE.viableMove:
                    radius = 25
                    circle = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
                    pygame.draw.circle(circle, (150, 150, 150, 128), (radius, radius), radius)
                    window.blit(circle, (coord2Pos(coord)[0]-cfg.PIECE_WIDTH//4, coord2Pos(coord)[1]-cfg.PIECE_HEIGHT//4))
            # draw ui
            fontui = pygame.font.Font("Assets/Pacifico.ttf", 50)
            ui = pygame.transform.smoothscale(pygame.image.load("Assets/UI.png").convert_alpha(), (cfg.UI_WIDTH, cfg.HEIGHT))
            window.blit(ui, (cfg.WIDTH, 0))
            turnText = "White" if cfg.TURN == "w" else "Black"
            textImage = fontui.render(turnText, True, turnText)
            window.blit(textImage, (cfg.WIDTH + cfg.UI_WIDTH//2 - 70, 50))

            restartImage = fontui.render("Restart", True, "Black")
            restartRect = restartImage.get_rect(topleft=(cfg.WIDTH + cfg.UI_WIDTH//2 - 70, cfg.HEIGHT - 200))
            window.blit(restartImage, (cfg.WIDTH + cfg.UI_WIDTH//2 - 70, cfg.HEIGHT - 200))

            # draw piece
            cfg.PIECE_GROUP.draw(window)

            # draw win condition
            bk = next((piece for piece in cfg.ALIVE_PIECES if piece.side == "b" and piece.pieceType == "k"), None)
            wk = next((piece for piece in cfg.ALIVE_PIECES if piece.side == "w" and piece.pieceType == "k"), None)
            if bk == None:
                cfg.RESTART = True
                window.blit(whiteWinImage, (cfg.UI_WIDTH//2, cfg.HEIGHT//2 - 100))
            if wk == None:
                cfg.RESTART = True
                window.blit(blackWinImage, (cfg.UI_WIDTH//2, cfg.HEIGHT//2 - 100))
            if cfg.RESTART:
                cfg.RESTART_TIME += 1
            if cfg.RESTART_TIME == 60:
                cfg.RESTART = False
                cfg.RESTART_TIME = 0
                restart()

            pygame.display.update()
            clock.tick(cfg.FPS)

        else:  # play cfg.INTRO screen
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    cfg.INTRO = False

            window.blit(introImage, (0, 0))
            window.blit(titleImage, titlePos)
            window.blit(startImage, startPos)
            pygame.display.update()
            clock.tick(cfg.FPS)


def create_pieces():
    """Loop through the BOARD and create a instance for each piece encounter and append cfg.ALIVE_PIECES"""
    for y, rows in enumerate(cfg.CHESSBOARD_INIT):
        for x, sq in enumerate(rows):  # sq: "wp", "bk" etc.
            if sq != "o":  # square is not open
                side = sq[0]
                pieceType = sq[1]
                cfg.ALIVE_PIECES.append(Piece(side, pieceType, (x, y)))  # init Piece instance with with side, pieceType, coord


def addPieces2Group():
    """add all pieces in ALIVE_PIECE to sprite group"""
    for piece in cfg.ALIVE_PIECES:
        cfg.PIECE_GROUP.add(piece)


def restart():
    for piece in cfg.ALIVE_PIECES:
        piece.kill()
    cfg.ALIVE_PIECES = []
    create_pieces()
    addPieces2Group()
    cfg.TURN = "w"


if __name__ == "__main__":
    main()
