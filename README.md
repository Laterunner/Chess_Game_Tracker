# Chess_Game_Tracker
Track Chess Games with Computer Vision.

A Cam (Panasonic DV NV55) connected to a Nvidia Jetson NX mini computer, Python, OpenCV and Numpy, python-chess and Stockfish is used in this program. 

The Chess set is a wooden Chess board with colored pieces. A DGT3000 Chess clock was modifed with a HAL Sensor and a debounce circuit. Each time the lever is pressed a keystroke "p"  is sent to the mini computer via USB to signalize when a move has been done.

The Chessboard is identified by a method described by Murat Sahin 2023 (1) using a cascade of Canny Edge Detection and Hough Line Transform. After the corner coordinates are found the board image is  warped to a square of 800x800 pixels. Now assigning coordinates to the 64 sqaures is greatly faciliated.

FEN (Forsyth Edwards Notation) is used to describe chess positions. Moves are described their by origin and destination square (which is UCI notation). Normal chessgames always begin with a unique starting position:

	FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

This FEN string can be converted to an image using fen-to-png from Toby Adewoye 2019 (2) and rapidly displayed.

The next step is move detection. For move detection images of the board before and after each move are taken. These two images are processed with a apropriate color filters and masks to  obtain four images:

1. an image of white pieces before the move
2. an image of white pieces after the move
3. an image of black pieces before the move
4. an image of black pieces after the move

Pieces are than identified using the open CV contours() function with area threshold, a bounding boxes was applied. Coordinates of the bounding boxes were used to identify the name of the squares with pieces on (a1 ....h8). 

These squarenames are stored in sets. Four sets are obtained for each move:

1. set of squares with white pieces before a move
2. set of squares with black pieces before a move
3. set of squares with white pieces after a move
4. set of squares with black pieces after a move

For white moves sets with white pieces are used, for black moves sets with black pieces.
Moves are calculated using the python setdifference():
        
        setdifference(set_squares_of before_move, set_square_after a move)

For most moves Setdifference() gives two squares: the origin and destination square, thus the move in uci notation. Castling is recognized because here setdifference() results in four squares, which can be assigned to the respective castle move (e1g1, e8g8, e1c1, or e8c8 in uci notation).

When FEN string and the move (uci notation) are known, it is possible to convert the move in standard chess notation (SAN), which contains information of the moved piece. After validation the move is used to calculate the new FEN string of the resulting position of this move using python-chess/stockfish functions.
 
The new FEN string is used to get a new image using fen-to-png.

Now the cycle repeats, an image is taken, processed, a setdifference() with sets for the color that moves is calculated. This is done each time the lever of the DGT Clock is pressed.

The program can handle castling, en passant moves and promotion (and underpromotions) of pawns.

All game data, SAN moves and PGN (Portable Game Notation) are saved to a file. If wanted the program shows the current best move proposal by stockfish and the curent evaluation in an info window. 

A scoresheet is shown during the game and could be printed out after the game.
Games can be replayed or analysed in Lichess (one click).

The main directory contains:
1. main2ext.py is setup and should be run for calibration
2. cptestx.py, which is the main program.

fen-to-png and the program for corner detection are in subdirectories. 


Screenshots:
in the screeshots subfolder four screeshots are given:
1. 1_setup_corner_detection.png - showing the detected board and their coordinates
2. 2_setup_calibaration.png - showing color calibration window with sliders for the separation of black and white players pieces.
3. 3_chessboard_with_squares.png - The detected chessboard and its squares.  
4. 4_ main_window.png - The window of the main program with life image (top left), the boards before and after a move, the board generated from FEN (blue), an info window (black, bottom) and the scoresheet (right).

The code is hacky, but working very reliable even under changing light conditions. Move detection is within 200 msecs. Remember to set ".sh" files to executable. For demo watch the Youtube video.


Discussion:
Chess board and piece identification have been done with Yolo (You only look once) and trained Networks (1,3,4).  Although Yolo is very fast, it is not as reliable as the method used here, which completely avoids piece identification. Identifying chess pieces from an angle by looking at shape, size and color always has the problem of obscured, partly visible and difficult to detect pieces. If Yolo fails and detects a false but legal move, there is no immediate way to correct this. The method used here avoids direct piece identification.  With a birds eye view, the initial chess position and move detection and chess rules applied all problems with obscured and partly seen pieces are circumvented. Getting score sheets after games and easy access to lichess analysis are useful features for every serious chess OTB player.

There remains one problem with visual detection of chess moves and that is the players hands, which should not be over the board in the moment, when images are taken. This could be achieved, if both players use only one hand (the hand next to the chess clock located at the side of the board) to make moves and press the clock's lever. A good solution could eventually be the placement of a new button or keypad outside the board in front of each player ouside the board. Than it might even be possible to use hand detection instead of lever or key presses (for finishing moves).


References:
1. Murat Sahin: https://github.com/sta314/chess_state_recognition
2. Tobi Adewoye: https://github.com/tikul/fen-to-png
3. Wölflein 2021, Determining Chess Game State from an Image: https://www.mdpi.com/2313-433X/7/6/94
4. Nisan, Shai 2023, Represent Chess Boards Digitally with Computer Vision: https://blog.roboflow.com/chess-boards/

Abbreviations:
1. FEN:  Forsyth Edwards Notation
2. UCI:  Universal Chess Interface
3. SAN:  Standard Chess Notation
4. PGN:  Portable Game Notation
5. OTB:  Over The Board

Dr. Marius Bartsch Nov 2023

