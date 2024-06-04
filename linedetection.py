import numpy as np
import cv2
from PIL import Image
import math

def LineDetection(image, prev):
    # Define the box for cropping (left, upper, right, lower)
    crop_box = (10, 160, 320, 200)
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
    constmiddle = 165
    offset = 0
    left = 0
    right = 0
    overflow = 0
    change = 0
    change1 = 0
    flag = 0
    flag1 = 0
    change2 = 0
    change3 = 0

    
    white_pixel_counts = []
    biggestline = 0
    for j in range(0, 40):
        white_pixels_in_line = 0  # Count white pixels in the current horizontal line
        for i in range(0, 310):
            if erode2[j][i] == 255:
                white_pixels_in_line += 1
                if i < 155:
                    left += 1
                else:
                   right += 1
                total += 1
                sum += i
                if erode2[0][i] == 255 and flag == 0:
                    change = i
                    flag = 1
                if erode2[20][309-i] == 255 and flag1 == 0:
                    change1 = 309-i
                    flag1 = 1
        if biggestline < white_pixels_in_line:
            biggestline = white_pixels_in_line
        if erode2[19][i] == 255:
            total2 += 1
        if erode2[20][i] == 255:
            total2 += 1
        if erode2[21][i] == 255:
            total2 += 1
        if erode2[39][i] == 255 and flag == 0:
            change3 = i
    if total > 0:
        middle = sum / total
    offset = middle - constmiddle
    overflow = left - right
    change2 = (change + change1) / 2

    if change2 > 155:
        change2 = change2 - 155

    if change2 < 155:
        change2 = 155 - change2

    change2 = change2 / 8
    change2 = math.floor(change2)
    if change2 >= 64:
        change2 = 63
    if change2 <= 0:
        change2 = 1
    print("change2 " + str(change2))
    print("overflow " + str(overflow))
    print("offset" + str(offset))
    print("biggest line: " + str(biggestline))
     
    fixed_binary = bin(change2)[2:].zfill(6)  # Ensure the binary string is zero-padded to 6 bits

    if biggestline > 150:
        print("90")
        if change3 > 140:
            print("left")
            binary = '00000000'
        else:
            print("right")
            binary = '01000000'    
    elif offset > 20 and -1200 < overflow < 1200 and offset < 100:
        print("rechts 1")
        binary = '01' + fixed_binary
    elif offset < -20 and -1200 < overflow < 1200 and offset > -100:
        print("links 1")
        binary = '00' + fixed_binary
    elif overflow < -1800:
        print("links 2")
        binary = '00' + fixed_binary
    elif overflow > 1800:
        print("rechts 2")
        binary = '01' + fixed_binary
    else:
        print("rechtdoor")
        binary = '10' + fixed_binary
    print(binary)
    return binary
