import socket
#import tqdm
from PIL import Image
import io
import time

HOST = '192.168.1.102'  # Address of the server on the local network
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

    
while True:
    image_data = AskImage(client_socket)
    image = Image.open(io.BytesIO(image_data))  # Open the image from the received data
    image.save("received_image.jpg")  # Save the image as 'received_image.jpg'
    image.show()  # Display the image
    time.sleep(500)
