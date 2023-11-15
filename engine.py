#!/home/marius/tf2/bin/python
# This modul calculates FEN positions
# evalzation in centipawn or mate
# best move in algebraic notation
# calculation time set for 1000 msec
# choose a FEN line to test
# fen2boolboard generates various boolboard (no piece specification)

import time
import sys
import os
import cv2
import numpy as np
import subprocess
import chess  # python-chess V. 031
import chess.engine
from chess.engine import Cp, Mate, MateGiven
import chess.svg
subprocess.call(["clear"])


################################################################################################################
### choose an engine with correct path to engine
################################################################################################################

# engine = chess.engine.SimpleEngine.popen_uci("stockfish")  # SF8
# engine = chess.engine.SimpleEngine.popen_uci("/home/marius/Desktop/pyprojects/engine_dir/sf12nnue/stockfish")  # SF12NNUE
# engine = chess.engine.SimpleEngine.popen_uci("/home/marius/Desktop/pyprojects/engine_dir/lc0/lc0")  # Lc0 - dirty
#~/Desktop/pyprojects/Realtime-OpenCV-Chess/sf16nnue/Stockfish-master/src
engine = chess.engine.SimpleEngine.popen_uci("/home/marius/Desktop/pyprojects/ChessGameTracking/sf16nnue/Stockfish-master/src/stockfish")  # SF16NNUE


#################################################################################################################
### FEN Test POSITIONS to Cycle
#################################################################################################################

FEN0 = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"  # correct Initial FEN position with castling rights, halfmove counter and move counter.
FEN1 = "8/1p1K4/p7/b7/8/2P3k1/PP6/8 w - - 0 1"  # b  cp 456
# Pawn Conversion Teststellung und # 26?
FEN2 = "8/q1P1k3/8/8/8/8/6PP/7K w - - 0 1"
FEN3 = "1nb1kqn1/pppppppp/8/6r1/5b1K/6r1/8/8 w - - 2 2"  # stalemate, cp = 0
FEN4 = "6k1/p4p1p/6p1/5r2/3b4/6PP/4qP2/5RK1 b - - 14 36"  # Black is Mate in 2
FEN5 = "1nb1k1n1/pppppppp/8/6r1/5bqK/6r1/8/8 w - - 2 2"  # Mate
FEN6 = "r4rk1/pppb1p1p/2nbpqp1/8/3P4/3QBN2/PPP1BPPP/R4RK1 w - - 0 11"  # > 0
FEN7 = "5R2/2pb2pk/5n1p/5p2/2PPpP1P/3nP1P1/2pN1NR1/6KB b - - 2 33"  # mit Umwandlung
time0 = time.time()
FEN= FEN7

def legal_moves_2(FEN): # checks UCI moves
    print("RUNNING legal_moves_2")
    ## this version gives possible starting and destination fiels of a piece
    board = chess.Board(FEN)
    # print(board)
    legal_moves = list(board.legal_moves)  # Generate a list from the generator.
    n = len(legal_moves)  # Number of legal moves
    #print("Number of next legal moves: ", n)
    # print(legal_moves[0], legal_moves[n-1])
    # print("\nLegal moves (direct Output): ", legal_moves[0:n])
    k = str(legal_moves[0:n])  # k in str umwandeln
    # print("\nLegal moves als str: ", k)
    k = k.replace("Move.from_uci", "")
    k = k.replace("'", "")
    k = k.replace("[", "")
    k = k.replace("]", "")
    k = k.replace("(", "")
    k = k.replace(")", "")
    # print("legal moves as formated str: ", k)  # str ausdrucken
    l = k.split(", ")  # k in Liste umwandeln
    # print("legal moves (list): ", l[0:n])  # Liste ausdrucken
    # print("total time", int((time.time()-time0) *1000), "msecs")
    # print(k)
    # print(l)
    return k


def legalmove_3(FEN):   # as legalmoves_2 but checks SAN moves
    print("\nRUNNING legal_moves_3") # braucht ca. 6 microsec
    board=chess.Board(FEN)
    print(board)
    time10 = time.time()
    z= (board.legal_moves)
    print(z)
    z=str(z) # in str umwandeln
    z1 = z.split("(") # l=legalmove_3(FEN)
    print("legal move_list_dest:", z1)
    # time_x1=time.time()
    # print((time_x0 - time_x1), "msec")
    print("total time", int((time.time()-time10) *1000), "msecs")
    return


def engine_eval(FEN):
    print("\nRUNING engine_eval(FEN) ...")
    print("SHORT DEMO OF STOCKFISH CAPABILITIES:\n")
    print("FEN", FEN)
    board=chess.Board(FEN)
    print(board,"\n")
    print("half_move=",board.halfmove_clock)
    print("full_move_No=", board.fullmove_number)
    print("- mate?", board.is_checkmate())
    print("- stalemate?", board.is_stalemate())
    
    legal_moves=chess.LegalMoveGenerator(board)
    print("- are there legal moves?", bool(board.legal_moves))
    print("- legal moves (N):", board.legal_moves.count())
    print("- possible moves", str(legal_moves)[37:-2])
    move=chess.Move.from_uci("a2a3")
    j=move in board.legal_moves
    print("-",move, "- is a legal move? ...", j)

    if (board.is_stalemate() or board.is_checkmate()):
        print(" \nSTALEMATE or MATE, GAME OVER.  Nothing to calculate!")
    else:
        print("\ntotal time", int((time.time()-time0) *1000), "msecs \n")
        evaluate_fen(FEN)

    return

#################################################################################
### do not run this on Mate or Stalemate positions.
### to be safe run module from engine_eval(FEN) only
#################################################################################

def evaluate_fen(FEN): 
    print("RUNNING evaluate_fen()")
    print("Evaluates positions from whites perspective")
    print("FEN: ", FEN)
    board = chess.Board(FEN)
    #print(board)
    info = engine.analyse(board, chess.engine.Limit(time=1.0))
    # print(info.get("pv")[0])  # bester Zug
    eval_1w = str(info.get("score"))  # converted to str
    # print(eval_1w)  # score aus der Sicht des ziehenden

    if "+" in (eval_1w):
        eval_1b = eval_1w.replace("+", "-")
    
    if "-" in (eval_1w):
        eval_1b = eval_1w.replace("-", "+")
    # print(eval_1w)
    # print(eval_1b)

    eval=[]

    if " w " in FEN:
        
        print("white to move,  best move:", info.get("pv")[0])
        eval.append(eval_1w)
        print(eval_1w, "cp")

    if " b " in FEN:
        
        print("black to move, best move", info.get("pv")[0])
        eval.append(eval_1b)
        print(eval_1b, "cp")

    print("eval_order (bad to good):" ,"Mate(-0) < Mate(-1) < Cp(-50) < Cp(200) < Mate(4) < Mate(1) < MateGiven\n")
    
    # print(eval, "centipawns \n")
    #print("\ntotal time", round((time.time()-time0) *1000), "msecs, includes 1000 msec for evaluation")
    return  eval

####################################################################################################
### Generate Boolboards from FEN for Black, white or both players
####################################################################################################

def convert_fen2boolboard_black(FEN):
    print("generating black_player_boole_position (array)")
    black_player_bool_position = []
    for row in FEN.split(' ')[0].split('/'):
        bool_row = []
        for cell in list(row):
            if cell.isnumeric():
                for i in range(int(cell)):
                    bool_row.append(0)
            else:
                if cell.islower():
                    bool_row.append(1)
                else:
                    bool_row.append(0)
        black_player_bool_position.append(bool_row)
        print (bool_row)    
    black_player_bool_position = np.array(black_player_bool_position)
    print("time_used", round((time.time()-time0) *1000), "msecs")
    return #black_player_bool_position


def convert_fen2boolboard_white(FEN):
    print("generating white_player_boole_position (array)")
    white_player_bool_position = []
    for row in FEN.split(' ')[0].split('/'):
        bool_row = []
        for cell in list(row):
            if cell.isnumeric():
                for i in range(int(cell)):
                    bool_row.append(0)
            else:
                if cell.isupper():
                    bool_row.append(1)
                else:
                    bool_row.append(0)
        white_player_bool_position.append(bool_row)
        print (bool_row)    
    white_player_bool_position = np.array(white_player_bool_position)
    print("time_used", round((time.time()-time0) *1000), "msecs")
    return #white_player_bool_position


def convert_fen2boolboard(FEN):
    print("generating boole_position (array)")
    bool_position = []
    for row in FEN.split(' ')[0].split('/'):
        bool_row = []
        for cell in list(row):
            if cell.isnumeric():
                for i in range(int(cell)):
                    bool_row.append(0)
            else:
                if cell:
                    bool_row.append(1)
                else:
                    bool_row.append(0)
        bool_position.append(bool_row)
        print (bool_row)    
    bool_position = np.array(bool_position)
    print("time_used", round((time.time()-time0) *1000), "msecs")
    return bool_position


### Demo functions:

def which_piece1(): # Eingabe 
       
    
    board=chess.Board()
    x=board.fen()
    k=board.piece_at(chess.E1)
    print("\n",k)

def which_piece2():
    board=chess.Board()
    print(chess.A2)
    position=53
    r=board.piece_at(position)
    print(r)

def noch_eine():
    l=board.epd(bm=board.parse_uci("d2d4")) 
    print(l)
    ops = board.set_epd("1k1r4/pp1b1R2/3q2pp/4p3/2B5/4Q3/PPP2B2/2K5 b - - bm Qd1+; id \"BK.01\";")
    print(ops)

    print("half_move=",board.halfmove_clock)

    k=chess.square_name(63) # square Number (00-63)to position (a1-h8)
    print(k)
    k=chess.square(7,7) # row (0...7),col(0...7) to square number(0-63)
    print(k)


def move_pair_in_list(k, move):
    legal_moves_2(FEN)
    # subprocess.call(["clear"])
    print("\nRUNNING movepair_in_list, move: ", move)
    # print("tested list:", k)
    print("tested move_pair:", move[0:])
    if move[0:] in k:
        print("movepair is valid")

    else:
        move_inverted=str(move[2:4])+str(move[0:2]) # switch move_pair
        # print("trying inverted move: ", move_inverted)
        if move_inverted[0:4] in k:
            print("inverted movepair is valid")
            move = move_inverted
        else:
            print("move_pair not in list")
            move = "ERROR_1"
            
    
    # check if there is a promotion possible, than promote to queen
        
    print(move , end = '')
    if str(move[0:]+"q") in k:
        print (", pawn can be promoted to Queen")
        move=str(move+"q")
    if str(move[0:]+"Q") in k:
        print (", pawn can be promoted to Queen")
        move=str(move+"Q")        
    return move


### zug in uci, ausgabe im San

def function1():
    Move=["e2e4"]
    LL=board.variation_san([chess.Move.from_uci(m) for m in list])
    print("SAN_move: ", Move)


    #### Liste in uci, l=legalmove_3(FEN) Ausgabe in SAN
        
def make_san_movelist_from_uci_sequence(list):        
    list=list
    print("  UCI- Move list:", list)
    LL=board.variation_san([chess.Move.from_uci(m) for m in list])
    print("  San Moves :", LL, "\n")
    return LL

def move_from_sanlist(list):
    list=list
    print("  LIST:", list)
    for i in list:
        print(board, "\n")
        print("Move:", i)
        board.push_san(i)
        print(board.fen())

    #subprocess.call(["clear"])

def move_now(uci_move, FEN):
    print("\nRUNNING move_now(uci_move, FEN):")
    print(FEN)
    board=chess.Board(FEN)
    # print("uci_move, must be valid", uci_move)
    print("\nOrginal Board:")
    print(board)
    ##print("---FEN:  ", board.fen())
    board.push(chess.Move.from_uci(uci_move))
    newboard= board
    print("moved:", uci_move, "\n=> New Board:")
    
    print(board)
    newFEN=board.fen()
    return newFEN, newboard

board=chess.Board()

# Eingabe in uci
# board=chess.Board()
# board.puprint(sh(chess.Move.from_uci("d1d5")) # move piece, regardless of legal or not
# print(board)
# print("exiting now, Engine quit")
# engine.quit()

def update_FEN(FN, movepair):
    print("\nRUNNING update_FEN")
    print("FEN:", FN, "\nuci_move:", movepair)
    board=chess.Board(FN)
    
    ### next function checks move and inverted move
    ### movepair = move_pair_in_list(legal_moves_2(FN), movepair) ## if movepair or inverted movepair contains is a valid move, give move
    # print("Result movepair (now corrected): ============>", movepair)
    
    try:
        result1= move_now(movepair, FN)
        newFEN=(result1)[0]
        # print("org FEN", FN)
        # print("new FEN", newFEN)
        # movepair
        return newFEN, movepair
    
    except:
        print("Error occurred, Move not in list => cannot do that")
        

uci_move2="g1g3"

def field_no(n):
    #r=board.piece_at(n)
    letter1=n[0]
    zahl1=int(n[1])
    # letter2=n[2]
    # zahl2=int(n[3])
    
    field1= str(letter1+str(zahl1))   
    # field2= str(letter2+str(zahl2))   
    
    L=("a","b","c","d","e","f","g","h")
    n1=L.index(letter1) + (zahl1-1)*8
    # n2=L.index(letter2)-1 + (zahl2-1)*8
    
    # print("UCI:" , field1, field2, " No:" , n1, n2)
    piece=board.piece_at(n1)    
    return n1, piece

Piecex = field_no(uci_move2)[1]
print(uci_move2, Piecex)
print (board)

# SAN SAN notation (RNBKQ)
if str(Piecex) =="p" or str(Piecex) == "P":
    SAN= uci_move2[2:]
else:
    SAN=str(Piecex)+uci_move2[2:]


print(SAN)


        
if __name__ == "__main__":
    '''
    for i in range (1,40,4):
        imgcounter=i
        F="FEN{}".format(imgcounter)
        print(F)
    '''

    FEN=FEN7 ###  choose starting FEN testet F
    FN=FEN
    movepair="c2c1q"     ### choose Test move (uci, should be in move)
    l1= (update_FEN(FN, movepair))[0:] # gibt newFEN zurück
    print("result",l1)
    print("\n\n\n\n")
    # FEN=l1
    # R = update_FEN(FN, movepair)
    
    # print(movepair)
    # print("nnn", R[1]) #### R[0] is new FEN , R[1] is corrected move.

    # print("R=", R)
    #  uncomment to run'
    # legal_moves_2(FEN)  ### Starting and destination 3msec
    # engine_eval(FEN)
    #################################################################################################################
    ########## MORE FUNCTIONS TO CALL
    #################################################################################################################
    # legalmove_3(FEN)   ### only destination 2 msec
    
    #engine_eval(FEN)
        # evaluate_fen(FEN) # run from info1(FEN)
    
    # which_piece1() # Square No (00 - 63) to piece (PRNBKQ)
    # which_piece2()  # Square Position (A1 -H8) returns Piece pPrRkKnBKQ)
    #print(Z)

    ### BOOLBOARDS
        #convert_fen2boolboard_black(FEN)
        # convert_fen2boolboard_white(FEN)
        #convert_fen2boolboard(FEN)
    
    ### VARIOUS FUCTIONS
        # noch_eine()
           
    ### MAKE A SAN LIST FROM UCI MOVES (not pairs)
        #list =["e2e4", "e7e5", "g1f3", "b8c6","f1c4", "g8f6"]
    ## make_san_movelist_from_uci_sequence(list)  # SAN move list)
    
    ### MOVE from SAN LIST (sehr gute Funktion!)
    ### list = ["e4", "e5", "Nf3", "Nc6", "Bc4", "Nf6"]
    ### move_from_sanlist(list)

    #### MOVES from UCI_Input
    # move="b1c3"
    # move_now(move, FEN0)
    
    print("exiting now")
    engine.quit()
