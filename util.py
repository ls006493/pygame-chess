from math import sqrt
import cfg
import pygame


def coord2Pos(coord):
    """convert coordinate to pixel position e.g.(1,2) -> (150,250)"""
    """1 tuple of coordinate -> 1 tuple of pixel postition"""
    xPos = cfg.PIECE_WIDTH//2 + coord[0] * cfg.PIECE_WIDTH
    yPos = cfg.PIECE_HEIGHT//2 + coord[1] * cfg.PIECE_HEIGHT
    return (xPos, yPos)


def get_closestCoord(mousePos):
    """get the x, y coordinate of square with that is closest to cursor"""
    """self, mouse position -> a tuple containing coordinates"""
    mx, my = mousePos
    # create a 2D list of tuple, each tuple contain coordinates of valid position
    VALID_POS = [[coord2Pos((x, y)) for x in range(cfg.BOARD_LENGTH)] for y in range(cfg.BOARD_LENGTH)]
    # create a 2D list of float, each float is distance from the mouse position
    dist = [[sqrt((pos[0]-mx)**2 + (pos[1]-my)**2) for pos in row] for row in VALID_POS]

    # get the x, y coordinate of square with that is closest to cursor
    dist_rowsums = [sum(row) for row in dist]
    y = dist_rowsums.index(min(dist_rowsums))
    x = dist[y].index(min(dist[y]))

    return (x, y)


def get_selected_piece(coord):
    """return the piece instance if cursor sit on a square that contain a piece, otherwise return None(empty square)"""
    for piece in cfg.ALIVE_PIECES:
        if piece.coord == coord:
            return piece
    return None


def draw_hint_dots(surf, slt_piece):
    """Draw hint dots on viable move position of selected piece"""
    # check selected piece exists
    if slt_piece is not None:

        for coord in slt_piece.viableMove:
            radius = 30
            circle = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
            pygame.draw.circle(circle, (150, 150, 150, 128), coord2Pos(coord), radius)
            surf.blit(circle, (500, 500))
