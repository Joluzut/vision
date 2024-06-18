import cv2
import numpy as np
#function to check if the surrounding pixel around the selected contours are black to signify an trafficlight
def is_surrounded_by_black(image, x, y, w, h, threshold=0.55):
    #margin to check around the region
    margin = 20

    #calculate the region of interest boundaries
    x_start = max(0, x - margin)
    y_start = max(0, y - margin)
    x_end = min(image.shape[1], x + w + margin)
    y_end = min(image.shape[0], y + h + margin)
    
    #extract the region of interest
    roi = image[y_start:y_end, x_start:x_end]
    
    #convert the ROI to grayscale
    gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    
    #apply binary inverse threshold to detect black pixels
    _, binary_roi = cv2.threshold(gray_roi, 50, 255, cv2.THRESH_BINARY_INV)
    
    #calculate the ratio of black pixels in the binary image
    black_pixels_ratio = np.sum(binary_roi == 255) / (binary_roi.size)
    
    #check if the ratio of black pixels exceeds the threshold
    return black_pixels_ratio > threshold


def detect_traffic_light(image):
    #change color from bgr to hsv
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    #select the bounds for the colors red yellow and green
    #red has two bounds because it loops around in the heu sphere
    red_lower1 = np.array([0, 100, 100])
    red_upper1 = np.array([10, 255, 255])
    red_lower2 = np.array([140, 100, 100])
    red_upper2 = np.array([180, 255, 255])
    
    #yellow/orange bounds
    yellow_lower = np.array([0, 40, 30])
    yellow_upper = np.array([50, 255, 255])
    
    #green bounds
    green_lower = np.array([50, 50, 40])
    green_upper = np.array([80, 255, 255])

    #make an mask for each color
    mask_red1 = cv2.inRange(hsv, red_lower1, red_upper1)
    mask_red2 = cv2.inRange(hsv, red_lower2, red_upper2)
    mask_red = cv2.bitwise_or(mask_red1, mask_red2)
    mask_yellow = cv2.inRange(hsv, yellow_lower, yellow_upper)
    mask_green = cv2.inRange(hsv, green_lower, green_upper)

    #find the contours of every color group
    contours_red, _ = cv2.findContours(mask_red, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours_yellow, _ = cv2.findContours(mask_yellow, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours_green, _ = cv2.findContours(mask_green, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    green = 0
    red = 0
    yellow = 0

    #for every contour check if it is a trafficlight for red, yellow and green
    for cnt in contours_red:
        #check if the contour is big enough
        if cv2.contourArea(cnt) > 500:
            x, y, w, h = cv2.boundingRect(cnt)
            #calculate the aspect ratio of the contour
            aspect_ratio = float(w) / h
            #check if the aspect ratio is between 0.8 and 1.2 and if the contour is surrounded by black pixels
            if 0.8 <= aspect_ratio <= 1.2 and is_surrounded_by_black(image, x, y, w, h):
                #cv2.rectangle(image, (x, y), (x+w, y+h), (0, 0, 255), 2)  # Red
                red += 1

    #yellow
    for cnt in contours_yellow:
        #check if the contour is big enough
        if cv2.contourArea(cnt) > 500:
            x, y, w, h = cv2.boundingRect(cnt)
            #calculate the aspect ratio of the contour
            aspect_ratio = float(w) / h
            #check if the aspect ratio is between 0.8 and 1.2 and if the contour is surrounded by black pixels
            if 0.8 <= aspect_ratio <= 1.2 and is_surrounded_by_black(image, x, y, w, h):
                #cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 255), 2)  # 
                yellow += 1
    
    #green
    for cnt in contours_green:
        #check if the contour is big enough
        if cv2.contourArea(cnt) > 500:
            x, y, w, h = cv2.boundingRect(cnt)
            #calculate the aspect ratio of the contour
            aspect_ratio = float(w) / h
            #check if the aspect ratio is between 0.6 and 1.4 and if the contour is surrounded by black pixels
            if 0.6 <= aspect_ratio <= 1.4 and is_surrounded_by_black(image, x, y, w, h):
                #cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)  # Green
                green += 1

    #print("groen" + str(green))
    #print("rood" + str(red))
    #print("geel" + str(yellow))          
    #which colors has the most counts gets send back
    if green >= 1:
        return "11000101"
    elif yellow >= 1:
        return "11000110"
    elif red >= 1: 
        return "11000111"
    else: 
        #if no color is detected return 11000000 
        return "11000000"
    