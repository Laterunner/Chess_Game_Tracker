import cv2
import numpy as np
import os 
ix,iy = -1,-1
img = 0 

###################################################################################
## Code For Detect corner points 
###################################################################################

def draw_circle(event,x,y,flags,param):
    global ix,iy
    if event == cv2.EVENT_LBUTTONDBLCLK:
        cv2.circle(img,(x,y),5,(0,0,255),-1)
        ix,iy = x,y

def get_points(image,numOfPoints):
    global img 
    img = image.copy()
    img = cv2.resize(img,(800, 800))   
    width, height = image.shape[:2]
    cv2.namedWindow("image")
    cv2.setMouseCallback("image",draw_circle)
    points = []
    print("Press a for add point : ")
    while len(points) != numOfPoints:
        cv2.imshow("image",img)
        k = cv2.waitKey(1)
        if k == ord('a'):
            points.append([int(ix),int(iy)])
            cv2.circle(img,(ix,iy),5,(0,255,0),-1)
    cv2.destroyAllWindows()
    print("corners:", list(points))
    return list(points)


def get_points_800():
    x,y = 0 ,0
    points=[]
    for i in range(9):
        L=[[0,y], [100,y],[200,y],[300,y],[400,y],[500,y],[600,y],[700,y],[800,y]]
        y=y+100
        points.append(list(L))
    cv2.destroyAllWindows()
    print("got points")
    return list(points)

if __name__ == "__main__":
    # get_points_800()
    pass

