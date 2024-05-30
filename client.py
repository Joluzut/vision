import socket
from PIL import Image
from linedetection import LineDetection
from stoplicht import detect_traffic_light
import io
import cv2
import numpy as np
import time

HOST = '192.168.1.101'  # Address of the server on the local network
PORT = 9090

foto = 0

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
        
        filename = f"received_image_{foto}.jpg"
        #image.save(filename)
        foto += 1
        # Convert the image to a NumPy array
        image_np = np.array(image)
        # Convert the image from RGB (PIL format) to BGR (OpenCV format)
        image_np = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
        # Convert the image from BGR to HSV
        hsv = cv2.cvtColor(image_np, cv2.COLOR_BGR2HSV)
       
        detect_traffic_light(hsv, client_socket)
        LineDetection(hsv, client_socket)
except Exception as e:
    print(f"An error occurred: {e}")
    client_socket.send("disconnect".encode('utf-8'))