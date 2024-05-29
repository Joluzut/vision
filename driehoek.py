# import required libraries
import cv2
import numpy as np




# read the input image
img = cv2.imread('compr2.jpg')

kernel = np.ones((5, 5), np.uint8)
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
red_mask_gray = cv2.cvtColor(red, cv2.COLOR_HSV2BGR)
red_mask_gray = cv2.cvtColor(red_mask_gray, cv2.COLOR_BGR2GRAY)
(thresh, im_bw) = cv2.threshold(red_mask_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
im_bw = cv2.dilate(im_bw, kernel,iterations=3) 
im_bw = cv2.erode(im_bw, kernel,iterations=2) 


red_mask = cv2.dilate(red_mask, kerneltriangle,iterations=4) 
red_mask = cv2.erode(red_mask, kerneltriangle,iterations=2) 
cv2.imshow("red_mask", red_mask)
red = cv2.bitwise_and(img, img, mask=red_mask)

cv2.imshow("red_mask2", red_mask)
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




# convert the image to grayscale
redRGB = cv2.cvtColor(red, cv2.COLOR_HSV2BGR)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#gray = 255 - gray


#gray = cv2.erode(gray,kerneltriangle,iterations=2)
#gray = cv2.dilate(gray,kerneltriangle,iterations=2)
cv2.imshow("gray", gray)
# apply thresholding to convert the grayscale image to a binary image
ret,thresh = cv2.threshold(gray,130,255,0)
cv2.imshow("gray222", thresh)
# find the contours
contours,hierarchy = cv2.findContours(thresh, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
print("Number of contours detected:",len(contours))

for cnt in contours:
    approx = cv2.approxPolyDP(cnt, 0.017*cv2.arcLength(cnt, True), True)
    area = cv2.contourArea(cnt)
    rect = cv2.minAreaRect(cnt)
    box = cv2.boxPoints(rect)
    box = np.intp(box)
    x,y,w,h = cv2.boundingRect(cnt)
    ratio = w/h

    if len(approx) == 3 and area > 100 and (ratio > 0.80 and ratio < 1.20):
        
        
        
        
        img = cv2.drawContours(img, [cnt], -1, (0,255,255), 3)
       
        # compute the center of mass of the triangle
        M = cv2.moments(cnt)
        if M['m00'] != 0.0:
            x = int(M['m10']/M['m00'])
            y = int(M['m01']/M['m00'])
        cv2.putText(img, 'Triangle' + str(area), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
    elif len(approx) == 4 and area > 100 and (ratio > 0.80 and ratio < 1.20):
        
        
        
        
        img = cv2.drawContours(img, [cnt], -1, (0,255,255), 3)
       
        # compute the center of mass of the triangle
        M = cv2.moments(cnt)
        if M['m00'] != 0.0:
            x = int(M['m10']/M['m00'])
            y = int(M['m01']/M['m00'])
        cv2.putText(img, 'Square ' + str(area) , (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)    
    elif len(approx)==8 and area > 100  and (ratio > 0.80 and ratio < 1.20):
        k=cv2.isContourConvex(approx)
        if k:
            img = cv2.drawContours(img, [cnt], -1, (0,255,255), 3)
            M = cv2.moments(cnt)
            if M['m00'] != 0.0:
                x = int(M['m10']/M['m00'])
                y = int(M['m01']/M['m00'])
            cv2.putText(img, 'Circle' + str(area), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
        #now you select a circle
 
cv2.imshow("Shapes", img)
cv2.waitKey(0)



cv2.destroyAllWindows()