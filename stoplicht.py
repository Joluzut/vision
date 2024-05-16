import cv2
import numpy as np

def detect_traffic_light(image):
    # Convert the image to HSV (Hue, Saturation, Value) color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define the color range for detecting red, yellow, and green lights
    red_lower1 = np.array([0, 100, 100])
    red_upper1 = np.array([10, 255, 255])
    red_lower2 = np.array([160, 100, 100])
    red_upper2 = np.array([180, 255, 255])
    
    yellow_lower = np.array([20, 100, 100])
    yellow_upper = np.array([30, 255, 255])
    
    green_lower = np.array([40, 150, 150])
    green_upper = np.array([90, 255, 255])

    # Threshold the HSV image to get only red colors
    mask_red1 = cv2.inRange(hsv, red_lower1, red_upper1)
    mask_red2 = cv2.inRange(hsv, red_lower2, red_upper2)
    mask_red = cv2.bitwise_or(mask_red1, mask_red2)

    # Threshold the HSV image to get only yellow colors
    mask_yellow = cv2.inRange(hsv, yellow_lower, yellow_upper)

    # Threshold the HSV image to get only green colors
    mask_green = cv2.inRange(hsv, green_lower, green_upper)

    # Find contours for each color
    contours_red, _ = cv2.findContours(mask_red, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours_yellow, _ = cv2.findContours(mask_yellow, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours_green, _ = cv2.findContours(mask_green, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Draw bounding boxes around detected colors
    for cnt in contours_red:
        if cv2.contourArea(cnt) > 500:  # Adjust the area threshold as needed
            x, y, w, h = cv2.boundingRect(cnt)
            aspect_ratio = float(w) / h
            if 0.8 <= aspect_ratio <= 1.2:  # Adjust aspect ratio range
                cv2.rectangle(image, (x, y), (x+w, y+h), (0, 0, 255), 2)  # Red

    for cnt in contours_yellow:
        if cv2.contourArea(cnt) > 500:
            x, y, w, h = cv2.boundingRect(cnt)
            aspect_ratio = float(w) / h
            if 0.8 <= aspect_ratio <= 1.2:
                cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 255), 2)  # Yellow

    for cnt in contours_green:
        if cv2.contourArea(cnt) > 500:
            x, y, w, h = cv2.boundingRect(cnt)
            aspect_ratio = float(w) / h
            if 0.8 <= aspect_ratio <= 1.2:
                cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)  # Green

    return image


# Load the image
image = cv2.imread('3.jpg')

# Detect traffic lights
result_image = detect_traffic_light(image)

# Display the result
cv2.imshow('Detected Traffic Light', result_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
