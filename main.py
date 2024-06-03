import cv2
import numpy as np
import math

# Read the image
image = cv2.imread('received_image_152.jpg')
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
mask = cv2.inRange(hsv, lower_black, upper_black)

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

for i in range(0, 310):
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
    if erode2[0][i] == 255 and flag == 0:
        print(i)
        change = i
        flag = 1
    if erode2[20][309-i] == 255 and flag1 == 0:
        print(i)
        change1 = 309-i
        flag1 = 1


if total > 0:
    middle = sum / total
offset = middle - constmiddle
overflow = left - right
change2 = (change + change1) / 2

if change2 > 165:
    change2 = change2 - 165

if change2 < 165:
    change2 = 165 - change2
change2 = change2/1.5
change2 = math.floor(change2)
print("totaal: " + str(total))
print("rechts: " + str(right))
print("links: " + str(left))
print("middel: " + str(middle))
print("offset: " + str(offset))
print("overflow: " + str(overflow))
print("change: " + str(change))
print("change1: " + str(change1))
print("change2: " + str(change2))

if overflow > 1700:
    print("tright")
elif overflow < -1700:
    print("tleft")
    
if total2 < 5:
    print("cross")

if offset < -14 and -900 < overflow < 900:
    print("left1")
elif offset > 14 and -900 < overflow < 900:
    print("right1")
elif overflow < -1600:
    print("left2")
elif overflow > 1600:
    print("right2")
else:
    print("straight")

# Display the result
cv2.imshow('cropped', cropped_image)
cv2.imshow('og', image)
cv2.imshow('erode2', erode2)
cv2.imshow('dilate2', dilate2)
cv2.imshow('mask', mask)
cv2.imshow('hsv', hsv)
cv2.waitKey(0)
cv2.destroyAllWindows()
