import cv2
import numpy as np
import math

# Read the image
image = cv2.imread('C:/school/visiongithub/received_image_72.jpg')
# Convert the image to a NumPy array
image_np = np.array(image)
      
# Convert the image from RGB (PIL format) to BGR (OpenCV format)
image_np = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
        
# Convert the image from BGR to HSV
hsv = cv2.cvtColor(image_np, cv2.COLOR_BGR2HSV)
crop_box = (10, 160, 320, 200)
x, y, w, h = crop_box

# Crop the image using NumPy slicing
cropped_image = hsv[y:y+h, x:x+w]

# Convert the image from BGR to HSV

# Define the lower and upper bounds for the black color in HSV space
lower_black = np.array([0, 0, 0])
upper_black = np.array([190, 255, 80])

# Threshold the HSV image to get only black colors
mask = cv2.inRange(cropped_image, lower_black, upper_black)

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
            if i < 160:
                left += 1
            else:
                right += 1
            total += 1
            sum += i
    if biggestline < white_pixels_in_line:
        biggestline = white_pixels_in_line
    if erode2[19][i] == 255:
        total2 += 1
    if erode2[20][i] == 255:
        total2 += 1
    if erode2[21][i] == 255:
        total2 += 1
    if erode2[0][i] == 255 and flag == 0:
        change = i
        flag = 1
    if erode2[20][299-i] == 255 and flag1 == 0:
        change1 = 299-i
        flag1 = 1
    if erode2[40][i] == 255 and flag == 0:
        change3 = i
if total > 0:
    middle = sum / total
offset = middle - constmiddle
overflow = left - right
change2 = (change + change1) / 2

if change2 > 165:
    change2 = change2 - 165

if change2 < 165:
    change2 = 165 - change2

change2 = change2 / 7
change2 = math.floor(change2)
if change2 >= 64:
    change2 = 63
if change2 <= 0:
    change2 = 1
print("change1 " + str(change1))
print("change2 " + str(change2))
print("overflow " + str(overflow))
print("offset" + str(offset))
print("biggest line:"+ str(biggestline))
fixed_binary = bin(change2)[2:].zfill(6)  # Ensure the binary string is zero-padded to 6 bits
if biggestline > 150:
    print("90")
    if change3 > 150:
        print("left")
        binary = '00000000'
    else:
        print("right")
        binary = '01000000'
elif offset > 15 and -900 < overflow < 900 and offset < 100:
    print("rechts 1")
    binary = '01' + fixed_binary
elif offset < -15 and -900 < overflow < 900 and offset > -100:
    print("links 1")
    binary = '00' + fixed_binary
elif overflow < -1600:
    print("links 2")
    binary = '00' + fixed_binary
elif overflow > 1600:
    print("rechts 2")
    binary = '01' + fixed_binary
else:
    print("rechtdoor")
    binary = '10' + fixed_binary
print(binary)

# Display the result
cv2.imshow('cropped', cropped_image)
cv2.imshow('og', image)
cv2.imshow('erode2', erode2)
cv2.imshow('dilate2', dilate2)
cv2.imshow('mask', mask)
cv2.imshow('hsv', hsv)
cv2.waitKey(0)
cv2.destroyAllWindows()
