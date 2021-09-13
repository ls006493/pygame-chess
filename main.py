import pygame
from sys import exit
from math import sqrt

# GLOBAL CONSTANT
FPS = 120  # if fps too low the game will lose track of mouse movement
# screen
WIDTH = 800
HEIGHT = 800
# piece
PIECE_WIDTH = 100
PIECE_HEIGHT = 100
# initial chess board
PIECE_DICT = {
    "r": "b_Rook",
    "n": "b_Knight",
    "b": "b_Bishop",
    "q": "b_Queen",
    "k": "b_King",
    "p": "b_Pawn",

    "R": "w_Rook",
    "N": "w_Knight",
    "B": "w_Bishop",
    "Q": "w_Queen",
    "K": "w_King",
    "P": "w_Pawn"
}

BOARD = [
    ["r", "n", "b", "q", "k", "b", "n", "r"],
    ["p", "p", "p", "p", "p", "p", "p", "p"],
    ["o", "o", "o", "o", "o", "o", "o", "o"],
    ["o", "o", "o", "o", "o", "o", "o", "o"],
    ["o", "o", "o", "o", "o", "o", "o", "o"],
    ["o", "o", "o", "o", "o", "o", "o", "o"],
    ["P", "P", "P", "P", "P", "P", "P", "P"],
    ["R", "N", "B", "Q", "K", "B", "N", "R"]
]

VALID_POS = []
for i in range(len(BOARD)):  # 8*8
    temp = []
    for j in range(len(BOARD)):
        temp.append((PIECE_WIDTH//2 + j * PIECE_WIDTH, PIECE_HEIGHT//2 + i * PIECE_HEIGHT))
    VALID_POS.append(temp)

# GLOBAL VARIABLE
ALIVE_PIECES = []  # list of alive piece objects
SELECTED_PIECE = None  # selected piece instance
SELECTED_PIECE_ORICOORD = (0, 0)  # original position of drag piece


class Piece(pygame.sprite.Sprite):

    def __init__(self, side, pieceType, coord):
        super().__init__()
        self.side = side
        self.pieceType = pieceType
        self.coord = coord
        self.image = pygame.transform.smoothscale(pygame.image.load("Assets/piece/" + side + pieceType + ".png").convert_alpha(), (PIECE_WIDTH, PIECE_HEIGHT))
        self.rect = self.image.get_rect(center=(PIECE_WIDTH//2 + coord[0] * PIECE_WIDTH, PIECE_HEIGHT//2 + coord[1] * PIECE_HEIGHT))
        self.movedStep = 0

    @classmethod
    def select_piece(cls, event):
        """return selected piece instance, if no piece is selected return none"""
        mx, my = pygame.mouse.get_pos()
        for piece in ALIVE_PIECES:
            if piece.rect.x <= mx <= piece.rect.x + PIECE_WIDTH and piece.rect.y <= my <= piece.rect.y + PIECE_HEIGHT:
                return piece
        return None

    @classmethod
    def get_spot_coord(cls):
        """return a tuple of position of the closest valid spot that the selected piece has been dragged to"""
        """if the spot is occupied, return SELECTED_PIECE_ORICOORD"""
        global SELECTED_PIECE_ORICOORD
        mx, my = pygame.mouse.get_pos()

        distances = []
        for rows in VALID_POS:
            temp = []
            for pos in rows:
                temp.append(sqrt((pos[0]-mx)**2 + (pos[1]-my)**2))
            distances.append(temp)

        dest_xpos = min(distances[0])
        dest_xcoord = distances[0].index(dest_xpos)

        y_list = [rows[dest_xcoord] for rows in distances]
        dest_ypos = min(y_list)
        dest_ycoord = y_list.index(dest_ypos)

        # check no piece already in that spot to avoid overlapping
        pieces_pos = [piece.rect.center for piece in ALIVE_PIECES]
        if SELECTED_PIECE.isValidMove(dest_xcoord, dest_ycoord) and (VALID_POS[dest_ycoord][dest_xcoord] not in pieces_pos or SELECTED_PIECE.allowCapture(dest_xcoord, dest_ycoord)):
            # if move is valid, and spot is empty or capture is allowed
            SELECTED_PIECE.coord = (dest_xcoord, dest_ycoord)
            return (dest_xcoord, dest_ycoord)
        else:
            # not valid move, or allied piece is captured
            return SELECTED_PIECE_ORICOORD

    def allowCapture(self, dest_xcoord, dest_ycoord):
        dest_side = ""
        for piece in ALIVE_PIECES:

            if piece.coord == (dest_xcoord, dest_ycoord) and piece != SELECTED_PIECE:
                dest_side = piece.side

                if self.side != dest_side:
                    ALIVE_PIECES.remove(piece)  # remove from list
                    piece.kill()  # remove from all group
                    del piece  # delete instance
                    return True

        return False

    def isValidMove(self, dest_xcoord, dest_ycoord):

        if self.pieceType == "Rook":
            return self.validate_rook(dest_xcoord, dest_ycoord)
        if self.pieceType == "Knight":
            return self.validate_knight(dest_xcoord, dest_ycoord)
        if self.pieceType == "Bishop":
            return self.validate_bishop(dest_xcoord, dest_ycoord)
        if self.pieceType == "Queen":
            return self.validate_queen(dest_xcoord, dest_ycoord)
        if self.pieceType == "King":
            return self.validate_king(dest_xcoord, dest_ycoord)
        if self.pieceType == "Pawn":
            return self.validate_pawn(dest_xcoord, dest_ycoord)

    def validate_rook(self, dest_xcoord, dest_ycoord):
        if dest_xcoord == self.coord[0] or dest_ycoord == self.coord[1]:
            if not self.haveObstacle(dest_xcoord, dest_ycoord):
                return True
        return False

    def validate_knight(self, dest_xcoord, dest_ycoord):
        valid_move_list = []

        a = (self.coord[0] + 1, self.coord[1] + 2)  # up
        b = (self.coord[0] - 1, self.coord[1] + 2)

        c = (self.coord[0] + 2, self.coord[1] + 1)  # right
        d = (self.coord[0] + 2, self.coord[1] - 1)

        e = (self.coord[0] - 2, self.coord[1] + 1)  # left
        f = (self.coord[0] - 2, self.coord[1] - 1)

        g = (self.coord[0] + 1, self.coord[1] - 2)  # down
        h = (self.coord[0] - 1, self.coord[1] - 2)

        op_list = [a, b, c, d, e, f, g, h]

        for op in op_list:
            if min(op) >= 0 and max(op) <= len(BOARD):
                valid_move_list.append(op)

        if (dest_xcoord, dest_ycoord) in valid_move_list:
            return True

        return False

    def validate_bishop(self, dest_xcoord, dest_ycoord):
        valid_move_list = []
        for i in range(len(BOARD)):
            a = (self.coord[0] + i, self.coord[1] + i)
            b = (self.coord[0] + i, self.coord[1] - i)
            c = (self.coord[0] - i, self.coord[1] + i)
            d = (self.coord[0] - i, self.coord[1] - i)

            op_list = [a, b, c, d]

            for op in op_list:
                if min(op) >= 0 and max(op) <= len(BOARD):
                    valid_move_list.append(op)

        if (dest_xcoord, dest_ycoord) in valid_move_list:
            if not self.haveObstacle(dest_xcoord, dest_ycoord):
                return True

        return False

    def validate_queen(self, dest_xcoord, dest_ycoord):
        if self.validate_rook(dest_xcoord, dest_ycoord) or self.validate_bishop(dest_xcoord, dest_ycoord):
            if not self.haveObstacle(dest_xcoord, dest_ycoord):
                return True
        return False

    def validate_king(self, dest_xcoord, dest_ycoord):
        valid_move_list = []

        a = (self.coord[0] - 1, self.coord[1] - 1)  # top left, ccw
        b = (self.coord[0], self.coord[1] + 1)

        c = (self.coord[0] + 1, self.coord[1] + 1)  
        d = (self.coord[0] + 1, self.coord[1] )

        e = (self.coord[0] + 1, self.coord[1] - 1)  
        f = (self.coord[0], self.coord[1] - 1)

        g = (self.coord[0] - 1, self.coord[1] + 1)  
        h = (self.coord[0] - 1, self.coord[1])

        op_list = [a, b, c, d, e, f, g, h]

        for op in op_list:
            if min(op) >= 0 and max(op) <= len(BOARD):
                valid_move_list.append(op)

        if (dest_xcoord, dest_ycoord) in valid_move_list:
            return True

        return False

    def validate_pawn(self, dest_xcoord, dest_ycoord):
        if self.side == "b":
            if self.movedStep == 0:
                # First step of black pawn can move 1 or 2 stpe forward
                if (dest_ycoord == self.coord[1] + 2 or dest_ycoord == self.coord[1] + 1) and dest_xcoord == self.coord[0]:
                    return True

            else:
                # after first step
                if dest_ycoord == self.coord[1] + 1 and dest_xcoord == self.coord[0]:
                    return True

        else:  # self.side == "w"
            if self.movedStep == 0:
                # First step of white pawn can move 1 or 2 stpe forward
                if (dest_ycoord == self.coord[1] - 2 or dest_ycoord == self.coord[1] - 1) and dest_xcoord == self.coord[0]:
                    return True

            else:
                # after first step
                if dest_ycoord == self.coord[1] - 1 and dest_xcoord == self.coord[0]:
                    return True
        return False

    def haveObstacle(self, dest_xcoord, dest_ycoord):
        # check for queen, bishop and rook 
        if self.pieceType == "Rook":
            dest_coord = (dest_xcoord, dest_ycoord)
            index = 0 # x is changing index -> 0, y is changing index -> 1
            if dest_xcoord == self.coord[0]:
                index = 1 # y coord is changing
            else: 
                index = 0 # x coord is changing
            increment = 1 if self.coord[index] < dest_coord[index] else -1
            print(self.coord[index], dest_coord[index], increment)
            for i in range(self.coord[index], dest_coord[index], increment):
                obst_ccoord = (self.coord[0], i) if index == 1 else (i, self.coord[1])
                for piece in ALIVE_PIECES:
                    if piece.coord == (obst_ccoord) and piece != SELECTED_PIECE:
                        return True

            return False

        if self.pieceType == "Bishop":
            pass
            

    def enPassant():
        pass


def create_pieces():
    """Loop through the BOARD and create a instance for each piece encounter and append ALIVE_PIECES"""
    for y, rows in enumerate(BOARD):
        for x, square in enumerate(rows):  # square: "r", "Q", "q", "K" etc
            if square != "o":  # square not empty
                side = PIECE_DICT[square].split("_")[0]
                pieceType = PIECE_DICT[square].split("_")[1]
                ALIVE_PIECES.append(Piece(side, pieceType, (x, y)))


def main():
    # initialize pygame and clock
    pygame.init()
    clock = pygame.time.Clock()

    # initialize screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen_surf = pygame.transform.smoothscale(pygame.image.load("Assets/chessboard_grey.png").convert_alpha(), (WIDTH, HEIGHT))

    # create a list containing piece instances
    create_pieces()

    # add piece instances to a group
    piece_group = pygame.sprite.Group()
    for piece in ALIVE_PIECES:
        piece_group.add(piece)

    global SELECTED_PIECE  # allow main function to modify the global variable
    global SELECTED_PIECE_ORICOORD
    # game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()  # if windows closed, exit programme

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # get the instance and update original position of the instance when mouse button is down
                SELECTED_PIECE = Piece.select_piece(event)
                if SELECTED_PIECE is not None:
                    SELECTED_PIECE_ORICOORD = (SELECTED_PIECE.coord[0], SELECTED_PIECE.coord[1])  # center position

            elif event.type == pygame.MOUSEBUTTONUP:
                # set the position of selected rectangle and reset selected instance to none when mousebutton is up
                if SELECTED_PIECE is not None:
                    coord = Piece.get_spot_coord()
                    SELECTED_PIECE.rect.center = VALID_POS[coord[1]][coord[0]]

                    if coord != SELECTED_PIECE_ORICOORD:  # make sure the piece made a move
                        SELECTED_PIECE.movedStep += 1

                SELECTED_PIECE = None

        # drag the selected piece with mouse movement
        if SELECTED_PIECE is not None:
            SELECTED_PIECE.rect.center = pygame.mouse.get_pos()

        # Order matter! The newly drawn screen will cover the old screen and sprite
        screen.blit(screen_surf, (0, 0))
        piece_group.draw(screen)
        pygame.display.update()

        clock.tick(FPS)


if __name__ == "__main__":
    main()
