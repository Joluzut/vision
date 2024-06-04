import numpy as np
import cv2
from PIL import Image
import math

def LineDetection(image, prev):
    # Define the box for cropping (left, upper, right, lower)
    crop_box = (10, 120, 280, 190)
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
    constmiddle = 130
    offset = 0
    left = 0
    right = 0
    overflow = 0
    change = 0
    change1 = 0
    flag = 0
    flag1 = 0
    flag2 = 0
    change2 = 0
    change3 = 0
    temp = 0
    
    biggestline = 0
    for j in range(0, 70):
        white_pixels_in_line = 0  # Count white pixels in the current horizontal line
        for i in range(0, 260):
            if erode2[j][i] == 255:
                white_pixels_in_line += 1
                if i < 130:
                    left += 1
                else:
                    right += 1
                total += 1
                sum += i
                if erode2[20][i] == 255 or flag == 1:
                    change = i
                    flag = 1
                if erode2[40][259-i] == 255 or flag1 == 1:
                    change1 = 259 - i
                    flag1 = 1
        if biggestline < white_pixels_in_line:
            temp = j
            biggestline = white_pixels_in_line
    for k in range(0, 260):
        if temp < 55:
            if erode2[temp + 10][k] != 0 and flag2 == 0:
                change3 = k
                flag2 = 1
            elif k == 259 and flag2 == 0:
                flag2 = 1
                change3 = 10
    if total > 0:
        middle = sum / total
    offset = middle - constmiddle
    overflow = left - right
    change2 = (change + change1) / 2

    if change2 > 160:
        change2 = change2 - 160

    if change2 < 160:
        change2 = 160 - change2

    change2 = change2 / 6
    change2 = math.floor(change2)
    if change2 >= 64:
        change2 = 63
    if change2 <= 0:
        change2 = 1
    print("change2 " + str(change2))
    print("overflow " + str(overflow))
    print("offset" + str(offset))
    print("biggest line: " + str(biggestline))
    print("change3 " + str(change3))
    print("test" + str(temp))
    fixed_binary = bin(change2)[2:].zfill(6)  # Ensure the binary string is zero-padded to 6 bits

    if biggestline > 170:
        print("90")
        if change3 > 110:
            print("left")
            binary = '00000000'
        else:
            print("right")
            binary = '01000000'    
    elif offset > 25:
        print("rechts 1")
        binary = '01' + fixed_binary
    elif offset < -25:
        print("links 1")
        binary = '00' + fixed_binary
    elif overflow < -600:
        print("links 2")
        binary = '00' + fixed_binary
    elif overflow > 600:
        print("rechts 2")
        binary = '01' + fixed_binary
    else:
        print("rechtdoor")
        binary = '10' + fixed_binary
    print(binary)
    return binary

