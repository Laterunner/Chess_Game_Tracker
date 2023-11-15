import numpy as np 
import cv2 
import time
import subprocess

subprocess.call(["clear"])

# creating the videocapture object 
# and reading from the input file 
# Change it to 0 if reading from webcam 

### taken from https://www.geeksforgeeks.org/python-displaying-real-time-fps-at-which-webcam-video-file-is-processed-using-opencv/


## img_resize1 = (1920,1080)
## img_resize1 = (1920,1440)
## img_resize1 = (1280, 960)
# img_resize1 = (960, 720)
img_resize1 = (720,576) # set o/p image size
# img_resize1 = (640,480)
# img_resize1 = (320,240)
img_resize1 =(480,320)


def fps(camNo):
    ...
    cam1  = 'v4l2src device=/dev/video0 ! videoconvert ! appsink'
    cam2 = 'v4l2src device=/dev/video0 ! jpegdec ! videoconvert! appsink'
    cam3  = 'v4l2src device=/dev/video1 ! videoconvert ! appsink'
    cam4 = 'v4l2src device=/dev/video1 ! jpegdec ! videoconvert! appsink'
    cam5  = 'v4l2src device=/dev/video2 ! videoconvert ! appsink'
    cam6 = 'v4l2src device=/dev/video2 ! jpegdec ! videoconvert! appsink'
    ...
    cap = cv2.VideoCapture(camNo)
    subprocess.call(["clear"])
    # used to record the time when we processed last frame 
    prev_frame_time = 0
    
    # used to record the time at which we processed current frame 
    new_frame_time = 0
    
    # Reading the video file until finished 
    while(cap.isOpened()): 
    
        # Capture frame-by-frame 
    
        ret, frame = cap.read() 
    
        # if video finished or no Video Input 
        if not ret: 
            break
    
        # Our operations on the frame come here 
        image = frame
    
        # resizing the frame size according to our need 
        image = cv2.resize(image, img_resize1)
              
        ############################################################### 
        # to turn cam choose 0 = 90, 1 = 180,  2= 270 degree clockwise

        # image = cv2.rotate(image,cv2.ROTATE_90_CLOCKWISE)
        # image = cv2.rotate(image,0) # == ROTATE_90_CLOCKWISE

        # image = cv2.rotate(image,cv2.ROTATE_180)
        # image= cv2.flip(image,-1)   # == ROTATE_180 
        # image = cv2.rotate(image,1) # == ROTATE_180

        # image = cv2.rotate(image,cv2.ROTATE_90_COUNTERCLOCKWISE)
        # image = cv2.rotate(image,2) # == cv2.ROTATE_90_COUNTERCLOCKWISE
        
        ##############################################################
    
        # font which we will be using to display FPS 
        font = cv2.FONT_HERSHEY_SIMPLEX 
        # time when we finish processing for this frame 
        new_frame_time = time.time() 
    
        # Calculating the fps 
    
        # fps will be number of frame processed in given time frame 
        # since their will be most of time error of 0.001 second 
        # we will be subtracting it to get more accurate result 
        fps = 1/(new_frame_time-prev_frame_time) 
        prev_frame_time = new_frame_time 
    
        # converting the fps into integer 
        fps = int(fps)
    
        # converting the fps to string so that we can display it on frame 
        # by using putText function 
        fps = str(fps)
        fps = fps + " fps device" + str(camNo)
        # puting the FPS count on the frame 
        cv2.putText(image, fps, (7,20), font, 0.5, (100, 255, 0), 1 , cv2.LINE_AA) 
            # displaying the frame with fps 
        
        cv2.imshow('CAM1, press "Q" to quit', image)
        cv2.moveWindow('CAM1, press "Q" to quit', 0, 0)
    
        # press 'Q' if you want to exit 
        if cv2.waitKey(1) & 0xFF == ord('q'): 
            break
    
    # When everything done, release the capture 
    cap.release() 
    # Destroy the all windows now 
    cv2.destroyAllWindows()

if __name__ == "__main__":
    ##Beispiel:
    fps(0)
    pass
