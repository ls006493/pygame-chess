# pygame chess
#### Video Demo: https://www.youtube.com/watch?v=Nl75Isa16dk
#### Description: A chess game made using pygame framework. This game allow player to practice their chess skills. Player will play both white side and black side of the chess game.

#### How to play the game: Use mouse left click to drag the piece you desired to move, release left click to drop pieces to square on the chessboard, the game will predict the square the player wanted to place his/her piece. When player want to restart the game, press the restart button located on the bottom left corner.

#### Feature: fullly Graphical user interface, sound effect, intro screen, piece move restriction, grey dots to indicate viable move of piece when dragging,winning detection, restart game function

#### Limitation: en passant, pawn promotion selection, castle, stalemate/ checkmate detection
#### These special moves for chess game is not implemented because they are quite complex and may need to change the structure of the game for that to work. Despite some special moves is not available, pawn still can do diagonal capture and double push in first move. 

#### customization: player can change the chessboard game into puzzle solving by changing CHESSBOARD_INIT in cfg.py, "o" represent empty square, "b"/"w" in first character represent side, "p","b","n","k","q","r" in second character represent the type of the piece. The chessboard is represented by a 2D list. You can modify the list to initialize the chessboard into different puzzles. 

#### Besides, player can also change the theme of the chessboard, goto chess.py and change the line: chessboard = pygame.transform.smoothscale(pygame.image.load("Assets/cb_blue.png").convert_alpha(), (cfg.WIDTH, cfg.HEIGHT)), change "cb_blue.png" to "cb_brown.png" or "cb_green.png" or "cb_grey.png" or "cb_pink.png" to have different chessboard color theme.


#### Future work: When player made a move it is possible to convert them into standard chess move notation and communicate with a chess engine through API and get the next move of the engine. Then player can play with a bot the enhance their skill.
#### The chess game can also implement a save/ loading function to allow player to export/ import chess game easily, or allow player to save the game and continune to play after closing and re-opening the game.

#### Assets: except the chessboard image all other assets are downloaded from internet and I do not own them

#### version: pygame 2.0.1 python 3.9.7