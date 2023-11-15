from shutil import *
import chess
import chess.engine
import chess.svg
import cv2
import sys
import cairosvg
import time
import subprocess
import random
subprocess.call(["clear"])

fen0 = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
FEN0 = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
fen1 = 'rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1'

FEN10 = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"  # correct Initial FEN position with castling rights, halfmove counter and move counter.
FEN11 = "8/1p1K4/p7/b7/8/2P3k1/PP6/8 w - - 0 1"  # b  cp 456  # Pawn Conversion Teststellung und # 26?
FEN12 = "8/q1P1k3/8/8/8/8/6PP/7K w - - 0 1"
FEN13 = "1nb1kqn1/pppppppp/8/6r1/5b1K/6r1/8/8 w - - 2 2"  # stalemate, cp = 0
FEN14 = "6k1/p4p1p/6p1/5r2/3b4/6PP/4qP2/5RK1 b - - 14 36"  # Black is Mate in 2
FEN15 = "1nb1k1n1/pppppppp/8/6r1/5bqK/6r1/8/8 w - - 2 2"  # Mate
FEN16 = "r4rk1/pppb1p1p/2nbpqp1/8/3P4/3QBN2/PPP1BPPP/R4RK1 w - - 0 11"  # > 0
FEN17 = "5R2/2pb2pk/5n1p/5p2/2PPpP1P/3nP1P1/2pN1NR1/6KB b - - 2 33"  # mit Umwandlung
FEN18 = "r1bqk2r/ppp2ppp/2n5/3n4/2BP4/5N2/PP1N1PPP/R2Q1RK1 b kq - 1 10" ## italian game 0-0
FEN19 = "1nbqkb1r/r1p1npp1/pp2p2p/3pP3/2B5/1P1P1P2/P1P1N1PP/RNBQK2R w KQk d6 0 8" ### ep move is best


# engine = chess.engine.SimpleEngine.popen_uci("/home/marius/Desktop/pyprojects/engine_dir/sf12nnue/stockfish")  # SF12NNUE
engine = chess.engine.SimpleEngine.popen_uci("/home/marius/Desktop/pyprojects/ChessGameTracking/sf16nnue/Stockfish-master/src/stockfish")  # SF16NNUE

# a=fen1
# board=chess.Board(FEN11)
# print(board)

# arguments = sys.argv
# fen = str(arguments[1])

def get_field_no(uci_field):
    Li = ["a","b","c","d","e","f","g","h"]
    field_no= Li.index(uci_field[0]) + 8*(int(uci_field[1]) -1)
    return field_no

def write_svg_from_fen(Z1,Z2):
    # board = chess.Board()
    # boardsvg = chess.svg.board(board=board, size=400, flipped=False, coordinates=True, arrows = [(chess.E2,chess.E4, )])
    boardsvg = chess.svg.board(board=board, size=800, flipped=False, coordinates=True, arrows = [(Z1,Z2)], check=Z1)
    f = open("BoardVisualisedFromFEN.SVG", "w")
    f.write(boardsvg)
    f.close()

def show_svg():
    cairosvg.svg2png(url="BoardVisualisedFromFEN.SVG", write_to="output.png")
    image = cv2.imread("output.png")
    cv2.namedWindow("Image_from.FEN")
    cv2.moveWindow("Image_from.FEN",0,0)
    cv2.imshow("Image_from.FEN", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def flip_board(boardstr):
    l = boardstr.split("\n")
    reverse = "\n".join(l[::-1])
    return reverse
# z= flip_board(FEN11)

'''
uci_move = "g1f3"

def convert_uci_for_San():
    A=str(uci_move. upper()[0:2])
    B=str(uci_move. upper()[2:4])
    
    print(A)
    print(B)
    
    return A, B
'''

#   returns newFEN und new board. Uses push san
def make_3_moves_from_start():
    print("make three moves")
    board = chess.Board(FEN0)
    #print(board)
    # Züge ausführen
    #print("make three moves from start pos")
    board.push_san("e4")
    #print(board)
    board.push_san("e5")
    #print(board)cv2.__version__
    board.push_san("Nc3")
    # print(board)
    newFEN=(board.fen())
    # print("newFEN:\n ",newFEN)
    return newFEN, board

'''
###############################
board = chess.Board()
san_move=board.san(chess.Move(chess.G1, chess.F3))
print(san_move)
board.parse_san('Nf3') 
# Move.from_uci('g1f3')
board.variation_san([chess.Move.from_uci(m) for m in ["e2e4", "e7e5", "g1f3"]])
'1. e4 e5 2. Nf3'
'''

def eval(board):
    #### this function return who is to move, lists legal moves, gives best move in uci and san
    #### color_to_move= eval()[0]
    #### number of legal moves [1]
    #### possible moves = eval()[2]
    #### best_move (uci) = eval[3]
    #### best move (san) = eval [4]
    ### score = eval[5]
    # print("\n")
    info = engine.analyse(board, chess.engine.Limit(time= 0.1))
    
    '''
    infostr=str(info)
    # print(info)
    
    # uncomment to printout info
    for key, value in info.items():
        print(key, value)
    print("\n")
    '''
    
    infostr=str(info)
    # print(infostr)
    if "BLACK" in infostr:
        color_to_move= "Black_to_move"
        white_to_move =False
        # print("white_to_move", "(from infostr")
    if "WHITE" in infostr:
        white_to_move=True
        color_to_move="White_to_move"
        # print("White_to_move")
    
    '''
    # uncomment Block to printout
    
    print(board, "\n")
    print("GAMESTATE:")
    print("full_move_No = " , board.fullmove_number)
    print("half_Counter = " , board.halfmove_clock)
    print("can_claim_threefold_repetition:  ",board.can_claim_threefold_repetition())
    print("is fivefold repetition:          ",board.is_fivefold_repetition())
    print("can_claim_fifty_moves:           ", board.can_claim_fifty_moves())
    print("is_seventyfive_moves:            ", board.is_seventyfive_moves())
    print("is check:                        ", board.is_check())
    print("can_claim_draw                   ", board.can_claim_draw())
    print("insufficient_material            ", board.is_insufficient_material())
    print("Checkmate is                     ", board.is_checkmate())
    print("Stalemate is                     ", board.is_stalemate())
    '''
    
    if board.is_checkmate() == True:
        subprocess.call(["clear"])
        print("checkmate, game over")
        return "", "", "", "", "", "Checkmate", ""
    
    if board.is_stalemate() == True:
        subprocess.call(["clear"])
        print("stalemate, game over")
        return "", "", "","", "", "", "", ""

    if board.is_game_over() == True:
        print("game_is_ over " , board.is_game_over(),"\n")
        print("game over")
        return "", "", "", "", "", "", "Stalemate", ""
    
    legal_moves_str =str(chess.LegalMoveGenerator(board))[37:-2]
    number_of_legal_moves= legal_moves_str.count(",")+1
    
    '''
    print("number of legal moves: " , number_of_legal_moves)
    print(legal_moves_str)
    print("depth", info["depth"])
    print("score", info["score"], "(cp or mate)")
    print("Best move uci:", info["pv"][0]) # 
    '''

    best_move= info["pv"][0]
    # print("Best move uci:", best_move)

    move=chess.Move.from_uci(str(best_move)) #### convert uci to san for a specific board position
    # print("Best move san:", board.san(move))
    # subprocess.call(["clear"]) #### comment out to show evals

  
    return color_to_move, number_of_legal_moves, legal_moves_str, info["pv"][0],  board.san(move),info["score"], info["depth"]  ### return color_to_move, movelist, best_move
    engine.quit()
    print("eval done") 

if __name__ == "__main__":

    ### uci_move in san_move umwandeln, benötigt board, muss ein legaler zug sein
    # funktion "convert_uci_for_San()" converts f3 to F3 which can be use to get f3 field number :) geht noch nicht
    # s=str(convert_uci_for_San()[1] )
    # print(s)
    # piece=(str(board.piece_at(chess.E1)))
    # print("piece for san_move ", piece)

    ####s=make_3_moves_from_start()
    # print(result[2])
    #### print("\n", s[0])
    #### print("newBoard:\n", s[1])


    ##### position after tree moves
    ##### eval()

    ### analyse FEN11:


    l = [FEN10,FEN11,FEN12,FEN13,FEN14, FEN15, FEN16, FEN17, FEN18, FEN19]

    xx=random.choice(l)
    board=chess.Board(xx)
    #print(board)
    time0=time.time()

    # eval()
    result=eval(board)
    print(result[0])
    print(result[1], "legal moves: ", result[2])
    print("score (cp or mate): ", result[5], " depth", result[6])
    print("best move uci:", result[3])
    print("best move san:", result[4])
    print()

    ##### get field No from uci notation for arrows (substitute "chess.a8 ....")

    uci_field1= str(result[3])[0:2]
    uci_field2= str(result[3])[2:4]
    if result[3] == "":
        Z1, Z2 = "0","0"
    else:    
        Z1 = get_field_no(uci_field1)
        Z2 = get_field_no(uci_field2)
        print("Arrowfields",Z1, Z2)

    time1=time.time()
    print(int((time1-time0)*1000), "msecs")
    print()

    '''
    first writes an svg file than converts to png. opens png file 
    combined in one Function
    boardsvg = chess.svg.board(chess.Board(FEN), size=800, flipped=False, coordinates=True, arrows = [(Z1,Z2)], check=Z1)
    f = open("FEN.SVG", "w")
    f.write(boardsvg)
    f.close()
    cairosvg.svg2png(url="FEN.SVG", write_to="output.png")
    image = cv2.imread("output.png")
    cv2.namedWindow("Image_from.FEN")
    cv2.moveWindow("Image_from.FEN",0,0)
    cv2.imshow("Image_from.FEN", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    '''
    write_svg_from_fen(int(Z1),int(Z2))             # ca 30 msecs
    show_svg()                                      # SLOW! 700 - 1000 msecs
    
    print("end of program")


    
