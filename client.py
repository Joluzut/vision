import socket
from PIL import Image
import io
import cv2
import numpy as np

HOST = '192.168.1.101'  # Address of the server on the local network
PORT = 9090

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

def AskImage(client_socket):
    client_socket.send("image".encode('utf-8'))

    image_data = b""
    while True:
        packet = client_socket.recv(1024)  # Receive 2048 bytes from the socket
        if b'END_OF_IMAGE' in packet:  # Check if the end of image sequence is in the received packet
            image_data += packet[:-len(b'END_OF_IMAGE')]  # Remove the end of image sequence from the image data
            break
        image_data += packet

    return image_data
try: 
    while True:
        image_data = AskImage(client_socket)
        image = Image.open(io.BytesIO(image_data))  # Open the image from the received data
        image.save("received_image.jpg")  # Save the image as 'received_image.jpg'
        # image.show()  # Display the image
        
        newimage = cv2.imread('recieved_image.jpg')
        cropped_image = newimage[160:200, 0:320]
        # Convert the image to the HSV color space
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        #hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # Define the lower and upper bounds for the black color in HSV space
        lower_black = np.array([0, 0, 0])
        upper_black = np.array([190, 255, 80])

        # Threshold the HSV image to get only black colors
        mask = cv2.inRange(hsv, lower_black, upper_black)

        dilate = cv2.dilate(mask, None, iterations=3)
        erode = cv2.erode(dilate , None, iterations=2)
        dilate1 = cv2.dilate(erode, None, iterations=3)
        erode1 = cv2.erode(dilate1 , None, iterations=2)
        dilate2 = cv2.dilate(erode1, None, iterations=3)
        erode2 = cv2.erode(dilate2 , None, iterations=2)
        #gray = cv2.cvtColor(erode2, cv2.COLOR_BGR2GRAY)
        #blur = cv2.GaussianBlur(erode2, (5, 5), 0)
        #edges = cv2.Canny(blur, 50, 150)
        total = 0
        sum = 0
        middle = 0
        constmiddle = 185
        offset = 0
        left = 0
        right = 0 

        for i in range(0, 320):  
            for j in range(0, 40):
                if erode2[j][i] == 255:
                    if i < 160:
                        left += 1
                    else:
                        right += 1
                    total += 1
                    sum += i
                

        middle = sum / total
        offset = middle - constmiddle
        print("totaal: " + str(total))
        print("rechts: " + str(right))
        print("links: " + str(left))
        print("middel: " + str(middle))
        print("offset: " + str(offset))
        if offset < -14:
            print("Turn left")
            client_socket.send("left".encode('utf-8'))
        elif offset > 14:
            print("Turn right")
            client_socket.send("right".encode('utf-8'))
        else:
            print("Go straight")
            client_socket.send("straight".encode('utf-8'))


        # Display the result
        #cv2.imshow('cropped', cropped_image)
        #cv2.imshow('og', image)
        #cv2.imshow('erode2', erode)
        #cv2.imshow('dilate2', dilate)
        #cv2.imshow('mask', mask)
        #cv2.imshow('edges', edges)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()
except Exception as e:
    print(f"An error occurred: {e}")
    client_socket.send("disconnect".encode('utf-8'))