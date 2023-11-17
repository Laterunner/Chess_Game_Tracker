

###################################################################################
## SETUP for TRACK CHESS GAMES V1
# dir+ = ./numpy_saved/hello
# 1. map_function writes to dir+
# 2. cam_pos() saves 000image.bin for corner detection, 
# 3. ./corner_detect.sh (Murat Sahins corner detector) to get corners cordinates
# loads 
# 4 warp() loads from murats 
#    "/home/marius/Desktop/pyprojects/csr-jet/chess_state_recognition/cornersmb.npy"
# 5. warp saves npz files to dir+ 
# 6. show_boxes() loads from dir+ cornersmn.npy 
# 7. calibrate() writes setup.bin to 

###################################################################################





###################################################################################
## Import Libraries
###################################################################################
from multiprocessing.connection import answer_challenge
import os
from platform import release
import chess
import chess.engine
import cv2
import numpy as np
import sys
import subprocess
import fps
import pickle

###################################################################################
## Import files
###################################################################################
# from detect_points import get_points ### only used with manual corner detection
from detect_points import get_points_800
from read_warp_img import get_warp_img
import cvzone


###################################################################################
## Define Main Variables
###################################################################################

points = []    # contains chess board corners points
boxes = np.zeros((8,8,4),dtype=int)    # contains top-left and bottom-right point of chessboard boxes
# fen_line = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR' # fen line of chess board
# board = chess.Board(fen=fen_line) # object of chess board

dir_path = os.path.dirname(os.path.realpath(__file__))+"/numpy_saved" # path of current directory
cam = cv2.VideoCapture(0) ### Panasonic cam via USB
img_resize = (800, 800)

subprocess.call(["clear"])
image = []

### no engine used in setup
### engine = chess.engine.SimpleEngine.popen_uci("/home/marius/Desktop/pyprojects/engine_dir/sf12nnue/stockfish")  # SF12NNUE

'''
### delete
chess_board = []   # it will store chess board matrix
player_bool_position =[]
bool_position = np.zeros((8,8),dtype=int)
number_to_position_map = []
last_move = ""
game_img = ""
fen_line = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR' # fen line of chess board
board = chess.Board(fen=fen_line) # object of chess board
'''
###################################################################################
## Code For Run Program
###################################################################################
'''
print("Enter Directory Name, i.e. ""(hello)"" ")
code = str(input(""))
'''
code = "hello"
dir_path += "/"+code
if not os.path.exists(dir_path):
    os.makedirs(dir_path)

###################################################################################
## Define Functions
###################################################################################

## map function for map values for (0,0)-> (8,a) , (0,1)-> (8,b).... so on
def map_function():
    map_position = {}
    x,y=0,0
    for i in "87654321":
        for j in "abcdefgh":
            map_position[j+i] = [x,y]
            y = (y+1)%8
        x = (x+1)%8
    np.savez(dir_path+"/map_position.npz",**map_position)
map_function()
map_position =np.load(dir_path+"/map_position.npz")   # map move values for (0,0)-> (8,a) , (0,1)-> (8,b).... so on


def cam_pos():
    ###################################################################################
    ## camera position calibration
    ###################################################################################

    while True:
        '''
        
        print("Do you want to set camera Position[y/n] : ",end=" ")
        answer = str(input())
        '''
        answer = "y"
        
        if answer == "" or answer == "Y" or answer =="y":
            print("Press q for exit : ")
            while True:
                ## show frame from camera and set positon by moving camera
                flag , img = cam.read()
                img = cv2.resize(img,(640,480))
                # cv2.rotate(img, cv2.ROTATE_180)
                if flag:
                    
                    cv2.namedWindow("Set camera position")
                    cv2.moveWindow("Set camera position", 0,0)
                    cv2.imshow("Set camera position",img)
                    k = cv2.waitKey(1)
                    
                    
                    if k == ord('q'):
                        img = cv2.resize(img,(800,800))
                        cv2.imwrite("000image.png", img)
                        print("000image.png written in working directory, now running external prog")
                        subprocess.run(["./corner_detect.sh"], shell=True)
                        cv2.destroyAllWindows()
                        break
            break
        '''
        elif answer == "n" or answer == "N":
            print("\nHope that camera position already set...\n")
            break
        else:
            print("Invalid Input")
        '''
    return

#cam_pos()



def warp():
    ###################################################################################
    ## Image warp_perspective
    ###################################################################################

    while True:
        '''
        print("DO you want to warp perspective image[y/n] :",end=" ")
        answer = str(input())
        '''
        answer = "y"
        ret , img = cam.read()
        img =   cv2.resize(img,(800,800))
        
        ## img =   cv2.resize(img,(640,480))
        width,height = 800,800
        ##width,height = 640, 480
        if answer == "y" or answer == "Y" or answer == "":
            # Reading from myfile.txt, corners from "chess_state_recognition"
            
            
            
            '''
            ######################## TO BE DELETED, FOR TEST ONLY    ###############################################
            
            with open("/home/marius/Desktop/pyprojects/csr-jet/chess_state_recognition/myfile.txt", "r+") as file1:
                Reading form a file
                z= file1.readlines()[1]

            print("CORNERS from myfiles.txt:")
            print(z)
            print()
            
            ########################################################################################################
            '''
            corn  =np.load("./chess_state_recognition/cornersmb.npy")
            print(np.shape(corn))

          ##TEST
            c1 = corn[0][0]
            c2 = corn[8][0]
            c3 = corn[8][8]
            c4 = corn[0][8]

            # print(corn)

            print()
            warp_points_ =np.float32([[c1[1],c1[0],], 
                    [c2[1] , c2[0],],
                    [c4[1], c4[0],],
                    [c3[1], c3[0],]])
            print("warp_points_from_pts\n", warp_points_)
            print("-------------")

            #########################################################################################################
            '''
            ### only for manual corner detection
            warp_points = get_points(img,4)
            print("warp_points from mouseclicks:", warp_points)
            print("warp_points:", warp_points[0:])
            
            
            pts1 = np.float32([[warp_points[0][0],warp_points[0][1]],
                            [warp_points[1][0],warp_points[1][1]],
                            [warp_points[3][0],warp_points[3][1]],
                            [warp_points[2][0],warp_points[2][1]]])
            '''

            pts1 = warp_points_            
            pts2 = np.float32([[0,0],[width,0],[0,height],[width,height]])
            print()
            print("pts1\n",pts1)
            print()
            print("pts2\n", pts2)
            
            np.savez(dir_path+"/chess_board_warp_prespective.npz",pts1=pts1,pts2=pts2)
            
            result = get_warp_img(img,dir_path,img_resize)
            '''
            cv2.imshow("result",result)
            cv2.waitKey(0)
            '''
            cv2.destroyAllWindows()
            break
        elif answer == "n" or answer == "N":
            result = get_warp_img(img,dir_path,img_resize)
            cv2.imshow("result",result)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            break
        else:
            print("Enter valid input")

    ###################################################################################
    ## calibrate points for chess corners
    ###################################################################################
    while True:
            '''
            print("do you want to calculate and save new Points for corners [y/n]:",end=" ")
            answer = str(input())
            '''
            
            answer = "y"
            if answer == "y" or answer == "Y" or answer =="":
                print("RUNNING getpoints_800 from image")
                get_points_800()
                points = np.load(dir_path+'/chess_board_points.npz')['points']
                break

            ''' # deactivated
            elif answer == "n" or answer == "N":
                # do some work
                points = np.load(dir_path+'/chess_board_points.npz')['points']
                print("points.npz loaded successfully")
                break
            else:
                print("something wrong input")
            '''

    ###################################################################################
    ## Define Boxes
    ###################################################################################
    for i in range(8):
        for j in range(8):
            boxes[i][j][0] = points[i][j][0]
            boxes[i][j][1] = points[i][j][1]
            boxes[i][j][2] = points[i+1][j+1][0]
            boxes[i][j][3] = points[i+1][j+1][1]

    np.savez(dir_path+"/chess_board_Box.npz",boxes=boxes)
    return

# warp()

def view_boxes():
    ###################################################################################
    ## View Boxes
    ###################################################################################
    while True:
        '''
        print("Do you want to see the Chess board with named squares? [y/n]:",end=" ")
        ans = str(input())
        '''
        answer = "y"
        if answer == 'y' or answer == "Y":
            # show boxes
            ret , img = cam.read()
            img =   cv2.resize(img,(800,800))
            img = get_warp_img(img,dir_path,img_resize)
            img_box = img.copy()
            for i in range(8):
                for j in reversed(range(8)):
                    box1 = boxes[i,j]
                    cv2.rectangle(img_box, (int(box1[0]), int(box1[1])), (int(box1[2]), int(box1[3])), (255,0,0), 2)
                    cv2.putText(img_box,"{}{}".format(chr(j+97),8-i),(int(box1[2])-70, int(box1[3])-50),cv2.FONT_HERSHEY_SIMPLEX,1.0,(0,0,0),2)
                    cv2.imshow("img",img_box)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            break
        elif answer == 'N' or answer == "n":
            print("ok, got it you don't want to see boxes")
            break
        else:
            print("Enter valid input")

    return


def empty(a):
    pass


def calibrate(): ## usage calibrate(f ,w,b)

    ###Load preset values from setup.bin

    ### with open('setup.bin', 'rb') as f:
    with open("setup.bin", 'rb') as f:



        L3 = pickle.load(f)
    print("L3 loaded from setup.bin L3:")
    print(L3)
    # L3=[h_min, s_min, v_min, h_max, s_max, v_max, h_min2, s_min2, v_min2, h_max2, s_max2, v_max2]

    k0=int(L3[0])
    k1=int(L3[1])
    k2=int(L3[2])
    k3=int(L3[3])
    k4=int(L3[4])
    k5=int(L3[5])
    k6=int(L3[6])
    k7=int(L3[7])
    k8=int(L3[8])
    k9=int(L3[9])
    k10=int(L3[10])
    k11=int(L3[11])

    ### Filter red (black) pieces
    cv2.namedWindow("HSV")
    cv2.moveWindow("HSV",0,0)
    cv2.resizeWindow("HSV",640,240)


    cv2.createTrackbar("HUE Min","HSV",k0,179,empty)
    cv2.createTrackbar("SAT Min","HSV",k1,255,empty)
    cv2.createTrackbar("VALUE Min","HSV",k2,255,empty)
    cv2.createTrackbar("HUE Max","HSV",k3,179,empty)
    cv2.createTrackbar("SAT Max","HSV",k4,255,empty)
    cv2.createTrackbar("VALUE Max","HSV",k5,255,empty)

    #xxx Filter yellow (White Pieces)
    cv2.createTrackbar("HUE Min2","HSV",k6,179,empty)
    cv2.createTrackbar("SAT Min2","HSV",k7,255,empty)
    cv2.createTrackbar("VALUE Min2","HSV",k8,255,empty)
    cv2.createTrackbar("HUE Max2","HSV",k9,179,empty)
    cv2.createTrackbar("SAT Max2","HSV",k10,255,empty)
    cv2.createTrackbar("VALUE Max2","HSV",k11,255,empty)
    '''
    cv2.createTrackbar("HUE Min","HSV",156,179,empty)
    cv2.createTrackbar("SAT Min","HSV",125,255,empty)
    cv2.createTrackbar("VALUE Min","HSV",38,255,empty)
    cv2.createTrackbar("HUE Max","HSV",179,179,empty)
    cv2.createTrackbar("SAT Max","HSV",255,255,empty)
    cv2.createTrackbar("VALUE Max","HSV",255,255,empty)

    #xxx Filter yellow (White Pieces)
    cv2.createTrackbar("HUE Min2","HSV",0,179,empty)
    cv2.createTrackbar("SAT Min2","HSV",164,255,empty)
    cv2.createTrackbar("VALUE Min2","HSV",190,255,empty)
    cv2.createTrackbar("HUE Max2","HSV",40,179,empty)
    cv2.createTrackbar("SAT Max2","HSV",255,255,empty)
    cv2.createTrackbar("VALUE Max2","HSV",255,255,empty)
    '''

    while True:
        _, img = cam.read()

        imgHsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

        # for red (black) pieces
        h_min = cv2.getTrackbarPos("HUE Min","HSV")
        h_max = cv2.getTrackbarPos("HUE Max", "HSV")
        s_min = cv2.getTrackbarPos("SAT Min", "HSV")
        s_max = cv2.getTrackbarPos("SAT Max", "HSV")
        v_min = cv2.getTrackbarPos("VALUE Min", "HSV")
        v_max = cv2.getTrackbarPos("VALUE Max", "HSV")

        # for yellow (white) pieces
        h_min2 = cv2.getTrackbarPos("HUE Min2","HSV")
        h_max2 = cv2.getTrackbarPos("HUE Max2", "HSV")
        s_min2 = cv2.getTrackbarPos("SAT Min2", "HSV")
        s_max2 = cv2.getTrackbarPos("SAT Max2", "HSV")
        v_min2 = cv2.getTrackbarPos("VALUE Min2", "HSV")
        v_max2 = cv2.getTrackbarPos("VALUE Max2", "HSV")

        ### for red (black pieces)
        lower = np.array([h_min,s_min,v_min])
        upper = np.array([h_max,s_max,v_max])
        mask1 = cv2.inRange(imgHsv,lower,upper)
        result1 = cv2.bitwise_and(img,img, mask = mask1)

        ### for yellow (white pieces)
        lower2 = np.array([h_min2,s_min2,v_min2])
        upper2 = np.array([h_max2,s_max2,v_max2])
        mask2 = cv2.inRange(imgHsv,lower2,upper2)
        result2 = cv2.bitwise_and(img,img, mask = mask2)


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
        ##cv2.moveWindow("Horizontal Stacking", 440,0)

        ###alternative mit stackimages
        imgStacked=cvzone.stackImages([img,result1, result2,],3, 0.7)
        cv2.imshow("image",imgStacked)
        cv2.moveWindow("image", 480, 100)

        ### print("running ....", " q to quit")

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # cam.release()
    # cv2.destroyAllWindows()
    # ### subprocess.call("clear")

    L1=[h_min, s_min, v_min, h_max, s_max, v_max, h_min2, s_min2, v_min2, h_max2, s_max2, v_max2]

    with open("setup.bin", "wb") as f: 
        pickle.dump(L1,f)
        print("Data dumped to setup.bin:")
        print(L1)
    return L1

if __name__ == "__main__":
    cam_pos()
    warp()
    cv2.destroyAllWindows()    
    view_boxes()
    cv2.destroyAllWindows()
    calibrate()
    cam.release
    cv2.destroyAllWindows()
    subprocess.run("clear")
    print("CALIBRATION AND SETUP IS DONE")
    sys.exit("NOW RUN cptestx.py")
