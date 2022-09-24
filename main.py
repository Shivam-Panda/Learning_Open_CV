
import cv2 as cv
import numpy as np

cap = cv.VideoCapture(0)

def nothing(x):
    pass

cv.namedWindow('result')
cv.createTrackbar('h_low', 'result', 0, 179, nothing)
cv.createTrackbar('s_low', 'result', 0, 255, nothing)
cv.createTrackbar('v_low', 'result', 0, 255, nothing)

cv.createTrackbar('h_upper', 'result', 0, 179, nothing)
cv.createTrackbar('s_upper', 'result', 0, 255, nothing)
cv.createTrackbar('v_upper', 'result', 0, 255, nothing)

while(1):
    h_low=  cv.getTrackbarPos('h_low', 'result')
    s_low=  cv.getTrackbarPos('s_low', 'result')
    v_low=  cv.getTrackbarPos('v_low', 'result')

    h_upper =  cv.getTrackbarPos('h_upper', 'result')
    s_upper =  cv.getTrackbarPos('s_upper', 'result')
    v_upper =  cv.getTrackbarPos('v_upper', 'result')

    # Take each frame
    _, frame = cap.read()
    
    # Convert BGR to HSV
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    # define range of color in HSV
    lower_red = np.array([h_low, s_low, v_low])
    upper_red = np.array([h_upper, s_upper, v_upper])

    # Threshold the HSV image to get only blue colors
    red_mask = cv.inRange(hsv, lower_red, upper_red)


    # Bitwise-AND mask and original image
    final_res = cv.bitwise_and(frame,frame, mask= red_mask)

    cv.imshow('frame',frame)
    cv.imshow('red mask',red_mask)
    cv.imshow('final res',final_res)

    k = cv.waitKey(5) & 0xFF
    if k == 27:
        break

cv.destroyAllWindows()
