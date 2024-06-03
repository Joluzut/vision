# import required libraries
import cv2
import numpy as np

def siftstopbord(img):
    # read images
    img1 = img  
    img2 = cv2.imread('stopbordtemplate1.jpg') 

    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    #sift
    sift = cv2.SIFT_create()

    keypoints_1, descriptors_1 = sift.detectAndCompute(img1,None)
    keypoints_2, descriptors_2 = sift.detectAndCompute(img2,None)

    #feature matching
    bf = cv2.BFMatcher(cv2.NORM_L1, crossCheck=True)

    matches = bf.match(descriptors_1,descriptors_2)
    matches = sorted(matches, key = lambda x:x.distance)

    img3 = cv2.drawMatches(img1, keypoints_1, img2, keypoints_2, matches, img2, flags=2)
    #cv2.imshow("test",img3)
    
    #print("stopbord overeen",len(matches))
    if(len(matches) > 30):
        return 1
    else:
        cv2.waitKey(0)
        return 0

def croppedcoor(x,y):
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
    # Define the color range for detecting red, yellow, and green lights
    red_lower1 = np.array([0, 100, 100])
    red_upper1 = np.array([10, 255, 255])
    red_lower2 = np.array([160, 100, 100])
    red_upper2 = np.array([180, 255, 255])

    # Threshold the HSV image to get only red colors
    mask_red1 = cv2.inRange(hsv, red_lower1, red_upper1)
    mask_red2 = cv2.inRange(hsv, red_lower2, red_upper2)
    mask_red = cv2.bitwise_or(mask_red1, mask_red2)

    mask_red = cv2.dilate(mask_red, kernelcircle,iterations=2*kernelD) 
    mask_red = cv2.erode(mask_red, kernelcircle,iterations=2) 
    #cv2.imshow("red_mask", mask_red)
    red = cv2.bitwise_and(img, img, mask=mask_red)

    #cv2.imshow("Result", red)
    gray = cv2.cvtColor(red, cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(gray,50,255,0)
    #cv2.imshow("OverLapBefore", thresh)
    thresh = cv2.dilate(thresh, kernelcircle,iterations=1) 
    thresh = cv2.erode(thresh, kernelcircle,iterations=1) 
    #cv2.imshow("OverLap", thresh)

    return thresh


def voorrangvierkant(img,x,y):
    kerneldiamond = np.array([[0,0,1,0,0],
                            [0,1,1,1,0],
                            [1,1,1,1,1],
                            [0,1,1,1,0],
                            [0,0,1,0,0]],np.uint8) 
    
    cropped_x, cropped_y = croppedcoor(x,y)
    #print("croppped xy",cropped_x,cropped_y)
    combined = np.vstack((cropped_x, cropped_y)).T
    # convert image to hsv
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # Red color
    # Define the color range for detecting red, yellow, and green lights
    yellow_lower = np.array([10, 100, 100])
    yellow_upper = np.array([30, 255, 255])

    # Threshold the HSV image to get only yellow colors
    mask_yellow = cv2.inRange(hsv, yellow_lower, yellow_upper)

    mask_yellow = cv2.dilate(mask_yellow, kerneldiamond,iterations=4) 
    mask_yellow = cv2.erode(mask_yellow, kerneldiamond,iterations=2) 
    #cv2.imshow("yellow_mask", mask_yellow)
    yellow = cv2.bitwise_and(img, img, mask=mask_yellow)

    #cv2.imshow("Result", yellow)
    gray = cv2.cvtColor(yellow, cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(gray,100,255,0)
    #cv2.imshow("OverLapBefore", thresh)
    thresh = cv2.dilate(thresh, kerneldiamond,iterations=2) 
    thresh = cv2.erode(thresh, kerneldiamond,iterations=1) 
    #cv2.imshow("OverLap", thresh)
    yellow = cv2.bitwise_and(img, img, mask=thresh)

    
    ret,mask = cv2.threshold(gray,230,255,0)
    
    cv2.drawContours(mask, [combined], -1, (255,255,255), -1)  # Draw filled contour on mask.
    eindresult = cv2.bitwise_and(yellow,yellow,mask=mask)
    #cv2.imshow("grayss end", eindresult)
    #cv2.waitKey(0)
    #cv2.imshow("mask",mask)
    
    mean_val = cv2.mean(thresh, mask=mask)[0]  # Mean value of pixels inside the contour
    #print("crop",mean_val)
    if mean_val > 100:
        return 1
    
    return 0


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

def stopCircle(img,x,y):
    kernelcircle = np.array([[0,1,1,1,0],
                            [1,1,1,1,1],
                            [1,1,1,1,1],
                            [1,1,1,1,1],
                            [0,1,1,1,0]],np.uint8)  
    cropped_x, cropped_y = croppedcoor(x,y)
    #print("croppped xy",cropped_x,cropped_y)
    height, width = img.shape[:2]
    x_min = max(min(cropped_x),1)
    y_min = max(min(cropped_y),1)
    x_max = min(max(cropped_x),width)
    y_max = min(max(cropped_y),height)

    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret,mask = cv2.threshold(gray,255,255,0)
    cv2.rectangle(mask,(x_min,y_min),(x_max,y_max),(255,255,255),-1)
    mask = cv2.bitwise_not(mask)
    thresh = convertRed(img,"circle")
    #cv2.imshow("stop2 thresh",thresh)
    #cv2.imshow("stop2 mask",mask)
    #cv2.waitKey(0)
    
    mean_val = cv2.mean(thresh, mask=mask)[0]  # Mean value of pixels inside the contour
    #print("crop acces den val ",mean_val)
    if mean_val > 150:
        return 1
    else:
        return 0






def redCircle(img,radius,cX,cY):
    
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    radius = int(radius / 2)
    thresh = convertRed(img,"circle")
    
    #print("crop",cropped_x,cropped_y)    
    red = cv2.bitwise_and(img, img, mask=thresh)
    ret,mask = cv2.threshold(gray,230,255,0)
    
    cv2.circle(mask,(cX,cY), radius, (255,255,255), -1)
    eindresult = cv2.bitwise_and(red,red,mask=mask)
    #cv2.imshow("grayss end", eindresult)
    #cv2.imshow("mask",mask)
    #cv2.waitKey(0)
    mean_val = cv2.mean(thresh, mask=mask)[0]  # Mean value of pixels inside the contour
    #print("crop circle 1",mean_val)
    if mean_val > 150:
        return 1
    
    return 0

def voorrangdriehoek(img,x,y):
    
    cropped_x , cropped_y = croppedcoor(x,y)
        
    thresh = convertRed(img,"triangle")
   
    #print("crop",cropped_x,cropped_y)
    
    for i in range (0,3):
        if thresh[cropped_y[i],cropped_x[i]] == 0:
            return 0
        
    return 1




def shape_herkenning(img, nrec):
    # convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #gray = 255 - gray

    img_copy = img.copy()
    # apply thresholding to convert the grayscale image to a binary image
    ret,thresh = cv2.threshold(gray,80 + (nrec*20),255,0)
    #cv2.imshow("threshold shape", thresh)
    # find the contours
    contours,hierarchy = cv2.findContours(thresh, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    #print("Number of contours detected:",len(contours))
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

            #print("minmax",x_min,y_min,x_max,y_max)
            #print("amount of points:",corners)
            #print("x_y",corner_x,corner_y)
            cropped_image = img_copy[y_min:y_max ,x_min:x_max]
            #cv2.imshow("Cropped", cropped_image)

            if shape == "triangle":
                if triangleCheck(corner_x,corner_y) == 1:
                    if voorrangdriehoek(cropped_image,corner_x,corner_y) == 1:
                        return 1
                    else:
                        print("Geen voorrangsdriehoek")  
                else:
                    print("Geen voorrangsdriehoek")
            if shape == "square":
                    if voorrangvierkant(cropped_image,corner_x,corner_y) == 1:
                        return 2 
                    else:
                        print("Geen voorrangsvierkant")  
    
            if shape == "circle":
                if redCircle(cropped_image,w,cX-x_min,cY-y_min) == 1:
                    if siftstopbord(cropped_image) == 1:
                        return 3
                    else:
                        print("Geen stopbord")

            #now you select a circle

            if shape == "box":
                xyc = [0,0,0,0]
                xyc[0] = int(cX - (w/2)) -10
                xyc[1] = int(cY - (w/2)) -10
                xyc[2] = int(cX + (w/2)) +10
                xyc[3] = int(cY + (w/2)) +10     
                #for z in xyc:
                #print("echekc",cX - (w/2)) 
                #print("echekc2",cY - (w/2)) 
                #print("echekc3",cX + (w/2)) 
                #print("echekc4",cY + (w/2))                  
                #cropped_image = img_copy[xyc[1]:xyc[3] ,xyc[0]:xyc[2]]
                if stopCircle(cropped_image,corner_x,corner_y) == 1:
                    return 4
                    img = cv2.drawContours(img, [cnt], -1, (0,255,255), 3)
                    cv2.putText(img, 'Box ' + str(area) , (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
      
    if nrec > 0:
        cv2.destroyAllWindows()
        shape_herkenning(img_copy , nrec-1)       

   
    #cv2.imshow("Shapes", img)
    #cv2.waitKey(0)
    return 0



def show(original_image):

    rec = shape_herkenning(original_image,2)
    if  rec == 1:
        print("voorrangsdriehoek")
    elif rec == 2:
        print("voorrangsvierkant")   
    elif rec == 3:
        print("stopbord")      
    elif rec == 4:
        print("geentoegangbord")

    binair = '11' + bin(rec).replace("0b", "")    
    print("bin",binair)

    return binair    



# convert the image to grayscale


# read the input image


'''

'''
auto = [cv2.imread('niclaauto.jpg'), cv2.imread('received_image_13.jpg'), cv2.imread('received_image_22.jpg'), cv2.imread('received_image_7.jpg')] 
for i in range(0,4):
    show(auto[i])

stopbord = [cv2.imread('stopbordtemplate1.jpg'), cv2.imread('stop2.jpg'), cv2.imread('stop3.jpg'), cv2.imread('stop4.jpg')] 
for i in range(0,4):
    show(stopbord[i])

vierkant = [cv2.imread('verkeersbordenperfect.jpg'), cv2.imread('voorrangvierkant2.jpeg'), cv2.imread('voorrangvierkant3.jpeg'), cv2.imread('voorrangvierkant4.jpeg'), cv2.imread('voorrangvierkant5.jpeg')] 
for i in range(1,len(vierkant)):
    show(vierkant[i])


driehoek = [cv2.imread('driehoek1.jpg'), cv2.imread('driehoek2.jpg'), cv2.imread('driehoek3.jpg')] 
for i in range(0,3):
    show(driehoek[i])
  

cv2.waitKey(0)
cv2.destroyAllWindows()