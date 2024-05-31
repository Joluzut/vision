import numpy as np
import cv2
from PIL import Image

def LineDetection(image, prev):
    # Define the box for cropping (left, upper, right, lower)
    crop_box = (0, 160, 320, 200)
    # Crop the image using the defined box
    cropped_image = Image.fromarray(image).crop(crop_box)

    # Convert cropped image back to HSV (required if further processing is in HSV)
    hsv_cropped = cv2.cvtColor(np.array(cropped_image), cv2.COLOR_RGB2HSV)

    # Define the lower and upper bounds for the black color in HSV space
    lower_black = np.array([0, 0, 0])
    upper_black = np.array([190, 255, 80])

    # Threshold the HSV image to get only black colors
    mask = cv2.inRange(hsv_cropped, lower_black, upper_black)

    dilate = cv2.dilate(mask, None, iterations=3)
    erode = cv2.erode(dilate, None, iterations=2)
    dilate1 = cv2.dilate(erode, None, iterations=3)
    erode1 = cv2.erode(dilate1, None, iterations=2)
    dilate2 = cv2.dilate(erode1, None, iterations=3)
    erode2 = cv2.erode(dilate2, None, iterations=2)

    total = 0
    total2 = 0
    sum = 0
    middle = 0
    constmiddle = 170
    offset = 0
    left = 0
    right = 0
    overflow = 0

    for i in range(0, 320):
        for j in range(0, 40):
            if erode2[j][i] == 255:
                if i < 160:
                    left += 1
                else:
                    right += 1
                total += 1
                sum += i
        if erode2[19][i] == 255:
            total2 += 1
        if erode2[20][i] == 255:
            total2 += 1
        if erode2[21][i] == 255:
            total2 += 1

    if total > 0:
        middle = sum / total
    offset = middle - constmiddle
    overflow = left - right

    #print("totaal: " + str(total))
    #print("rechts: " + str(right))
    #print("links: " + str(left))
    #print("middel: " + str(middle))
    #print("offset: " + str(offset))
    #print("overflow: " + str(overflow))

    if prev == "straight" and overflow > 1700:
        return "tright"
    elif prev == "straight" and overflow < -1700:
        return "tleft"
    
    if prev == "straight" and total2 < 5:
        return "cross"

    if offset < -14 and -900 < overflow < -500:
        return "left"
    elif offset > 14 and 500 < overflow < 900:
        return "right"
    elif overflow < -1300:
        return "left"
    elif overflow > 1300:
        return "right"
    else:
        return "straight"

