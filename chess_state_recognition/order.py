import numpy as np
import imutils
# import the necessary packages
from scipy.spatial import distance as dist
import numpy as np
import cv2


def load():
    #### load cornersmb.npy
     
    corners=np.load("cornersmb.npy") 
    print("corners loaded from cornernsmb.npy")
    ###print("Array of all chessboard corners:\n", corners, "\n")

    ####  find outer corners:
    c1 = corners[0][0]
    c2 = corners[8][0]
    c3 = corners[8][8]
    c4 = corners[0][8]

    ### if needed invert corners (xy):
    c1inv = c1[::-1]
    c2inv = c2[::-1]    
    c3inv = c3[::-1]
    c4inv = c4[::-1]

    #print("\nOuter corners from cornersmb.npy (clockwise, xy):")
    #print("corner 1 x,y", c1inv)
    #print("corner 2 x,y", c2inv)
    #print("corner 3 x,y", c3inv)
    #print("corner 4 x,y", c4inv)

    ### make arry and invert yx to xy:
    
    pts =np.array([[c1[1], c1[0]], [c2[1], c2[0]], [c3[1], c3[0]], [c4[1], c4[0]]] )

    # print ("\npts (clockwise, xy):\n", pts)
    return pts
pts = load()

def order_points_2(pts):
    # better Version 2016, from https://pyimagesearch.com/2016/03/21/ordering-coordinates-clockwise-with-python-and-opencv/
	# sort the points based on their x-coordinates
	xSorted = pts[np.argsort(pts[:, 0]), :]
	# grab the left-most and right-most points from the sorted
	# x-roodinate points
	leftMost = xSorted[:2, :]
	rightMost = xSorted[2:, :]
	# now, sort the left-most coordinates according to their
	# y-coordinates so we can grab the top-left and bottom-left
	# points, respectively
	leftMost = leftMost[np.argsort(leftMost[:, 1]), :]
	(tl, bl) = leftMost
	# now that we have the top-left coordinate, use it as an
	# anchor to calculate the Euclidean distance between the
	# top-left and right-most points; by the Pythagorean
	# theorem, the point with the largest distance will be
	# our bottom-right point
	D = dist.cdist(tl[np.newaxis], rightMost, "euclidean")[0]
	(br, tr) = rightMost[np.argsort(D)[::-1], :]
	# return the coordinates in top-left, top-right,
	# bottom-right, and bottom-left order
	return np.array([tl, tr, br, bl])

#### sort corners clocwise top left, top right, bottom right, bottom left:
pts = order_points_2(pts)

#### pts = pts.astype('float64')
#### print(pts)
#### print("shape:", pts.shape, "\ndtype:", pts.dtype)

####  save corners as array "pts1.npy":
np.save("pts1.npy", pts)
print("=> Array of outer board corners xy sorted clockwise written to ’pts1’:")
print(pts)
#print("shape:", pts.shape, "\ndtype:", pts.dtype)

###pts_list= pts.tolist()
###print("pts_list:", pts_list)

###generate corners4 (array)  from pts_list (list)
###corners4= np.array(pts_list)
###print("corners4\n", corners4)
###print (corners4.dtype)
