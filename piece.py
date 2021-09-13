import main
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
            return True

        return False

    def validate_queen(self, dest_xcoord, dest_ycoord):
        if self.validate_rook(dest_xcoord, dest_ycoord) or self.validate_bishop(dest_xcoord, dest_ycoord):
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