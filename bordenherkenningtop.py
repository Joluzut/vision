"""@signrecognition docstring
Documentation for this module.
 
This module can recognise 4 traffic signs
Stop sign
No acces sign
Yield sign (both triangle and square)
"""

# import required libraries
import cv2
import numpy as np

"""Documentation for siftstopbord(img).
This function compares input file with a stop sign template using SIFT

Input: image variable that used cv2.imread('file.extension')
Return: boolean if there is a match
"""
def siftstopbord(img):
    # read images
    img1 = img  
    img2 = cv2.imread('stopbordtemplate1.jpg') #template file for stop sign SIFT
    # convert to gray
    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    # sift
    sift = cv2.SIFT_create()

    keypoints_1, descriptors_1 = sift.detectAndCompute(img1,None)
    keypoints_2, descriptors_2 = sift.detectAndCompute(img2,None)

    #feature matching
    bf = cv2.BFMatcher(cv2.NORM_L1, crossCheck=True)

    matches = bf.match(descriptors_1,descriptors_2)
    matches = sorted(matches, key = lambda x:x.distance)

    img3 = cv2.drawMatches(img1, keypoints_1, img2, keypoints_2, matches, img2, flags=2)
    # SIFT matches. increase value if too many false true
    if(len(matches) > 19):
        return 1
    else:
        return 0

"""Documentation for croppedcoor(x,y,crop).
This function alters x and y coordinates from original file to the cropped image that contains a shape

Input: 
    x: x-coordinates from shape of original file
    y: y-coordinates from shape of original file
    crop: croptype. 1 is for box shape. other values are regarded as normal crop format 
Return: x and y coordinates of cropped image size
"""
def croppedcoor(x,y,crop):
    if crop == 1:
        min_x = max(min(x)-4,1)
    else:
        min_x = max(min(x)-15,1)

    min_y = max(min(y)-15,1)
    tel_i = 0
    cropped_x = []
    cropped_y = []
    for i in x:
        cropped_x.append(i - (min_x )) 
        cropped_y.append(y[tel_i] - (min_y))
        tel_i += 1
    return cropped_x,cropped_y
    
"""Documentation for convertRed(img,kernel).
This function convert a BGR image to HSV. It creates a binary image that contains the area with the red colour

Input: 
    img: image variable created with cv2.imread('file.extension')
    kernel: string with kernel type (triangle or circle)
Return:
    thresh: binary mask image. White area contains the red colour
"""
def convertRed(img,kernel):
        
    kernelcircle = np.array([[0,1,1,1,0],
                        [1,1,1,1,1],
                        [1,1,1,1,1],
                        [1,1,1,1,1],
                        [0,1,1,1,0]],np.uint8)  
    
    kerneltriangle = np.array([[0,0,1,0,0],
                        [0,1,1,1,0],
                        [0,1,1,1,0],
                        [1,1,1,1,1],
                        [1,1,1,1,1]],np.uint8)

    if kernel == "circle":
        kernel = kernelcircle
        kernelD = 1
    elif kernel == "triangle":
        kernel = kerneltriangle
        kernelD = 2

    # convert image to hsv
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # Red color
    # Define the color range for detecting red
    red_lower1 = np.array([0, 100, 100])
    red_upper1 = np.array([10, 255, 255])
    red_lower2 = np.array([160, 90, 100])
    red_upper2 = np.array([180, 255, 255])

    # Threshold the HSV image to get only red colors
    mask_red1 = cv2.inRange(hsv, red_lower1, red_upper1)
    mask_red2 = cv2.inRange(hsv, red_lower2, red_upper2)
    mask_red = cv2.bitwise_or(mask_red1, mask_red2)

    mask_red = cv2.dilate(mask_red, kernelcircle,iterations=2*kernelD) 
    mask_red = cv2.erode(mask_red, kernelcircle,iterations=2) 
    red = cv2.bitwise_and(img, img, mask=mask_red)
    gray = cv2.cvtColor(red, cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(gray,25,255,0)
    thresh = cv2.dilate(thresh, kernelcircle,iterations=1) 
    thresh = cv2.erode(thresh, kernelcircle,iterations=1) 
    #cv2.imshow("stop2 thresh",thresh)
    #cv2.imshow("stop2 mask",mask_red)
    #cv2.waitKey(0)
    return thresh

"""Documentation for voorrangvierkant(img,kernel).
This function convert a BGR image to HSV. It creates a binary image that contains the area with the yellow colour
It checks if the shape contains the yellow colour in its center. 
Input: 
    img: image variable created with cv2.imread('file.extension')
    x: x-coordinates of shape from original image 
    y: y-coordinates of shape from original image
Return:
    boolean: true if shape contains yellow in its center
"""
def voorrangvierkant(img,x,y):
    kerneldiamond = np.array([[0,0,1,0,0],
                            [0,1,1,1,0],
                            [1,1,1,1,1],
                            [0,1,1,1,0],
                            [0,0,1,0,0]],np.uint8) 
    
    cropped_x, cropped_y = croppedcoor(x,y,0)
    combined = np.vstack((cropped_x, cropped_y)).T
    # convert image to hsv
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # Red color
    # Define the color range for detecting yellow
    yellow_lower = np.array([9, 100, 100])
    yellow_upper = np.array([30, 255, 255])

    # Threshold the HSV image to get only yellow colors
    mask_yellow = cv2.inRange(hsv, yellow_lower, yellow_upper)

    mask_yellow = cv2.dilate(mask_yellow, kerneldiamond,iterations=4) 
    mask_yellow = cv2.erode(mask_yellow, kerneldiamond,iterations=2) 
    yellow = cv2.bitwise_and(img, img, mask=mask_yellow)

    gray = cv2.cvtColor(yellow, cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(gray,20,255,0)

    thresh = cv2.dilate(thresh, kerneldiamond,iterations=2) 
    thresh = cv2.erode(thresh, kerneldiamond,iterations=1) 

    yellow = cv2.bitwise_and(img, img, mask=thresh)

    ret,mask = cv2.threshold(gray,255,255,0)
    
    cv2.drawContours(mask, [combined], -1, (255,255,255), -1)  # Draw filled contour on mask.
    eindresult = cv2.bitwise_and(yellow,yellow,mask=mask)
    #cv2.imshow("stop2 thresh",thresh)
    #cv2.imshow("stop2 mask",mask)
    #cv2.waitKey(0)
    
    mean_val = cv2.mean(thresh, mask=mask)[0]  # Mean value of pixels inside the contour
    if mean_val > 100:
        return 1
    
    return 0

"""Documentation for triangleCheck(x,y).
This function checks if triangle is pointing down or up.

Input: 
    x: x-coordinates of shape corners
    y: y-coordinates of shape corners
Return:
    boolean: true if pointing down if not false
"""
def triangleCheck(x, y):

    
    y_left = y[x.index(min(x))]
    y_middle = 0
    y_right = y[x.index(max(x))]
   
    for i in y:
        if y_left != i and y_right != i:
            y_middle = i
    if y_middle > y_left and y_middle > y_right:
        return 1
    else:
        return 0

"""Documentation for stopCircle(img,x,y).
This function checks if horizontal rectangle has a red border.

Input: 
    img:cropped image variable created with cv2.imread('file.extension')
    x: x-coordinates of shape corners from original file
    y: y-coordinates of shape corners from original file
Return:
    boolean: true if rectangle has a red border
"""
def stopCircle(img,x,y):
    kernelcircle = np.array([[0,1,1,1,0],
                            [1,1,1,1,1],
                            [1,1,1,1,1],
                            [1,1,1,1,1],
                            [0,1,1,1,0]],np.uint8)  
    cropped_x, cropped_y = croppedcoor(x,y,1)

    height, width = img.shape[:2]
    x_min = max(min(cropped_x),1)
    y_min = max(min(cropped_y),1)
    x_max = min(max(cropped_x),width)
    y_max = min(max(cropped_y),height)

    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    #create mask for check
    ret,mask = cv2.threshold(gray,255,255,0)
    cv2.rectangle(mask,(x_min,y_min),(x_max,y_max),(255,255,255),-1)
    mask = cv2.bitwise_not(mask)
    thresh = convertRed(img,"circle")
    #cv2.imshow("stop2 thresh",thresh)
    #cv2.imshow("stop2 mask",mask)
    #cv2.waitKey(0)
    
    mean_val = cv2.mean(thresh, mask=mask)[0]  # Mean value of pixels inside the contour
    if mean_val > 150:
        return 1
    else:
        return 0

"""Documentation for stopCircle(img,radius,cX,cY).
This function checks if circle contains red in the whole shape

Input: 
    img:cropped image variable created with cv2.imread('file.extension')
    radius:radius of shape
    cX: x-coordinates of shape corners in cropped image
    cY: y-coordinates of shape corners in cropped image
Return:
    boolean: true if circle contains red
"""
def redCircle(img,radius,cX,cY):
    
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    radius = int(radius / 2)
    thresh = convertRed(img,"circle")
    
    red = cv2.bitwise_and(img, img, mask=thresh)
    ret,mask = cv2.threshold(gray,230,255,0)
    
    cv2.circle(mask,(cX,cY), radius, (255,255,255), -1)
    mean_val = cv2.mean(thresh, mask=mask)[0]  # Mean value of pixels inside the contour

    if mean_val > 150:
        return 1
    
    return 0

"""Documentation for voorrangdriehoek(img,x,y).
This function checks if triangle contains red on the edge of the shape. It uses the corners of the shape and dilates.

Input: 
    img:cropped image variable created with cv2.imread('file.extension')
    x: x-coordinates of shape corners from original file
    y: y-coordinates of shape corners from original file
Return:
    boolean: true if triangle corners are in the red area
"""
def voorrangdriehoek(img,x,y):
    
    cropped_x , cropped_y = croppedcoor(x,y,0)
        
    thresh = convertRed(img,"triangle")
    
    for i in range (0,3):
        if thresh[cropped_y[i],cropped_x[i]] == 0:
            return 0
        
    return 1

"""Documentation for shape_herkenning(img,nrec).
This function contains the shape recognition. Shape that meets certain requirements go into sign checks


Input: 
    img:image variable created with cv2.imread('file.extension')
    nrec: recursion variable. How many times repeat function 
Return:
    boolean: type of sign that is found. Returns 0 if none
"""
def shape_herkenning(img, nrec):
    # convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    img_copy = img.copy()
    # apply thresholding to convert the grayscale image to a binary image
    ret,thresh = cv2.threshold(gray,80 + (nrec*20),255,0)
    # find the contours
    contours,hierarchy = cv2.findContours(thresh, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    height, width = img.shape[:2]
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.017*cv2.arcLength(cnt, True), True) 
        area = cv2.contourArea(cnt)
        x1,y1,w,h = cv2.boundingRect(cnt)
        ratio = w/h
        shape_found = False
        shape = "none"
        if len(approx) == 3 and area > 100 and (ratio > 0.80 and ratio < 1.20):
            shape_found = True
            shape = "triangle"
           
        elif len(approx) == 4 and area > 100 and area < (320*240) and ratio > 0.80:
            shape_found = True
            if ratio < 1.20:
                shape = "square"
            else:
                shape = "box"           
                
        elif len(approx)==8 and area > 100  and (ratio > 0.80 and ratio < 1.20):
            k=cv2.isContourConvex(approx)
            if k:
                shape_found = True
                shape = "circle"
                
    
        if shape_found == True:
            # Used to flatted the array containing 
            # the co-ordinates of the vertices. 
            n = approx.ravel()  
            i = 0
            M = cv2.moments(cnt)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])

            corner_x = []
            corner_y = []
            corners = 0
            for j in n : 
                if(i % 2 == 0): 
                    corner_x.append(n[i])
                    corner_y.append(n[i + 1] )
                    corners = corners + 1
                i = i + 1
            x_min = max(min(corner_x) - 15,1)
            y_min = max(min(corner_y) - 15,1)
            x_max = min(max(corner_x) + 15,width)
            y_max = min(max(corner_y) + 15,height)

            cropped_image = img_copy[y_min:y_max ,x_min:x_max]

            if shape == "triangle":
                if triangleCheck(corner_x,corner_y) == 1:
                    if voorrangdriehoek(cropped_image,corner_x,corner_y) == 1:
                        return 1
            if shape == "square":
                    if voorrangvierkant(cropped_image,corner_x,corner_y) == 1:
                        return 2 
            if shape == "circle":
                if redCircle(cropped_image,w,cX-x_min,cY-y_min) == 1:
                    if siftstopbord(cropped_image) == 1:
                        return 3


            #now you select a circle

            if shape == "box":
                x_min = max(min(corner_x) - 4,1)
                y_min = max(min(corner_y) - 15,1)
                x_max = min(max(corner_x) + 4,width)
                y_max = min(max(corner_y) + 15,height)                 
                cropped_image = img_copy[y_min:y_max ,x_min:x_max]
                if stopCircle(cropped_image,corner_x,corner_y) == 1:
                    return 4
      
    if nrec > 0:
        cv2.destroyAllWindows()
        return shape_herkenning(img_copy , nrec-1)       
    else:
        return 0
   
    #cv2.imshow("Shapes", img)
    #cv2.waitKey(0)
    

"""Documentation for show(orignal_image).
This function contains function call of shape_herkenning and returns a binary value 
This length is always 8bit and starts with 11.

Input: 
    img: original image variable created with cv2.imread('file.extension')
Return:
    boolean: binary 8-bit value starting with 11
"""
def show(original_image):

    binair = '11'   
    output = bin(shape_herkenning(original_image,2)).replace("0b", "")

    if len(output) != 6:
        missingbit = 6 - len(output)
        for i in range (0,missingbit):
           binair += '0' 
    #print("bin",binair)
    binair += output
    return binair    
