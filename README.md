# Chess_Game_Tracker
Track Chess Games with Computer Vision
A Cam (Panasonic DV NV55)connected to a Nvidia Jetson NX mini computer, Python, OpenCV and Numpy, python-chess and Stockfish were used in this program. 

The Chess set was a wooden Chess board with colored pieces. A DGT3000 Chess clock was modifed with a HAL Sensor and a debounce circuit. Each time the lever was pressed a keystroke "p"  was sent to the mini computer via USB to signalize when a move was done.

The Chessboard was identified by a method described by Murat Sahin 2023 (1) using a cascade of Canny Edge Detection and Hough lines. 
The board image was  warped to a square of 800x800 pixels.

At game start the chess position is described by FEN (Forsyte Edwards Notation). Moves  are described their by origin and destination Square (given in UCI notation).

At games start FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

This FEN string can be converted to an image using fen-to-png Toby Adewoye 2019 (2) and displayed.

Color filters for Black and White pieces and background mask were applied to images taken before and after each move.
Pieces were identified using the open CV contours() function with area threshold. Pieces were than located with bounding boxes. Coordinates of the bounding boxes were used 
to identify the name of the squares with pieces on (a1 ....h8).

These squarenames were stored in sets. Four sets were obtained for each move:

set of squares with white pieces before a move
set of squares with black pieces before a move
set of squares with white pieces after a move
set of squares with black pieces after a move

The move can than be calculated using the python setdifference():
        
        setdifference(set_squares_of before_move, set_square_after a move)
For white moves sets with white pieces are used, for black moves sets with black pieces.

This gives the origin and destination squares (move in uci notation). Knowing the FEN string the standard chess notation (SAN) for this move can be calculated and 
checked if it is valid. When valid the move be used to calculate a the new FEN string of the position that results when the move is made. 
Fen-to-png is used again to convert the new FEN string a new image.
now the procedure the next image is taken, processed and the cycle repeats.
This is done each time the lever of the DGT Clock is pressed.

The program can handle castling, en passant moves and promotion ( and underpromotions) of pawns.

All game data, SAN moves and PGN are saved to a file.

If wanted the program shows the current best move proposoal by stockfish and the curent evaluation in an info window.  

A scoresheet is shown during the game and could be printed out after the game.
For there is a link to lichess/analysis with the game data.



Abbreviations
FEN  Forsythe Edwards Notation
UCI Universal Schess Interface
SAN Standard Chess Notation
PGN Portable Game Notatiom

References:
1. Murat Sahin    https://github.com/sta314/chess_state_recognition
2. Tobi Adewoye   https://github.com/tikul/fen-to-png


