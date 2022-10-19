import cv2
import numpy as np

cap = cv2.VideoCapture(0)

def nothing(x):
    pass

cv2.namedWindow('result')
cv2.createTrackbar('h_low', 'result', 0, 179, nothing)
cv2.createTrackbar('s_low', 'result', 0, 255, nothing)
cv2.createTrackbar('v_low', 'result', 0, 255, nothing)

cv2.createTrackbar('h_upper', 'result', 0, 179, nothing)
cv2.createTrackbar('s_upper', 'result', 0, 255, nothing)
cv2.createTrackbar('v_upper', 'result', 0, 255, nothing)

while True:
    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    h_low=  cv2.getTrackbarPos('h_low', 'result')
    s_low=  cv2.getTrackbarPos('s_low', 'result')
    v_low=  cv2.getTrackbarPos('v_low', 'result')

    h_upper =  cv2.getTrackbarPos('h_upper', 'result')
    s_upper =  cv2.getTrackbarPos('s_upper', 'result')
    v_upper =  cv2.getTrackbarPos('v_upper', 'result')

    low_orange = np.array([h_low,s_low,v_low])
    high_orange = np.array([h_upper,s_upper,v_upper])

    mask = cv2.inRange(hsv, low_orange, high_orange)
    kernel = np.ones((5,5), np.uint8)
    mask = cv2.erode(mask, kernel)

    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 400:
            cv2.drawContours(frame, [cnt], 0, (0, 0, 0), 5)

    cv2.imshow("Frame", frame)
    cv2.imshow("Mask", mask)

    key = cv2.waitKey(1)
    if key == 27:
        break
    
cap.release()    
cv2.destroyAllWindows()
