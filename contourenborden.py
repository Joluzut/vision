import cv2 as cv
import numpy as np

img = cv.imread("compr1.jpg")
element = (cv.Mat(11,11) <<     1,1,1,1,1,1,1,1,1,1,1,
                                1,1,1,1,1,1,1,1,1,1,1,
                                0,1,1,1,1,1,1,1,1,1,0,
                                0,1,1,1,1,1,1,1,1,1,0,
                                0,0,1,1,1,1,1,1,1,0,0,
                                0,0,1,1,1,1,1,1,1,0,0,
                                0,0,0,1,1,1,1,1,0,0,0,
                                0,0,0,1,1,1,1,1,0,0,0,
                                0,0,0,0,1,1,1,0,0,0,0,
                                0,0,0,0,1,1,1,0,0,0,0,
                                0,0,0,0,0,1,0,0,0,0,0)



cv.imshow("Display window", img)
k = cv.waitKey(0) # Wait for a keystroke in the window
imggray = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
cv.imshow("Display gray window", imggray)
k = cv.waitKey(0) # Wait for a keystroke in the window

thresh = 127
im_bw = cv.threshold(imggray, thresh, 255, cv.THRESH_BINARY)[1]
im_bw = cv.bitwise_not(im_bw)
cv.imshow("Display gray window", im_bw)
k = cv.waitKey(0) # Wait for a keystroke in the window

dst = cv.erode(im_bw, kernel)
cv.imshow("Display gray window", dst)
k = cv.waitKey(0) # Wait for a keystroke in the window