import pygame
# GLOBAL CONSTANT
WIDTH, HEIGHT = 800, 800
UI_WIDTH = 400
PIECE_WIDTH, PIECE_HEIGHT = 100, 100
BOARD_LENGTH = 8
FPS = 60

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

CHESSBOARD_INIT3 = [
    ["br",  "o",  "o",  "o",  "bk",  "o",  "o",  "br"],
    ["o",  "o",  "o",  "o",  "o",  "o",  "o",  "o"],
    ["o",  "o",  "o",  "o",  "o",  "o",  "o",  "o"],
    ["o",  "o",  "o",  "o",  "o",  "o",  "o",  "o"],
    ["o",  "o",  "o",  "o",  "o",  "o",  "o",  "o"],
    ["o",  "o",  "o",  "o",  "o",  "o",  "o",  "o"],
    ["o",  "o",  "o",  "o",  "o",  "o",  "o",  "o"],
    ["wr",  "o",  "o",  "o",  "wk",  "o",  "o",  "wr"]
]

# Global variables
INTRO = True
ALIVE_PIECES = []  # list of alive piece instances
PIECE_GROUP = pygame.sprite.Group()  # piece sprite group
TURN = "w"
RESTART = False
RESTART_TIME = 0
CHECKED = False