import pygame
import cfg
from util import get_closestCoord, get_selected_piece, coord2Pos

class Piece(pygame.sprite.Sprite):
    def __init__(self, side, pieceType, coord):
        super().__init__()
        # constant attribute
        self.side = side  # "w" or "b"
        self.pieceType = pieceType  # "r", "n", "b", "q", "k" or "p"
        self.image = pygame.transform.smoothscale(pygame.image.load("Assets/piece/" + side + pieceType + ".png").convert_alpha(), (cfg.PIECE_WIDTH, cfg.PIECE_HEIGHT))

        # variable attribute
        self.coord = coord  # (0,0), (3,4), (7,7), ...
        self.movedStep = 0  # 1, 2, 3, 4, ...
        self.viableMove = self.get_viableMove()  # [(0,0), (1,1), (4,7), (7,7), ...]
        self.rect = self.image.get_rect(center=coord2Pos(coord))

    def check_equal(self, other):
        if not isinstance(other, Piece):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.side == other.side and self.pieceType == other.pieceType \
            and self.coord == other.coord and self.movedStep == other.movedStep \
            and self.viableMove == other.viableMove

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
        occupied_coord = [piece.coord for piece in cfg.ALIVE_PIECES if piece.coord != self.coord]
        viableMove = []
        # tuple is not mutable, use list instead
        up_obst, down_obst, left_obst, right_obst = list(self.coord), list(self.coord), list(self.coord), list(self.coord)
        # finding obstacle's coordinates
        while True:
            if tuple(up_obst) in occupied_coord or up_obst[1] <= 0:
                break
            up_obst[1] -= 1
            viableMove.append(tuple(up_obst))  # append viable move

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
        allies_coord = [piece.coord for piece in cfg.ALIVE_PIECES if (piece.side == self.side and piece.coord != self.coord)]
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
        for move in viableMove[:]:  # make a copy of viableMove list to avoid unexpected behaviour
            if move[0] < 0 or move[0] > 7 or move[1] < 0 or move[1] > 7:  # 7 is max coord
                viableMove.remove(move)

        # delete move that will capture allies piece
        allies_coord = [piece.coord for piece in cfg.ALIVE_PIECES if (piece.side == self.side and piece.coord != self.coord)]
        viableMove = list(set(viableMove) - set(allies_coord))

        return viableMove

    def get_viableMove_bishop(self):
        occupied_coord = [piece.coord for piece in cfg.ALIVE_PIECES if piece.coord != self.coord]

        viableMove = []
        # tuple is not mutable, use list instead
        topleft_obst, topright_obst, botleft_obst, botright_obst = list(self.coord), list(self.coord), list(self.coord), list(self.coord)
        # finding obstacle's coordinates
        while True:
            if tuple(topleft_obst) in occupied_coord or topleft_obst[0] <= 0 or topleft_obst[1] <= 0:
                break
            topleft_obst[0] -= 1
            topleft_obst[1] -= 1
            viableMove.append(tuple(topleft_obst))  # append viable move

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
        allies_coord = [piece.coord for piece in cfg.ALIVE_PIECES if (piece.side == self.side and piece.coord != self.coord)]
        viableMove = list(set(viableMove) - set(allies_coord))

        return viableMove

    def get_viableMove_queen(self):
        # queen's viable moves is just rook plus bishop
        return self.get_viableMove_bishop() + self.get_viableMove_rook()

    def get_viableMove_king(self):
        a = (self.coord[0] - 1, self.coord[1] - 1)  # top left, cw
        b = (self.coord[0], self.coord[1] - 1)  # top
        c = (self.coord[0] + 1, self.coord[1] - 1)  # topright
        d = (self.coord[0] + 1, self.coord[1])  # right
        e = (self.coord[0] + 1, self.coord[1] + 1)  # botright
        f = (self.coord[0], self.coord[1] + 1)  # bot
        g = (self.coord[0] - 1, self.coord[1] + 1)  # botleft
        h = (self.coord[0] - 1, self.coord[1])  # left

        viableMove = [a, b, c, d, e, f, g, h]
        # delete out of bound move
        for move in viableMove[:]:  # make a copy of viableMove list to avoid unexpected behaviour
            if move[0] < 0 or move[0] > 7 or move[1] < 0 or move[1] > 7:  # 7 is max coord
                viableMove.remove(move)

        # delete move that will capture allies piece
        allies_coord = [piece.coord for piece in cfg.ALIVE_PIECES if (piece.side == self.side and piece.coord != self.coord)]
        viableMove = list(set(viableMove) - set(allies_coord))

        return viableMove

    def get_viableMove_pawn(self):
        if self.side == "b":
            viableMove = []
            alive_pieces = [piece.coord for piece in cfg.ALIVE_PIECES]
            enermy_pieces = [piece.coord for piece in cfg.ALIVE_PIECES if piece.side == "w"]

            # diagonal capture
            if (self.coord[0] - 1, self.coord[1] + 1) in enermy_pieces:
                viableMove.append((self.coord[0] - 1, self.coord[1] + 1))
            if (self.coord[0] + 1, self.coord[1] + 1) in enermy_pieces:
                viableMove.append((self.coord[0] + 1, self.coord[1] + 1))

            # first move
            if self.movedStep == 0 and (self.coord[0], self.coord[1] + 1) not in alive_pieces and (self.coord[0], self.coord[1] + 2) not in alive_pieces:
                viableMove.append((self.coord[0], self.coord[1] + 2))

            # regular move
            if self.coord[1] != 7 and (self.coord[0], self.coord[1] + 1) not in alive_pieces:
                viableMove.append((self.coord[0], self.coord[1] + 1))

            return viableMove

        else:  # side == "w"
            viableMove = []
            alive_pieces = [piece.coord for piece in cfg.ALIVE_PIECES]
            enermy_pieces = [piece.coord for piece in cfg.ALIVE_PIECES if piece.side == "b"]

            # diagonal capture
            if (self.coord[0] - 1, self.coord[1] - 1) in enermy_pieces:
                viableMove.append((self.coord[0] - 1, self.coord[1] - 1))
            if (self.coord[0] + 1, self.coord[1] - 1) in enermy_pieces:
                viableMove.append((self.coord[0] + 1, self.coord[1] - 1))

            # first move
            if self.movedStep == 0 and (self.coord[0], self.coord[1] - 1) not in alive_pieces and (self.coord[0], self.coord[1] - 2) not in alive_pieces:
                viableMove.append((self.coord[0], self.coord[1] - 2))

            # regular move
            if self.coord[1] != 0 and (self.coord[0], self.coord[1] - 1) not in alive_pieces:
                viableMove.append((self.coord[0], self.coord[1] - 1))

            return viableMove

    def isPawnPromotion(self, dest_coord):
        if self.pieceType == "p":
            if dest_coord[1] == 0 and self.side == "w":
                return True
            if dest_coord[1] == 7 and self.side == "b":
                return True
        return False

    def pawnPromote(self):
        self.pieceType = "q"
        if self.side == "w":
            self.image = pygame.transform.smoothscale(pygame.image.load("Assets/piece/wq.png").convert_alpha(), (cfg.PIECE_WIDTH, cfg.PIECE_HEIGHT))
        else:
            self.image = pygame.transform.smoothscale(pygame.image.load("Assets/piece/bq.png").convert_alpha(), (cfg.PIECE_WIDTH, cfg.PIECE_HEIGHT))
        self.rect = self.image.get_rect(center=coord2Pos(self.coord))

    def update_piece(self, ori_coord, move_soundeffect):
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
        elif dest_coord not in self.viableMove or self.side != cfg.TURN:
            self.coord = ori_coord
            self.rect.center = coord2Pos(ori_coord)
            return

        # valid move
        else:
            # pawn promotion
            if self.isPawnPromotion(dest_coord):
                self.pawnPromote()

            # capture
            dest_piece = next((piece for piece in cfg.ALIVE_PIECES if piece.coord == dest_coord), None)
            if dest_piece is not None:
                cfg.ALIVE_PIECES.remove(dest_piece)
                dest_piece.kill()
                del dest_piece

            # update self attribute after sucessful move
            self.coord = dest_coord
            self.rect.center = coord2Pos(dest_coord)
            self.movedStep += 1

            # play sound effect after valid move
            pygame.mixer.Sound.play(move_soundeffect)

            cfg.TURN = "b" if cfg.TURN == "w" else "w"