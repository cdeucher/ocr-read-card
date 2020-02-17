# USAGE
# python point.py --img image
import numpy as np
from imutils.perspective import four_point_transform
from imutils import contours
from pyzbar import pyzbar
import argparse
import imutils
import cv2, os, shutil

_threshold_ = 0.8


def math_answer(img_gray, Target, value):
    res = cv2.matchTemplate(img_gray, Target, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= value)
    answers = []
    for pt in zip(*loc[::-1]):
        cv2.circle(img_gray, pt, 50, (0, 255, 0), 2)  
        answers.append(pt)

    return answers, img_gray    
#End

answer1     = cv2.imread('answer1.png')
output     = cv2.imread('output.png')

answer1_gray = cv2.cvtColor(answer1, cv2.COLOR_BGR2GRAY)
output_gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)

answers, img_gray  = math_answer(output_gray, answer1_gray, _threshold_)

cv2.imwrite('img_gray.jpg',img_gray)