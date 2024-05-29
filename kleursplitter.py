import cv2
import numpy as np




def increaseContrast(img):

    # converting to LAB color space
    lab= cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l_channel, a, b = cv2.split(lab)

    # Applying CLAHE to L-channel
    # feel free to try different values for the limit and grid size:
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    cl = clahe.apply(l_channel)

    # merge the CLAHE enhanced L-channel with the a and b channel
    limg = cv2.merge((cl,a,b))

    # Converting image from LAB Color model to BGR color spcae
    enhanced_img = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
    cv2.imshow("enhanced_img", enhanced_img)
    return enhanced_img

def getColor(img):


    kernel = np.ones((7, 7), np.uint8)
    kerneltriangle = np.array([[0,0,1,0,0],
                            [0,1,1,1,0],
                            [0,1,1,1,0],
                            [1,1,1,1,1],
                            [1,1,1,1,1]],np.uint8) 
    kernelcircle = np.array([[0,0,1,0,0],
                            [0,1,1,1,0],
                            [1,1,1,1,1],
                            [0,1,1,1,0],
                            [0,0,1,0,0]],np.uint8) 
    # convert image to hsv
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        # Red color
    low_red = np.array([136, 87, 111])
    high_red = np.array([179, 255, 255])
    red_mask = cv2.inRange(hsv, low_red, high_red)
    red = cv2.bitwise_and(img, img, mask=red_mask)
    cv2.imshow("red_mask2", red_mask)
    red_mask_gray = cv2.cvtColor(red, cv2.COLOR_HSV2BGR)
    red_mask_gray = cv2.cvtColor(red_mask_gray, cv2.COLOR_BGR2GRAY)
    (thresh, im_bw) = cv2.threshold(red_mask_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    im_bw = cv2.dilate(im_bw, kernel,iterations=3) 
    im_bw = cv2.erode(im_bw, kernel,iterations=2) #adsdasds


    red_mask = cv2.dilate(red_mask, kernel,iterations=5) 
    red_mask = cv2.erode(red_mask, kernel,iterations=1) 
    cv2.imshow("red_mask", red_mask)
    red = cv2.bitwise_and(img, img, mask=red_mask)

    #cv2.imshow("red_mask2", red_mask)
    red = cv2.bitwise_and(img, img, mask=red_mask)


    # Blue color
    low_blue = np.array([94, 80, 2])
    high_blue = np.array([126, 255, 255])
    blue_mask = cv2.inRange(hsv, low_blue, high_blue)
    blue = cv2.bitwise_and(img, img, mask=blue_mask)
    # Green color
    low_green = np.array([25, 52, 72])
    high_green = np.array([102, 255, 255])
    green_mask = cv2.inRange(hsv, low_green, high_green)
    green = cv2.bitwise_and(img, img, mask=green_mask)
    # Every color except white
    low = np.array([0, 42, 0])
    high = np.array([179, 255, 255])
    mask = cv2.inRange(hsv, low, high)
    result = cv2.bitwise_and(img, img, mask=mask)


    #cv2.imshow("Frame", img)
    cv2.imshow("Red", red)
    #cv2.imshow("Blue", blue)
    #cv2.imshow("Green", green)
    #cv2.imshow("Result", result)
    #key = cv2.waitKey(1)

    return red




img = cv2.imread('driehoek1.jpg')

enhancedimg = increaseContrast(img)

redimg = getColor(enhancedimg)

enhancedimg = increaseContrast(redimg)

redimg = getColor(enhancedimg)

cv2.waitKey(0)
cv2.destroyAllWindows()