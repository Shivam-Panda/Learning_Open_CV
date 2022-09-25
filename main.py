
import cv2 as cv
import numpy as np

cap = cv.VideoCapture(0)

def nothing(x):
    pass

cv.namedWindow('result')
# cv.createTrackbar('h_low', 'result', 0, 179, nothing)
# cv.createTrackbar('s_low', 'result', 0, 255, nothing)
# cv.createTrackbar('v_low', 'result', 0, 255, nothing)

# cv.createTrackbar('h_upper', 'result', 0, 179, nothing)
# cv.createTrackbar('s_upper', 'result', 0, 255, nothing)
# cv.createTrackbar('v_upper', 'result', 0, 255, nothing)

cv.createTrackbar('x', 'result', 0, 1000, nothing)
cv.createTrackbar('y', 'result', 0, 1000, nothing)
cv.createTrackbar('radius', 'result', 0, 1000, nothing)

while(1):
    # h_low=  cv.getTrackbarPos('h_low', 'result')
    # s_low=  cv.getTrackbarPos('s_low', 'result')
    # v_low=  cv.getTrackbarPos('v_low', 'result')

    # h_upper =  cv.getTrackbarPos('h_upper', 'result')
    # s_upper =  cv.getTrackbarPos('s_upper', 'result')
    # v_upper =  cv.getTrackbarPos('v_upper', 'result')

    x = cv.getTrackbarPos('x', 'result')
    y = cv.getTrackbarPos('y', 'result')
    radius = cv.getTrackbarPos('radius', 'result')

    # Take each frame
    _, frame = cap.read()
    
    # Convert BGR to HSV
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    # define range of color in HSV
    # lower_red = np.array([h_low, s_low, v_low])
    # upper_red = np.array([h_upper, s_upper, v_upper])

    # Threshold the HSV image to get only blue colors
    # red_mask = cv.inRange(hsv, lower_red, upper_red)

    # Shaped Masks
    circle_mask = np.zeros(frame.shape[:2], dtype="uint8")
    cv.circle(circle_mask, (x, y), radius, 255, -1)
    rect_mask = np.zeros(frame.shape[:2], dtype="uint8")
    cv.rectangle(rect_mask, (x, y), (x+200, y+200), 255, -1)
    
    circle_final = cv.bitwise_and(frame, frame, mask=circle_mask)
    rect_final = cv.bitwise_and(frame, frame, mask=rect_mask)

    cv.imshow('mask', circle_mask)
    cv.imshow('final', circle_final)
    cv.imshow('rect final', rect_final)
    cv.imshow('rect mask', rect_mask)

    # Adding Two Different Masked Images
    comb = cv.bitwise_or(circle_final, rect_final)
    cv.imshow('final Comb', comb)


    # Bitwise-AND mask and original image
    # final_res = cv.bitwise_and(frame,frame, mask= red_mask)

    cv.imshow('frame',frame)
    # cv.imshow('red mask',red_mask)
    # cv.imshow('final res',final_res)

    k = cv.waitKey(5) & 0xFF
    if k == 27:
        break

cv.destroyAllWindows()
