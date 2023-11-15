# from chess import A1
import cv2
from cv2 import blur    

import numpy as np
import threading
import time
from datetime import datetime
import subprocess
import os
import sys
from detect_points import get_points
from read_warp_img import get_warp_img
from date import show_scoresheet
import cvzone
import pickle
import chess
import chess.engine
from engine import legal_moves_2
from engine import move_pair_in_list
from engine import update_FEN
from enginefunctions import eval
from enginefunctions import get_field_no
# from text_helper import text_function
import cairosvg
import chess.svg
from IPython.display import SVG
import webbrowser

# import pyvips
time0 = time.time()

#frameWidth = 640
#frameHeight = 480
# subprocess.call("clear")

cap = cv2.VideoCapture(0)
print("frameWidth= ", cap.get(3))
print("frameHeight= ",cap.get(4))
# cap.set(3, frameWidth)
# cap.set(4, frameHeight)

dir_path=os.path.dirname(os.path.realpath(__file__))+"/numpy_saved"
code="hello"
dir_path += "/"+code
print("working directory:", dir_path)


fen_line = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR' # fen line of chess board
board = chess.Board(fen=fen_line) # object of ches>s board
image = []
# SF12NNUE
stockfish_path = "/home/marius/Desktop/pyprojects/engine_dir/sf12nnue/stockfish"
# engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)

chess_board = []   # it will store chess board matrix
player_bool_position =[]
bool_position = np.zeros((8,8),dtype=int)
number_to_position_map = []
FEN0="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

last_move = ""
game_img = ""
move_counter = 0
uci_move = ""


def empty(a):
    pass

###Load preset values from setup.bin
with open('setup.bin', 'rb') as f:
    L3 = pickle.load(f) # load saved values (from main2ext.py)

# print("L3 loaded from setup.bin L3:")
# print(L3)

h_min =int(L3[0])
s_min =int(L3[1])
v_min =int(L3[2])
h_max =int(L3[3])
s_max =int(L3[4])
v_max =int(L3[5])
h_min2 =int(L3[6])
s_min2 =int(L3[7])
v_min2 =int(L3[8])
h_max2 =int(L3[9])
s_max2 =int(L3[10])
v_max2 =int(L3[11])

def cam_func(FEN):
    time00=time.time()
    move_counter=0
    _counter = 0
    action=False
    uci_list=[]                    
    image0 = np.zeros((800, 800, 3), np.uint8) # blanc image
    image0w = np.zeros((800, 800, 3), np.uint8) # blanc image
    image0b = np.zeros((800, 800, 3), np.uint8) # >blanc image
    
    image1 = np.zeros((800, 800, 3), np.uint8) # blanc image
    image1w = np.zeros((800, 800, 3), np.uint8) # blanc image
    image1b = np.zeros((800, 800, 3), np.uint8) # blanc image
   
    image3 = np.zeros((800, 800, 3), np.uint8) # blanc image
    image3w =np.zeros((800, 800, 3), np.uint8) # blanc image
    image3b =np.zeros((800, 800, 3), np.uint8) # blanc image
    
    _testim1 = np.zeros((800, 800, 3), np.uint8) # blanc image
    _testim2 = np.zeros((800, 800, 3), np.uint8) # blanc image
    _testim3 = np.zeros((800, 800, 3), np.uint8) # blanc image
    blanc_image = np.zeros((800, 800, 3), np.uint8) # blanc image
    blanc_image2 = np.zeros((200, 1200 , 3), np.uint8) # blanc image
        
    cv2.namedWindow("Image", cv2.WINDOW_AUTOSIZE)
    cv2.moveWindow("Image", 1, 1)
    cv2.namedWindow("Image2", cv2.WINDOW_AUTOSIZE)
    # cv2.moveWindow("Image2", 800, 1)
    cv2.moveWindow("Image2", 1, 470)
    fen_image = cv2.imread("fen-to-png/output/starting_pos.png") 
    text = ""
    LL=""
    uci_move_list = []
    san_move_list = []
    board0=chess.Board(FEN0)
    take_back_counter = 0
    wtime_list = []
    btime_list = []
    white_time=0
    black_time=0
    time000 = time.time()
    if move_counter == 0:
        subprocess.call("clear")
        print(move_counter)
        print( "White lever up, Board in initial position: Press 'p' to start game")
        text = "White lever up, Board in initial position: Press 'p' to start game"

    while True:
        _, img = cap.read()
        if not _:
            break
        img = cv2.resize(img, (800,800)) # 2 msec
        
        ###################################################################################
        # if necessary rotate cam image
        # img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)'
        # img = cv2.rotate(img, cv2.ROTATE_180)
        # img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
        # this must also be changed in main2ext.py (setup prog)
        ###################################################################################
        
        img =get_warp_img(img, dir_path,(800,800)) # 59 msecs
        imgHsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

        ### for red (black pieces)
        lower = np.array([h_min,s_min,v_min])
        upper = np.array([h_max,s_max,v_max])
        mask1 = cv2.inRange(imgHsv,lower,upper)
        result1 = cv2.bitwise_and(img,img, mask = mask1) # only red pieces are visible
            
        ### for yellow (white pieces)
        lower2 = np.array([h_min2,s_min2,v_min2])
        upper2 = np.array([h_max2,s_max2,v_max2])
        mask2 = cv2.inRange(imgHsv,lower2,upper2)
        result2 = cv2.bitwise_and(img,img, mask = mask2) # only yellow pieces are visible

        result3 = cv2.absdiff(result1, result2) # warped, b& w pieces

        ### for red (black )pieces
        mask1 = cv2.cvtColor(mask1, cv2.COLOR_GRAY2BGR)
        mask2 = cv2.cvtColor(mask2, cv2.COLOR_GRAY2BGR)

        ### blur (not used)
        ### mask2=blur(mask2,(7,3))
        ### mask2=blur(mask2,(5,5))
        
        ####Show  mask or results
        # hStack = np.hstack([img,result1,result2])
        #cv2.imshow('Original', img)
        #cv2.imshow('HSV Color Space', imgHsv)
        #cv2.imshow('Mask', mask1)
        #cv2.imshow('Result', result1)
        #cv2.imshow("File", result2)
        
        ##cv2.imshow('Horizontal Stacking', hStack)
        ##cv2.moveWindow("Horizontal Stacking", 440,0)mtext="hahaha"
        
        ###alternative mit stackimages
        FPS = int(1/((time.time()-time00)))
        # print(FPS, "FPS running ....... press 'q' to quit")

        # imgStacked=cvzone.stackImages([img,result1, result2,result3],4, 0.3) # show with live image
        # imgStacked=cvzone.stackImages([img, image0, image1, image0w, image1w, image0b, image1b],6, 0.5) # for tests
        
        # imgStacked=cvzone.stackImages([img, result2, result1,],3, 0.25)
        
        if " w " in FEN != 0:
            # imgStacked=cvzone.stackImages([img, image0, image1,],3, 0.25) # 
            imgStacked=cvzone.stackImages([img, np.copy(image3w), result2, fen_image],4, 0.375) # 
        
        if " b " in FEN:
            imgStacked=cvzone.stackImages([img, image1b,result1, fen_image],4, 0.375) # 
        
        if " w " in FEN and move_counter ==0:
            # imgStacked=cvzone.stackImages([img, image0, image1,],3, 0.25) #
            #imgStacked=cvzone.stackImages([img,np.copy(image3w), np.copy(image3w,)],3, 0.375 # 
            imgStacked=cvzone.stackImages([img,blanc_image, blanc_image,result3],4, 0.375) # 
        
        
        # print(imgStacked.shape)
        # cv2.moveWindow("Image", 400, 1)  
        
        # print(move_counter -1)
        
        # if move_counter == 0:
        #     vtext = ""    
        # if move_counter == 1:
        #     mtext = LL
        #if move_counter > 1:
        #    mtext = LL
        # print(vtext)
        
        
        # print("text ==", text)
           
        ### here you need window_name, image, text, 
        # if len(text) > 40:
        #     k = 42 # Zeichenzahl für Zeilenumbruch (\n) einfügen
        #     text= "\n".join(text[i:i+k] for i in range(0,len(text),k))    
        font = cv2.FONT_HERSHEY_SIMPLEX
        # font = cv2.FONT_HERSHEY_PLAIN
        # font = cv2.FONT_HERSHEY_SCRIPT_COMPLEX
        font_scale = 0.76
        thickness = 1
        color = (255, 255, 255)
        line_type = cv2.LINE_AA
        # line_type = cv2.LINE_AA
        # print("height  width:", image.shape[0],image.shape[1] )
        text_size, _ = cv2.getTextSize(text, font, font_scale, thickness)
        line_height = text_size[1] + 5
        x, y0 = int(10),int(25)
        for i, line in enumerate(text.split("\n")):
            y = y0 + i * line_height
            cv2.putText(blanc_image2,
                        line,
                        (x, y),
                        font,
                        font_scale,
                        color,
                        thickness,
                        line_type)

        cv2.imshow("Image" ,imgStacked) # show only worked out images
        #cv2.moveWindow("Image", 1, 1)
        cv2.imshow("Image2", blanc_image2) # show only worked out images
        

        xyz = cv2.waitKey(5)

        if xyz%256 == 27:
            break
        
        if xyz%256 == 112 or xyz%256 == 80: # "p":
            timep=time.time()
         
            print("\n====>Image Counter",move_counter)

            #######################################################
            # generate imagepairs  for move detection             #
            # use either image0/image1                            #
            # or image1w image0w & image1b und image0b            #
            #######################################################            
            
            if move_counter== 0:
                print("generated image0 = initial position")
                image0 =np.copy(result3)
                image0w = np.copy(result2)
                image1= blanc_image
                image3 = np.copy(blanc_image)
                print("Make Move 1, press p")
                move_counter = move_counter+1    
            
            if move_counter > 0: # and move_counter%2 ==0:
                image0 = np.copy(result3)
                image0w= np.copy(result2)
                image0b= np.copy(result1)
                image1 = image3
                image1w =image3w
                image1b= image3b
                image3 =image0
                image3w = image0w
                image3b = image0b
                move_counter = move_counter+1
                print("generated new image0, image 1")
                print("make move ", move_counter, "press p")
            

            '''
            file_name = "{}.jpg".format(move_counter)
            cv2.imwrite(file_name, img)
            '''
            ### inserted "moved_pieces"
            
            ### use images acoordind the color of the move piece text4 = "\nbest reply would be: " +  str(eval(newboard)[3])
            if move_counter%2 ==1: # white just moved
                prev_piecelist = detect_position_of_pieces(image1w) ## =list_0
                new_piecelist = detect_position_of_pieces(image0w) ## 0 = piecelist in detect_moved ...
                print("prev_piecelist_w:", prev_piecelist)
                print("\nnew_piecelist_w:", new_piecelist)
                
            if move_counter%2 ==0: # black just moved
                prev_piecelist = detect_position_of_pieces(image1b) ## = list_0
                new_piecelist = detect_position_of_pieces(image0b) ## 0 = piecelist in detect_moved ...
                print("prev_piecelist_b:", prev_piecelist)
                print("\nnew_piecelist_b:", new_piecelist)

            # prev_piecelist = detect_position_of_pieces(image1) ## =list_0
            # new_piecelist = detect_position_of_pieces(image0) ## 0 = piecelist in detect_moved ...
            # print("prev_piecelist:", prev_piecelist)
            # print ("\nnew_piecelist:", new_piecelist)

            difference_1 = set(new_piecelist).difference(set(prev_piecelist))
            difference_2 = set(prev_piecelist).difference(set(new_piecelist))
            list_difference = list(difference_1.union(difference_2))
            ### The difference() method computes the difference of two sets 
            ### and returns the items that are unique to the first.
            print("list_difference ", list_difference)
            
            ###############################################
            ### comment next line for debug             ###    
            subprocess.call("clear")                    ### 
            ###############################################

            print(".... detecting uci_move")
            
            ###############################################
            ### DETECT CASTLE                           ###
            ###############################################

            if len(list_difference) == 4:
                if sorted(list_difference) == ["e1","f1","g1","h1"]:
                    print("detected white castled short ..")
                    list_difference = ["e1","g1"]
                        
                if sorted(list_difference) == ["a1","c1","d1","e1"]:
                    print("detected white castled long ..")
                    list_difference = ["e1","c1"]
                    
                if sorted(list_difference) == ["e8","f8","g8","h8"]:
                    print("detected black castled short ..")
                    list_difference = ["e8","g8"]
                    
                if sorted(list_difference) == ["a8","c8","d8","e8"]:
                    print("detected black castled long ..")
                    list_difference = ["e8","c8"]
                ### to do: meck move check legal_move list


            ###############################################
            ### detect normal moves, including e.p.     ###
            ###############################################

            if len(list_difference) == 2:
                #correct move is d2 d4 not d4 d2!
                print("HYO",list_difference)
                if (list_difference[0]) in new_piecelist:
                    uci_list.append(list_difference[1])
                    uci_list.append(list_difference[0])

                if (list_difference[1]) in new_piecelist:
                    uci_list.append(list_difference[0])
                    uci_list.append(list_difference[1])

            # print("last uci_move:", uci_list[-2:]) # uci_list gives corrected uci_move
            #### generate san Notation and arrow_field_numbers ####
            
            uci_move = uci_list[-2:]
            uci_move ="".join(uci_move)
            uci_move.replace(" ", "")
            if uci_move is not "":
                Z1=get_field_no(str(uci_move[0:2]))
                piece=str(board.piece_at(Z1)).upper() 
                print("found uci_move", uci_move)           
                Z1 = get_field_no(uci_move[0:2])
                Z2 = get_field_no(str(uci_move[2:4]))
                print("Arrowfields for SVG:",Z1, Z2)
                print()

            
            
            uci_move = uci_list[-2:]
            uci_move ="".join(uci_move)
            uci_move.replace(" ", "")
            
            
            
            if uci_move is not "":
                Z1=get_field_no(str(uci_move[0:2]))
                piece=str(board.piece_at(Z1)).upper() 
                print("found uci_move", uci_move)           
                Z1 = get_field_no(uci_move[0:2])
                Z2 = get_field_no(str(uci_move[2:4]))
                print("Arrowfields for SVG:",Z1, Z2)
                print()
            else:
                print("found no uci_move", uci_move)
                if move_counter == 2:
                    # This loop is only entered at gamestart
                    # subprocess.call("clear")
                    print("389 Make Whites first Move and press P")
                    text = "ok"
                    time000 = time.time() ### time when game start
                    game_started = str(datetime.today().strftime("%A, %B %d, %Y %H:%M:%S"))        
                    print("zero_time ", game_started)

            print(move_counter)
            print(text)
            
            subprocess.call("clear")
            blanc_image2 = np.zeros((200, 1200, 3), np.uint8) # blanc image AUTOSIZE)
            text = "Now make White's first move and press lever or "'"p"'", time is running!"
      
            
            print(FEN)
            print(text)

            
            if uci_move is not "":
                uci_copy = str(uci_move)
                kkk = legal_moves_2(FEN)
                print()
                print("legalmove_list: ",kkk)

                ########################################
                # recognize and handle pawn promotion: #
                ########################################
                if str(uci_move)+"q" in kkk:
                    blanc_image3 = np.zeros((200, 1200, 3), np.uint8) # blanc image AUTOSIZE)                    
                    cv2.putText(blanc_image3, "To promote pawn to Queen, Knight, Rock or Bishop press "'q'", "'n'", "'r'" or "'b'" ", (20,20),font, font_scale, color, thickness, line_type)
                    while True:
                        cv2.imshow("Image3", blanc_image3)
                        cv2.moveWindow("Image3", 680, 1)
                        stop = cv2.waitKey(0)
                        if stop%256 == 113 or stop%256 == 110 or stop%256 == 114 or stop%256 == 98:
                            break
                    cv2.destroyWindow("Image3")
                    uci_move = uci_move + chr(stop)
                    print("***uci_move corrected:", uci_move)

                ##################################
                #   HANDLE VALID MOVES:        ###
                ##################################
                if uci_move in kkk:
                    print("uci_move is valid")
                    validity = "valid"
                    
                    
                    ##################################
                    # update FEN with uci_move       #

                    ##################################
                    
                    R = update_FEN(FEN,uci_move)
                    print("move_counter", move_counter)
                    print("half_move_counter", (move_counter -1)%2)
                    print("full_move_no", move_counter//2)

                    ####### Minmize Output ##########
                    subprocess.call(["clear"])
                    #################################

                    FEN_new = R[0]
                    print("\nFEN:", FEN)
                    print("FEN_new:", R[0])
                    print("last move", R[1], "was", validity)
                    
                    # if move_counter%2 ==0:
                    #     to_move = "White"
                    #     print("===> WHITE_to_move")
                    # if move_counter%2 ==1:
                    #     to_move = "Black"
                    #     print("===> BLACK_to_move")
                    
                    uci_move_list.append(uci_move)
                    # print("  uci move list:", uci_move_list)
                    # make_san_movelist_from_uci_sequence(uci_move_list and board)
                     
                    previous_LL = LL
                    # print("previous_LL", previous_LL)
                    
                    LL = board0.variation_san([chess.Move.from_uci(m) for m in uci_move_list])
                    
                    print("\nGame Notation (SAN):", LL)
                    last_san = LL.replace(previous_LL,"") # gives last entry of san moves 
                    
                    print("last san: " , last_san)
                    san_move_list.append(last_san)
                    
                    # print("san_move_list ...", san_move_list)  ## List includes move Nums for White, can be used for PGN construction
                                        
                    if "w " in FEN_new:
                        to_move = "White"
                        san_str = str(move_counter//2-1)  + ". ..." + san_move_list[-1]
                        time_used = round(time.time()- time000,1)
                        btime_list.append(time_used)
                        black_time = round(sum(btime_list),1)
                        ###print("time_list, secs", btime_list)
                        ###print("black_time:", black_time)
                    
                    if "b " in FEN_new:
                        to_move = "Black"
                        san_str = san_move_list[-1]
                        time_used = round(time.time()- time000,1)
                        wtime_list.append(time_used)
                        white_time = round(sum(wtime_list),1)
                        ###print("time_list (secs)", wtime_list)
                        ###print("white_time:", white_time)
                    
                    time000= time.time() # reset time_stamp for moves
                    ### print("san__str: ",san_str) # ppppp
                    
                    print("\n==> ", to_move + " to move")

                    # print(FEN_new[-1] ) # moves done from FEN_new

                    newboard = chess.Board(R[0])
                    best_move = eval(newboard)[3]
                                        
                    # ????? GEHT NICHT, ÜBERARBEITEN
                    # move1=chess.Move.from_uci(str(uci_move)) #### convert uci to san for a specific board position
                    # print("san_move",  move1)
                    # san_move = board.san(chess.Move(Z1, Z2))?
                    # san_move = board.san(Z1, Z2)) ?

                    #################################################################
                    # TEXT FOR INFO WINDOW                                          #
                    # TEXT FOR TERMiNAL                                             #
                    #################################################################

                    ### text0 = FEN+ "\n"
                    text1 = "New: " + R[0] # FEN_new
                    # print(text1)
                    text2 = "\n" + "last move " + R[1] + " was " + validity     
                    text3 = "\n\n" + san_str
                    text4 =  ""                                            
                    ### "\n\nGame Notation: " + LL
                    text5 = "\n\n==> now " + to_move + " to move"
                    text6 = "\nBest reply (0.1 sec) would be: " +  str(best_move)
                    valid_moves_now = legal_moves_2(R[0])
                    print("valid moves: ", valid_moves_now)
                    print(text6)
                    
                    ##################################################################
                    # enable/disable EVALUATION here
                    # print("EVAL (cp / dist to mate: )", str(eval(newboard)[5])[8:])       
                    ##################################################################

                    blanc_image2 = np.zeros((200, 1200, 3), np.uint8) # blanc image AUTOSIZE)
                    timex=(time.time() -timep)*1000
                    text7 = "\nTime used:" "    White " + str(white_time) + " secs" + "    Black " + str(black_time) + " secs" + "                                    " + str(int(timex)) + " msecs"

                    print(text7)
                    text = text1 + text2 + text3 + text4 + text5 + text6 + text7

                    print(datetime.today().strftime("%A, %B %d, %Y %H:%M:%S"))
                    print("san_move_list =" , san_move_list)                    
 
                    san_str= " ".join(san_move_list) # convert san_move_list to str
                    sss = str(san_str).replace(","," ") # remove ","
                    # subprocess.run("clear")
                    print("\n\nGame Notation: ", sss, end = "")
                    print()
                                        

                    ##############################################################
                    ### convert san_move_list for show_scoresheet:
                    ### 
                    ##############################################################
                    data1=  san_move_list
                    ### print(len(data1))

                    i=0
                    k=[]
                    while i < (len(data1)):
                        if i < len(data1)-1:
                            if i < 2:
                                zc1 = "  " + str(data1[i]).ljust(10)  + str(data1[i+1]).ljust(10)  # add missing space move "1"
                            if i >= 2:
                                zc1 = " "+ str(data1[i]).ljust(11)  + str(data1[i+1]).ljust(10)  # add missing space move "1"
                            
                            k.append(zc1)

                        else:
                            if i < 2:
                                k.append("  "+ str(data1[i]))
                            if i >= 2:
                                k.append(" " +str(data1[i]))
                        i=i+2

                    x= k 
                    ##############################################################
                    ### conversion finished
                    ##############################################################
                    
                    '''
                    ### working not as well, could be deleted
                    print(len(data1))
                    i=0
                    k=[]
                    while i < (len(data1)):
                        if i < len(data1)-1: 
                            z1 =  str(data1[i]).ljust(11)  + str(data1[i+1]).ljust(11)
                            # print(z1)
                            k.append(z1)
                        else: 
                            k.append(str(data1[i]))
                        i= i +2
                   # print(k)
                    x= k
                    '''

                    ###############################################################
                    ### uncomment to show core sheet                            ###
                    ###############################################################
                    show_scoresheet(x)
 
 

                    ###############################################################
                    ### END OF CYCLE correct moves                              ###
                    ###############################################################
                    take_back_counter = 0
                    # cv2.moveWindow(window_name, 1,1)
                    # cv2.imshow(window_name, blanc_image)obs plugins
                    
                
                #########################################################
                ### ERROR HANDLING
                ### (uci = "" oder not in Legal:moveList)  
                #########################################################
                else:
                    if str(uci_move) is "":
                        print("uci_move is none") 

                    print("\n",FEN, "\n",R[0])

                    if "w " in FEN:
                        ### print(move_counter-2)
                        to_move = "White"
                        # san_str = str((move_counter)%2 +1) +". ..." + san_move_list[-1]
                        opp_move= "Black"
                    if "b " in FEN:
                        # san_str = san_move_list[-1]
                        to_move = "Black"
                        opp_move = "White"
                    
                    ### subprocess.call(["clear"])
                    print("takeback_counter: ", take_back_counter)
                    inverted_uci_move = uci_move[2:4]+ uci_move[0:2]

                    if take_back_counter == 0 and last_move == uci_move:
                        
                        text1 = (
                            str(to_move) + " had to move" + "\nlever or p was pressed, but no " + to_move + 
                            " move was done! \nto resume undo " + opp_move  + " move (if done), than press opponents lever (or p) "
                            )
                        
                        print(text1)

                        
                        ### insert a check whether white pieces have moved

                    if take_back_counter == 0 and last_move != uci_move:
                        text1 = "Illegal " + str(to_move) + " move! " + "\nTo take back play " +  "'" +   str( inverted_uci_move) + "'" + " than press lever or p"
                        print(text1)


                    if take_back_counter == 1:
                        text1 = "now make a correct " + str(to_move) + " move and press lever again"
                        print(text1)

                      
                    text2 = ""
                    text3 = ""
                    text4 = ""
                    text5 = ""
                    text6 = ""
                    text7 = ""
                    text = text1 +text2 +text3 +text4 +text5 +text6 +text7
                    # blanc_image2 = np.zeros((200, 1200, 3), np.uint8) # blanc image AUTOSIZE)
                    move_counter = move_counter -1 
                    # take_back_move = str(uci_move[2] + str(uci_move[3])+ str(uci_move[0]) + str(uci_move[1]))
                    # print("to roll back move go:", take_back_move, ", press 'p' to confirm, than do a legal move, and confirm with 'p'")
                    take_back_counter = take_back_counter +1


                ###############################################################
                ### write game data to file                                 ###
                ###############################################################

                with open("FENFILE.txt","w") as f:
                    f.write("Game started: " + game_started +"\n")
                    f.write("Old FEN: " + FEN + "\n")
                    f.write("legal moves:" + kkk + "\n")
                    f.write("uci_move: " + uci_move + "\n")
                    f.write("SAN_move: " + san_str + "\n\n")
                    f.write("New FEN: " + R[0] + "\n")
                    f.write("Game: " +  str(LL) +" \n\n")
                    f.write("Move_No: " + str(move_counter//2) + "\n")
                    f.write("to_move: " + to_move + "\n")
                    f.write("valid moves_now: " + valid_moves_now +"\n")
                    f.write("best reply 0.1 secs: " + str(best_move) + "\n")
                    f.write("White_time: " + str(white_time) + " secs\n")
                    f.write("Black_time: " + str(black_time) + " secs\n")
                    f.write("game stopped: " + datetime.today().strftime("%A, %B %d, %Y %H:%M:%S") + "\n")                    
                    # f.write("Last analysed Image: " + str(img_name2))

                ##### new cycle with New_FEN
                last_move = uci_move
                FEN = R[0]
                time_start = time.time()    
                
                #####################################
                # generate png file from FEN:       #
                # runs fen-to-pgn                   #
                # ###################################
                
                commando = "./run2.sh" , FEN
                subprocess.run(commando)
                fen_image = cv2.imread("fen-to-png/output/result.png")# , cv2.IMREAD_GRAYSCALE)
                
                # now show lichess_link
                Lichess_pgn = str(LL).replace(" ","_")

                Lichess_URL = ("https://lichess.org/analysis/pgn/" + Lichess_pgn)
                print()
                print("Lichess_URL = ", Lichess_URL)


    cap.release()
    cv2.destroyAllWindows()
    return result3, result2, result1, Lichess_URL

def new_func():
    time_start = time.time()
    print(time_start)
    return time_start

    # # # result3 = cam_func()[0]
    # # # cap.release()
    # # # cv2.destroyAllWindows()            

'''
    elif cv2.waitKey(1) & 0xFF == ord("x"):
        file_name = "{}.jpg".format(move_counter-1)
        cv2.imwrite(file_name, img)
        # img1=cv2.imread(dir_path+'/boards/'+str(file_name))
'''    

def nothing(X):
        pass

def detect_position_of_pieces(diff):
    print("RUNNING detect position_of_pieces")
    diff_gray = cv2.cvtColor(diff,cv2.COLOR_BGR2GRAY)
    # value = thresold_calibreation(diff_gray)
    value= 10 ### was 42
    print("treshhold applied:",value)
    print()
    matrix,thresold = cv2.threshold(diff_gray,value,255,cv2.THRESH_BINARY)
    cnts,_ = cv2.findContours(thresold, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    # print("len(cnts)", len(cnts))
    # uncomment next line for result in color, very peculiar, gray is better

    diffc=cv2.cvtColor(diff_gray,cv2.COLOR_GRAY2BGR)
    piece_pos=[]
    area_list=[]
    piece_count=0
    for c in cnts:
        area = cv2.contourArea(c)
        
        if area > 500:
            area_list.append(area)
            piece_count = piece_count+1
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(diffc, (x,y), (x+w, y+h), (0, 0, 255), 3)

            ### UNCOMMENT TO PRINT RESULTS ON SCREEN
            #print("\n area", piece_count, ":", area)
            #print("x", x, "y", y)
            #print ("width", w, "height", h)
            #print("rectangle_pos (x,y)", x+w, y+h)
            
            piece_pos.append(x+int(w/2))
            piece_pos.append(y+int(h/2))
            ### print("piece_positions:", piece_pos)


    ############################################################
    ### uncomment for debug                                    #
    ############################################################
    # print("min_area", min(area_list))
    # print("max_area", max(area_list))    

    # print("piece_pos:",piece_pos[0:])
    #subprocess.call(["clear"])
    # print("\n", piece_count, "Pieces detected")
    
    if (piece_count > 16):
        print(piece_count, "e_Pieces")
        print("INVALID POSITION")
        print()
        
    # print("pieces (x,y):", piece_pos)

    ############################################################
    ### Function to generate the list of pieces (3.2023)       #
    ############################################################
    
    L1=["a","b","c","d","e","f","g","h"]
    L2=["8","7","6","5","4","3","2","1"]

    values=range(2*(piece_count) -1)
    piecelist=[]
    for i in values:
        if i% 2==0:
            # print(L1[int(piece_pos[i]/100)],L2[int(piece_pos[i+1]/100)])
            a = L1[int(piece_pos[i]/100)],L2[int(piece_pos[i+1]/100)]
            a_1="".join(c for c in str(a) if c.isalnum())
            piecelist.append(a_1)

    npiecelist = "".join(c for c in str(piecelist) if c.isalnum()) ## not needed

    print(piece_count, "Pieces found (piecelist): ", "\n",piecelist, "\n")
    return piecelist

def ShowSVG():
    return
# '''
# ### konvertieren von svg files
# image=pyvips.Image.new_from_file("img.svg", dpi = 300)
# image.write_to_file(img.png)
# '''

FEN0  = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
board = chess.Board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

# '''
# ### snippet SVG
# boardsvg = board.(board((FEN) , size=600, coordinates =True)
# with open('temp.svg', 'w') as outputfile:
#    outputfile.write(boardsvg)
#    time.sleep(0.1)
#    os.startfile('temp.svg')
# '''

'''
def make_san_movelist_from_uci_sequence(list):        
    list=list
    board.variation_san([chess.Move.from_uci(m) for m in [list]])
    LL=board.variation_san([chess.Move.from_uci(m) for m in [list]])
    print("  San Moves :", LL, "\n")
    return LL
'''

if __name__ == "__main__":

    FEN = FEN0
    testimage = cam_func(FEN)[0]
    # if neccesary write result3.jpg
    # # writeStatus = cv2.imwrite("result3.jpg\n",result3) # write resul3 to file ,~ 60 msecs
    # # if writeStatus is True:
    # #     print("\n====> image written as '"'result3.jpg'"' \n", )
    # # else:
    # #     print("Problem saving image")
    # # # print(" result3 shape:", result3.shape)

    # # # testpic=cv2.imread("result3.jpg")
    # # # cv2.imshow("Test-Image" ,testpic)
    # # # cv2.waitKey(1)
    # # # cv2.destroyAllWindows()
    # # # cap.release()3 
    ################################# detect move starts here ##############################
    time0=time.time()
    # # # testimage  ### image to test
    # # # piecelist = detect_position_of_pieces(testimage)
    # # # print("Original FEN is: ", FEN)  
    # # # legal_uci = legal_moves_2(FEN)
    # # # print("legal_uci moves:", legal_uci)
    # z=move_pair_in_list(legal_uci, uci_move_x)
    # print(z)
    '''
    cv2.imshow("Name", testimage)
    cv2.waitKey(0)
    cap.release()
    cv2.destroyAllWindows()
    '''
    # # # R= detect_moved_pieces()
    # # # # subprocess.call("clear")
    
    # # # print("New FEN", R[0])
    # # # print("last_uci_move", R[1])
    # # # FEN = R[0] ### newFEN
    # # # list = R[1]
    
    # # # san_move = make_san_movelist_from_uci_sequence(list)
    # # # print(san_move)
    
    time_now=time.time()
    time_spent= time_now -time0
    print(int(time_spent *1000), "msecs")

    with open("FENFILE.txt") as f:
        s = f.read()
        list_doc = s.split("\n")
        print(s)
        new_FEN  = list_doc[6][9:]
        game_pgn = Fen=list_doc[7][6:]
        

    Lichess_pgn = game_pgn.replace(" ","_")
    
    subprocess.run("clear")
    print()
    print("game data        = ", "file://fenfile.txt", "\n")
    print("score_sheet      = ", "file://output.log", "\n" )
    print("Replay with Lichess  = ", ("https://lichess.org/analysis/pgn/" + Lichess_pgn), "\n")

    #############################################################################
    # Lichess:                                                                  #
    # To analyse a position or a line, just construct an analysis board URL:    #
    # https://lichess.org/analysis/pgn/e4_e5_Nf3_Nc6_Bc4_Bc5_Bxf7+              #
    # see https://lichess.org/api#tag/Games/operation/gamesExportIds etc        #
    #############################################################################
    
    #############################################################################
    # Lichess                                                                   #
    # To analyse a FEN position:                                                #
    # https://lichess.org/analysis/new_Fen                                      #
    #############################################################################

    
    url1 = ("https://lichess.org/analysis/" + new_FEN)
    url2 = ("https://lichess.org/analysis/pgn/" + Lichess_pgn) # this is best

    webbrowser.open_new(url2)
    print("done ...")
    quit()
