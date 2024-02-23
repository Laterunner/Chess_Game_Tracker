# Chess_Game_Tracker
Track Chess Games with Computer Vision.

A Cam (Panasonic DV NV55) connected to a Nvidia Jetson NX mini computer, Python, OpenCV and Numpy, python-chess and Stockfish is used in this program. 


Chessboard, Chess Clock:
The Chess set is a wooden chess board with colored pieces. A DGT3000 Chess clock was modifed with a HAL Sensor and a debounce circuit. Each time the lever is pressed a keystroke "p"  is sent to the mini computer via USB to signalize when a move has been done. Later I used two self constructed, connected chessclocks to signal the program, when a move wis done (see below).


Chess board detection:
The first step is detection of the chessboards on the image, the next step is perspective warping to a square with a defined size. The chessboard is identified by a method described by Murat Sahin 2023 (1) using a cascade of Canny Edge Detection and Hough Line Transform. After the corner coordinates are found the board image is  warped (open CV, Numpy) to a square 800x800 pixels,  which allows easy assigning coordinates to the 4 squares of the chess board.


Piece detection and calibration for color distinction:
To faciliate piece detection colored chess pieces (yellow for the white and red for black pieces) were used. After conversion from BGR to HSV, values for masks to selectivly display either white (yellow) or black ( red pieces were obtained using trackbars (	Open CV) and saved. After this calibration each image could be converted to show selectivly the white (mask for yellow) or black (mask for red) pieces.

Conversion of FEN strings to to PGN/JPG images:
FEN (Forsyth Edwards Notation) is used to describe chess positions. Moves are described their by origin and destination square (which is UCI notation). Normal chessgames always begin with a unique starting position:

	FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

FEN strings were converted to images using fen-to-png from Toby Adewoye 2019 (2) and can be rapidly displayed.


Move detection:
The next step is move detection. For move detection images of the board before and after each move are taken. These two images are than processed with appropriate color filters and masks (see above) to  obtain four images:

1. an image of white pieces before the move
2. an image of white pieces after the move
3. an image of black pieces before the move
4. an image of black pieces after the move

Pieces on the board are identified using the open CV's contours function with area threshold. Rectangular bounding boxes are calculated and their coordinates are used to identify the name of the squares with pieces on (a1 .... h8). 

These square names are stored in sets. Four sets are obtained for each move:

1. set of squares with white pieces before a move
2. set of squares with black pieces before a move
3. set of squares with white pieces after a move
4. set of squares with black pieces after a move

For white moves sets with white pieces are used, for black moves sets with black pieces.
Moves are calculated using the python setdifference():
        
        setdifference(set_squares_of before_move, set_square_after a move)

For most moves setdifference() gives two squares: the origin and destination square, thus the move in uci notation. Castling is recognized because here setdifference() results in four squares, which can be assigned to the respective castle move (e1g1, e8g8, e1c1, or e8c8 in uci notation).

When FEN string and the move (uci notation) are known, it is possible to convert the move in standard chess notation (SAN), which contains information of the moved piece. The move is validated and if legal the move is used to calculate the new FEN string of the resulting position using python-chess/stockfish functions.
 
The new FEN string is used to update the calculated position image using fen-to-png.

Now the cycle repeats, an image is taken, processed, a setdifference() with sets for the color that moves is calculated. This is done each time the lever of the DGT Clock is pressed.

The program can handle castling, en passant moves, promotion and underpromotions of pawns.

All game data, SAN moves and PGN (Portable Game Notation) are saved to a file. If wanted the program shows the current best move proposal by stockfish and the curent evaluation in an info window. 


Notation sheet:
A notation sheet is shown during the game, saved as a text file and could be printed out during or after the game.


Lichess:
An URL is generated  to directly review the game on lichess analysis.

The main directory contains:
1. main2ext.py is setup and should be run for calibration
2. cptestx.py, which is the main program.

fen-to-png and the program for corner detection are in subdirectories. 


Screenshots and images:
in the screenshots subfolder four screenshots are given:
1. 1_setup_corner_detection.png - showing the detected board and their coordinates
2. 2_setup_calibaration.png - showing color calibration window with sliders for the separation of black and white players pieces.
3. 3_chessboard_with_squares.png - The detected chessboard and its squares.
4. 4_ main_window.png - The window of the main program with life image (top left), the boards before and after a move, the board generated from FEN (blue), an info window (black, bottom) and the notation sheet (right).

5. 5_ Prototypes of Chess clocks that can be placed and operated in front of the players rather than on the side of the board. These chess clocks also sent keystroke commands via usb to the computer running the tracking program. If there is a pawn promotion the player can decide how to promote.



The code is hacky, but working very reliable even under changing light conditions. Move detection is within 200 msecs. Remember to set ".sh" files to executable. For demo watch the Youtube video.


Discussion:
Chess board and piece identification have been done with Yolo (You only look once) and trained Networks (1,3,4).  Although Yolo is very fast, it is not as reliable as the method used here, which completely avoids piece identification by computer vision. Identifying chess pieces from an angle by looking at shape, size and color always has the problem of obscured, partly visible and difficult to detect pieces. If Yolo fails and detects a false but legal move, there is no immediate way to correct this. The method used here avoids direct piece identification. With a birds eye view, the initial chess position and move detection and chess rules applied all problems with obscured and partly seen pieces are circumvented. Getting score sheets after games and easy access to lichess analysis are useful features for every serious chess OTB player.

Playing with a chess Clock:
Chess games can be played with the modified DGT 3000 chess clocks placed on the site of the board. However there remains one problem with visual detection of chess moves: Players hands or arms can interfere with move detection. In the moment when images are taken it must be ensured that no body parts of the players obscure the cams view. When chess clocks are placed on the side of the board, it is  almost inavoidable that parts of the players arms are still over the board when the chess clocks lever or button is pressed. If the chessclock would be placed in front of the player there would per no such problem: In the moment the player presses the button his arm would not over the board any more. I therefore constructed chess clock prototypes, which could be placed in front of each player. These clocks are connected by a cable, when a player makes a move and confirms the move by pressing a button on his clock,  the signal is also tranferred to the other players clock. Thus both clocks can be operated from both sites and each one shows the time information and move number for both players. The clocks also send keystokes via usb to the computer that runs the trackng program. The clocks can be used to start the program's setup, start the main program, stop and restart the program, print the notation sheet and open lichess for replay or computer analysis.


References:
1. Murat Sahin: https://github.com/sta314/chess_state_recognition
2. Tobi Adewoye: https://github.com/tikul/fen-to-png
3. Wölflein 2021, Determining Chess Game State from an Image: https://www.mdpi.com/2313-433X/7/6/94
4. Nisan, Shai 2023, Represent Chess Boards Digitally with Computer Vision: https://blog.roboflow.com/chess-boards/
6. Niklas Fiekas 2024, Python-chess https://github.com/niklasf/python-chess

Abbreviations:
1. FEN:  Forsyth Edwards Notation
2. UCI:  Universal Chess Interface
3. SAN:  Standard Chess Notation
4. PGN:  Portable Game Notation
5. OTB:  Over The Board

Dr. Marius Bartsch Jan 2024

