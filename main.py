from sys import argv

import cv2 as cv
from cv2 import IMREAD_COLOR, imread

a = imread(argv[1], IMREAD_COLOR)

print(a)
