import cv2
import numpy as np

vid = cv2.VideoCapture(0)

def find_rect_points(points):
    all_x = []
    all_y = []
    if points is None:
        return None
    for holder in points:
        for h in holder:
            all_x.append(h[0])
            all_y.append(h[1])
    return [(min(all_x), min(all_y)), (max(all_x), max(all_y))]
    

while True:
    _, frame = vid.read()

    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    low_red = np.array([170, 70, 50])
    high_red = np.array([180, 255, 255])

    red_mask = cv2.inRange(hsv_frame, low_red, high_red)

    cv2.imshow("Image", red_mask)
    red_img = cv2.bitwise_and(frame, frame, mask=red_mask)

    points = cv2.findNonZero(red_mask)
    rect_points = find_rect_points(points)

    if rect_points is None:
        pass
    else:
        cv2.rectangle(red_img, rect_points[0], rect_points[1], (0, 255, 0), 3)

    cv2.imshow("Mask", red_img)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
vid.release()
    