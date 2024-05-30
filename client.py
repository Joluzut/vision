import socket
from PIL import Image
import io
import cv2
import numpy as np
import time

HOST = '192.168.1.100'  # Address of the server on the local network
PORT = 9090

foto = 0

def make_socket():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    return client_socket

def ask_image():
    client_socket = make_socket()
    client_socket.send("image".encode('utf-8'))

    image_data = b""
    while True:
        packet = client_socket.recv(1024)  # Receive 1024 bytes from the socket
        if b'END_OF_IMAGE' in packet:  # Check if the end of image sequence is in the received packet
            image_data += packet[:-len(b'END_OF_IMAGE')]  # Remove the end of image sequence from the image data
            break
        image_data += packet
    client_socket.close()
    return image_data

try: 
    while True:
        image_data = ask_image()
        image = Image.open(io.BytesIO(image_data))  # Open the image from the received data
        
        filename = f"received_image_{foto}.jpg"
        image.save(filename)

        # Increment the variable
        foto += 1
        
        # Convert the image to a NumPy array
        image_np = np.array(image)
        
        # Convert the image from RGB (PIL format) to BGR (OpenCV format)
        image_np = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
        
        # Convert the image from BGR to HSV
        hsv = cv2.cvtColor(image_np, cv2.COLOR_BGR2HSV)
       
        # detect_traffic_light(hsv)
        # LineDetection(hsv)
        
except Exception as e:
    print(f"An error occurred: {e}")
    client_socket = make_socket()
    client_socket.send("disconnect".encode('utf-8'))
    client_socket.close()
