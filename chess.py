import pygame
from sys import exit
from math import sqrt

# Coordinate system
"""Top left square coordinate: (0,0), bottom right square: coordinate (7,7), right direction: x-axis, down direction: y-axis"""
"""To interept the coordinate tuple, (x, y) 0th index is the x coordinate, 1th index is the y coordinate"""

# Chess board symbol
"""0th index char: side, 1th index char: piece type, "o" for open square"""
"""side: "w" = white ; "b" = black"""
"""piece type: "r" = rook; "n" = knight; "b" = bishop; "q" = queen; "k" = king; "p" = pawn"""

# GLOBAL CONSTANT
WIDTH, HEIGHT = 800, 800
PIECE_WIDTH, PIECE_HEIGHT = 100, 100
BOARD_LENGTH = 8
FPS = 120

CHESSBOARD_INIT = [
    ["br", "bn", "bb", "bq", "bk", "bb", "bn", "br"],
    ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
    ["o",  "o",  "o",  "o",  "o",  "o",  "o",  "o"],
    ["o",  "o",  "o",  "o",  "o",  "o",  "o",  "o"],
    ["o",  "o",  "o",  "o",  "o",  "o",  "o",  "o"],
    ["o",  "o",  "o",  "o",  "o",  "o",  "o",  "o"],
    ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
    ["wr", "wn", "wb", "wq", "wk", "wb", "wn", "wr"]
]

# Global variables
ALIVE_PIECES = []  # list of alive piece instances
PIECE_GROUP = pygame.sprite.Group()  # piece sprite group

class Piece(pygame.sprite.Sprite):

    def __init__(self, side, pieceType, coord):
        super().__init__()
        # constant attribute
        self.side = side  # "w" or "b"
        self.pieceType = pieceType  # "r", "n", "b", "q", "k" or "p"
        self.image = pygame.transform.smoothscale(pygame.image.load("Assets/piece/" + side + pieceType + ".png").convert_alpha(), (PIECE_WIDTH, PIECE_HEIGHT))

        # variable attribute
        self.coord = coord  # (0,0), (3,4), (7,7), ...
        self.movedStep = 0  # 1, 2, 3, 4, ...
        self.viableMove = self.get_viableMove()  # [(0,0), (1,1), (4,7), (7,7), ...]
        self.rect = self.image.get_rect(center=coord2Pos(coord))

    def get_viableMove(self):
        """take in self instance, return a list of viable moves"""
        """self instance-> a list of tuples contaning coordinates """
        
        if self.pieceType == "r":
            return self.get_viableMove_rook()
        if self.pieceType == "n":
            return self.get_viableMove_knight()
        if self.pieceType == "b":
            return self.get_viableMove_bishop()
        if self.pieceType == "q":
            return self.get_viableMove_queen()
        if self.pieceType == "k":
            return self.get_viableMove_king()
        if self.pieceType == "p":
            return self.get_viableMove_pawn()

    def get_viableMove_rook(self):
        """take self instance as input, return a list of tuple of viable move of rook"""
        occupied_coord = [piece.coord for piece in ALIVE_PIECES if piece.coord != self.coord]
        viableMove = []
        # tuple is not mutable, use list instead
        up_obst, down_obst, left_obst, right_obst = list(self.coord), list(self.coord), list(self.coord), list(self.coord)
        # finding obstacle's coordinates
        while True:
            if tuple(up_obst) in occupied_coord or up_obst[1] <= 0:
                break
            up_obst[1] -= 1
            viableMove.append(tuple(up_obst)) # append viable move

        while True:
            if tuple(down_obst) in occupied_coord or down_obst[1] >= 7:
                break
            down_obst[1] += 1
            viableMove.append(tuple(down_obst))

        while True:
            if tuple(left_obst) in occupied_coord or left_obst[0] <= 0:
                break
            left_obst[0] -= 1
            viableMove.append(tuple(left_obst))

        while True:
            if tuple(right_obst) in occupied_coord or right_obst[0] >= 7:
                break
            right_obst[0] += 1
            viableMove.append(tuple(right_obst))

        # delete the intersection of two set, remove all the viableMove that will capture allies piece
        allies_coord = [piece.coord for piece in ALIVE_PIECES if (piece.side == self.side and piece.coord != self.coord)]
        viableMove = list(set(viableMove) - set(allies_coord))

        return viableMove

    def get_viableMove_knight(self):
        
        a = (self.coord[0] - 1, self.coord[1] - 2)
        b = (self.coord[0] + 1, self.coord[1] - 2)
        c = (self.coord[0] + 2, self.coord[1] + 1)
        d = (self.coord[0] + 2, self.coord[1] - 1)
        e = (self.coord[0] + 1, self.coord[1] + 2)
        f = (self.coord[0] - 1, self.coord[1] + 2)
        g = (self.coord[0] - 2, self.coord[1] + 1)
        h = (self.coord[0] - 2, self.coord[1] - 1)

        viableMove = [a, b, c, d, e, f, g, h]
        
        # delete out of bound move
        for move in viableMove[:]: # make a copy of viableMove list to avoid unexpected behaviour
            if move[0] < 0 or move[0] > 7 or move[1] < 0 or move[1] > 7: # 7 is max coord
                viableMove.remove(move)

        # delete move that will capture allies piece
        allies_coord = [piece.coord for piece in ALIVE_PIECES if (piece.side == self.side and piece.coord != self.coord)]
        viableMove = list(set(viableMove) - set(allies_coord))
        
        return viableMove

    def get_viableMove_bishop(self):
        occupied_coord = [piece.coord for piece in ALIVE_PIECES if piece.coord != self.coord]
        
        viableMove = []
        # tuple is not mutable, use list instead
        topleft_obst, topright_obst, botleft_obst, botright_obst = list(self.coord), list(self.coord), list(self.coord), list(self.coord)
        # finding obstacle's coordinates
        while True:
            if tuple(topleft_obst) in occupied_coord or topleft_obst[0] <= 0 or topleft_obst[1] <= 0:
                break
            topleft_obst[0] -= 1
            topleft_obst[1] -= 1
            viableMove.append(tuple(topleft_obst)) #append viable move

        while True:
            if tuple(topright_obst) in occupied_coord or topright_obst[0] >= 7 or topright_obst[1] <= 0:
                break
            topright_obst[0] += 1
            topright_obst[1] -= 1

            viableMove.append(tuple(topright_obst))

        while True:
            if tuple(botleft_obst) in occupied_coord or botleft_obst[0] <= 0 or botleft_obst[1] >= 7:
                break
            botleft_obst[0] -= 1
            botleft_obst[1] += 1

            viableMove.append(tuple(botleft_obst))

        while True:
            if tuple(botright_obst) in occupied_coord or botright_obst[0] >= 7 or botright_obst[1] >= 7:
                break
            botright_obst[0] += 1
            botright_obst[1] += 1
            viableMove.append(tuple(botright_obst))

        # delete the intersection of two set, remove all the viableMove that will capture allies piece
        allies_coord = [piece.coord for piece in ALIVE_PIECES if (piece.side == self.side and piece.coord != self.coord)]
        viableMove = list(set(viableMove) - set(allies_coord))

        return viableMove

    def get_viableMove_queen(self):
        # queen's viable moves is just rook plus bishop
        return self.get_viableMove_bishop() + self.get_viableMove_rook()

    def get_viableMove_king(self):
        a = (self.coord[0] - 1, self.coord[1] - 1) #top left, cw
        b = (self.coord[0]    , self.coord[1] - 1) #top
        c = (self.coord[0] + 1, self.coord[1] - 1) #topright
        d = (self.coord[0] + 1, self.coord[1]    ) #right
        e = (self.coord[0] + 1, self.coord[1] + 1) #botright
        f = (self.coord[0]    , self.coord[1] + 1) #bot
        g = (self.coord[0] - 1, self.coord[1] + 1) #botleft
        h = (self.coord[0] - 1, self.coord[1]    ) #left

        viableMove = [a, b, c, d, e, f, g, h]
        # delete out of bound move
        for move in viableMove[:]: # make a copy of viableMove list to avoid unexpected behaviour
            if move[0] < 0 or move[0] > 7 or move[1] < 0 or move[1] > 7: # 7 is max coord
                viableMove.remove(move)

        # delete move that will capture allies piece
        allies_coord = [piece.coord for piece in ALIVE_PIECES if (piece.side == self.side and piece.coord != self.coord)]
        viableMove = list(set(viableMove) - set(allies_coord))
        
        return viableMove

    def get_viableMove_pawn(self):
        if self.side == "b":
            if self.movedStep == 0:
                viableMove = [(self.coord[0], self.coord[1] + 1), (self.coord[0], self.coord[1] + 2)]
                return viableMove
            elif self.coord[1] != 7: # movedStep > 0 and piece not in other end of board
                viableMove = [(self.coord[0], self.coord[1] + 1)]
                return viableMove
            else: return []

        else: # side == "w"
            if self.movedStep == 0:
                viableMove = [(self.coord[0], self.coord[1] - 1), (self.coord[0], self.coord[1] - 2)]
                return viableMove
            elif self.coord[1] != 0: # movedstep > 0 and piece not in other end of board
                viableMove = [(self.coord[0], self.coord[1] - 1)]
                return viableMove
            else: return []
                
    def update_piece(self, ori_coord):
        """take in self instance, update all the attributes if a move is made, no return"""
        dest_coord = get_closestCoord(pygame.mouse.get_pos())
        # update viable move no matter moved or not to show hint dots correctly
        self.viableMove = self.get_viableMove()

        # check if the piece moved or not
        if self.coord == dest_coord:
            # reset the piece's rect position if no move is made
            self.rect.center = coord2Pos(dest_coord)
            return

        # check move is in list of viableMove:
        elif dest_coord not in self.viableMove:
            self.coord = ori_coord
            self.rect.center = coord2Pos(ori_coord)
            return

        # valid move to other position
        else:
            #select dest object
            captureMoveCoord = [move for move in self.viableMove if move in [piece.coord for piece in ALIVE_PIECES]]
            if dest_coord in captureMoveCoord:

                dest_piece = None
                for piece in ALIVE_PIECES:
                    if piece.coord == dest_coord:
                        dest_piece = piece
                        break
                
                ALIVE_PIECES.remove(dest_piece)
                dest_piece.kill()
                del dest_piece
                

            self.coord = dest_coord
            self.rect.center = coord2Pos(dest_coord)
            self.movedStep += 1
    

def coord2Pos(coord):
    """convert coordinate to pixel position e.g.(1,2) -> (150,250)"""
    """1 tuple of coordinate -> 1 tuple of pixel postition"""
    xPos = PIECE_WIDTH//2 + coord[0] * PIECE_WIDTH
    yPos = PIECE_HEIGHT//2 + coord[1] * PIECE_HEIGHT
    return (xPos, yPos)


def get_closestCoord(mousePos):
    """get the x, y coordinate of square with that is closest to cursor"""
    """self, mouse position -> a tuple containing coordinates"""
    mx, my = mousePos
    # create a 2D list of tuple, each tuple contain coordinates of valid position
    VALID_POS = [[coord2Pos((x, y)) for x in range(BOARD_LENGTH)] for y in range(BOARD_LENGTH)]
    # create a 2D list of float, each float is distance from the mouse position
    dist = [[sqrt((pos[0]-mx)**2 + (pos[1]-my)**2) for pos in row] for row in VALID_POS]

    # get the x, y coordinate of square with that is closest to cursor
    dist_rowsums = [sum(row) for row in dist]
    y = dist_rowsums.index(min(dist_rowsums))
    x = dist[y].index(min(dist[y]))

    return (x, y)


def get_selected_piece(coord):
    """return the piece instance if cursor sit on a square that contain a piece, otherwise return None(empty square)"""
    for piece in ALIVE_PIECES:
        if piece.coord == coord:
            return piece
    return None


def create_pieces():
    """Loop through the BOARD and create a instance for each piece encounter and append ALIVE_PIECES"""
    for y, rows in enumerate(CHESSBOARD_INIT):
        for x, sq in enumerate(rows):  # sq: "wp", "bk" etc.
            if sq != "o":  # square is not open
                side = sq[0]
                pieceType = sq[1]
                ALIVE_PIECES.append(Piece(side, pieceType, (x, y)))  # init Piece instance with with side, pieceType, coord


def addPieces2Group():
    """add all pieces in ALIVE_PIECE to sprite group"""
    for piece in ALIVE_PIECES:
        PIECE_GROUP.add(piece)


def draw_hint_dots(surf, slt_piece):
    """Draw hint dots on viable move position of selected piece"""
    # check selected piece exists
    if slt_piece is None:
        return
    for coord in slt_piece.viableMove:
        pygame.draw.circle(surf, (150, 150, 150), coord2Pos(coord), 30)


def main():
    # initialize pygame
    pygame.init()
    clock = pygame.time.Clock()

    # initialize display window
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    chessboard = pygame.transform.smoothscale(pygame.image.load("Assets/cb_blue.png").convert_alpha(), (WIDTH, HEIGHT))

    # create pieces and add to sprite group
    create_pieces()
    addPieces2Group()

    SLT_PIECE = None
    SLT_PIECE_ORICOORD = (0, 0)
    # game Loop
    while True:
        for event in pygame.event.get():
            # exit game
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouseCoord = get_closestCoord(pygame.mouse.get_pos())
                # get the selected piece instance if it exists
                SLT_PIECE = get_selected_piece(mouseCoord)

                # record the selected piece coordinate if it exists
                if SLT_PIECE is not None:
                    SLT_PIECE.update_piece(SLT_PIECE_ORICOORD)
                    SLT_PIECE_ORICOORD = mouseCoord
                else:
                    SLT_PIECE_ORICOORD = None

            elif event.type == pygame.MOUSEBUTTONUP:
                if SLT_PIECE is not None:
                    # update the piece attributes after a piece is dropped
                    SLT_PIECE.update_piece(SLT_PIECE_ORICOORD)
                SLT_PIECE = None  # reset

        # drag the selected piece
        if SLT_PIECE is not None:
            SLT_PIECE.rect.center = pygame.mouse.get_pos()

        # drawing, wrong order may cause some surfaces being blocked
        window.blit(chessboard, (0, 0))
        draw_hint_dots(window, SLT_PIECE)  # draw hint dots
        PIECE_GROUP.draw(window)
        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
