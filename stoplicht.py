import cv2
import numpy as np

def is_surrounded_by_black(image, x, y, w, h, threshold=0.5):
    margin = 15
    x_start = max(0, x - margin)
    y_start = max(0, y - margin)
    x_end = min(image.shape[1], x + w + margin)
    y_end = min(image.shape[0], y + h + margin)
    
    roi = image[y_start:y_end, x_start:x_end]
    gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    _, binary_roi = cv2.threshold(gray_roi, 50, 255, cv2.THRESH_BINARY_INV)
    
    black_pixels_ratio = np.sum(binary_roi == 255) / (binary_roi.size)
    
    return black_pixels_ratio > threshold

def detect_traffic_light(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    red_lower1 = np.array([0, 100, 100])
    red_upper1 = np.array([10, 255, 255])
    red_lower2 = np.array([140, 100, 100])
    red_upper2 = np.array([180, 255, 255])
    
    yellow_lower = np.array([0, 0, 10])
    yellow_upper = np.array([50, 255, 255])
    
    green_lower = np.array([50, 40, 30])
    green_upper = np.array([100, 255, 255])

    mask_red1 = cv2.inRange(hsv, red_lower1, red_upper1)
    mask_red2 = cv2.inRange(hsv, red_lower2, red_upper2)
    mask_red = cv2.bitwise_or(mask_red1, mask_red2)
    mask_yellow = cv2.inRange(hsv, yellow_lower, yellow_upper)
    mask_green = cv2.inRange(hsv, green_lower, green_upper)

    contours_red, _ = cv2.findContours(mask_red, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours_yellow, _ = cv2.findContours(mask_yellow, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours_green, _ = cv2.findContours(mask_green, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    red = 0
    green = 0
    orange = 0
    for cnt in contours_red:
        if cv2.contourArea(cnt) > 500:
            x, y, w, h = cv2.boundingRect(cnt)
            aspect_ratio = float(w) / h
            if 0.8 <= aspect_ratio <= 1.2 and is_surrounded_by_black(image, x, y, w, h):
                #cv2.rectangle(image, (x, y), (x+w, y+h), (0, 0, 255), 2)  # Red
                red = red + 1
                

    for cnt in contours_yellow:
        if cv2.contourArea(cnt) > 500:
            x, y, w, h = cv2.boundingRect(cnt)
            aspect_ratio = float(w) / h
            if 0.8 <= aspect_ratio <= 1.2 and is_surrounded_by_black(image, x, y, w, h):
                #cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 255), 2)  #Orange
                orange = orange + 1
                

    for cnt in contours_green:
        if cv2.contourArea(cnt) > 500:
            x, y, w, h = cv2.boundingRect(cnt)
            aspect_ratio = float(w) / h
            if 0.6 <= aspect_ratio <= 1.4 and is_surrounded_by_black(image, x, y, w, h):
                #cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)  # Green
                green = green + 1
                

    if green > orange and green > red:
        print("green")
        return "11000101"
    elif orange > green and orange > red:
        print("orange")
        return "11000110"
    elif red > orange and red > green: 
        print("red")
        return "11000111"
    else:  
        return "11000000"
    