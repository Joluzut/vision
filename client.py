import socket
#import tqdm
from PIL import Image
import io

HOST = '192.168.1.102'  # Address of the server on the local network
PORT = 9090

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

client_socket.send("Hello server".encode('utf-8'))

image_data = b""
while True:
    packet = client_socket.recv(1024)
    if b'END_OF_IMAGE' in packet:  # Check if the end of image sequence is in the received packet
        image_data += packet[:-len(b'END_OF_IMAGE')]  # Remove the end of image sequence from the image data
        break
    image_data += packet

image = Image.open(io.BytesIO(image_data))# straks gan gewoon met image aan de s
image.save("received_image.jpg")  # Save the image as 'received_image.jpg'
image.show()  # Display the image
