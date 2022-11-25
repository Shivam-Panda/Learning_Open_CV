import math

import cv2
import numpy as np

y_int = 2848.499607135
slope = -60.20202691675

'''
Data Values
36" -> 681.218660968661
24" -> 1403.6509615384616
0" -> 2848.499607135

y = -60.20202691675x + 2848.499607135
'''

objects = []

cap = cv2.VideoCapture(0)

def find_mean_point(approx):
    x_vals = []
    y_vals = []
    for i in approx:
        x_vals.append(i[0])
        y_vals.append(i[1])
    return (sum(x_vals)/4, sum(y_vals)/4)


def distance_from_camera(area):
    return (area - y_int)/slope

# def nothing(x):
#     pass

# cv2.namedWindow('result')
# cv2.createTrackbar('h_low', 'result', 0, 179, nothing)
# cv2.createTrackbar('s_low', 'result', 0, 255, nothing)
# cv2.createTrackbar('v_low', 'result', 0, 255, nothing)

# cv2.createTrackbar('h_upper', 'result', 0, 179, nothing)
# cv2.createTrackbar('s_upper', 'result', 0, 255, nothing)
# cv2.createTrackbar('v_upper', 'result', 0, 255, nothing)

areas = []

while True:
    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # h_low=  cv2.getTrackbarPos('h_low', 'result')
    # s_low=  cv2.getTrackbarPos('s_low', 'result')
    # v_low=  cv2.getTrackbarPos('v_low', 'result')

    # h_upper =  cv2.getTrackbarPos('h_upper', 'result')
    # s_upper =  cv2.getTrackbarPos('s_upper', 'result')
    # v_upper =  cv2.getTrackbarPos('v_upper', 'result')

    low_orange = np.array([18,82,186])
    high_orange = np.array([22,144,255])
    # 
    # low_orange = np.array([h_low, s_low, v_low])
    # high_orange = np.array([h_upper, s_upper, v_upper])

    mask = cv2.inRange(hsv, low_orange, high_orange)
    kernel = np.ones((5,5), np.uint8)
    mask = cv2.erode(mask, kernel)

    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    dists = []
    points = []
    
    for cnt in contours:
        area = cv2.contourArea(cnt)
        dists.append(distance_from_camera(area))
        approx = cv2.approxPolyDP(cnt, 0.05 * cv2.arcLength(cnt, True), True)
        points.append(find_mean_point(approx))
        if area > 400 and len(approx) == 4:
            areas.append(area)
            cv2.drawContours(frame, [approx], 0, (0, 0, 0), 5)

    if len(dists) > 1 and len(points) > 1:
        z_dist = abs(dists[0]-dists[1])
        x_points = []
        y_points = []
        for i in points:
            x_points.append(i[0])
            y_points.append(i[1])
        x_dist = abs(x_points[0]-x_points[1])
        y_dist = abs(y_points[0]-y_points[1])

        y_angle = math.atan(y_dist/x_dist)
        z_angle = math.atan(z_dist/y_dist)

    cv2.imshow("Frame", frame)
    cv2.imshow("Mask", mask)

    key = cv2.waitKey(1)
    if key == 27:
        break
    
cap.release()
cv2.destroyAllWindows()
