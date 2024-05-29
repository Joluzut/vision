import socket  # The Nicla will be the server
import os
import network
import sensor, image, time
from machine import Pin

toZumo = Pin("PA9", Pin.OUT_PP)


# Configuration
HOST = '192.168.1.101'  # This should be the private IP address of the Nicla
PORT = 9090  # or another port
SSID = "ICIDU"
KEY = "ICIDUAVANS"

# Sensor initialization
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time=2000)
clock = time.clock()

def check_zero_one(input_string):
    toZumo.low()
    for char in input_string:
        time.sleep_us(500)
        if char == '0':
            toZumo.high()
        else:
            toZumo.low()


def do_connect():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('Connecting to network...')
        print(SSID)
        print(KEY)
        sta_if.active(True)
        sta_if.connect(SSID, KEY)
        while not sta_if.isconnected():
            pass
    print('Network config:', sta_if.ifconfig())

def send_image(communitcation_socket):
    img = sensor.snapshot()
    img.rotation_corr(z_rotation=180)  # Rotate the image 180 degrees
    compressed_img = img.compress(quality = 15)  # Compress the image
    communitcation_socket.send(compressed_img)
    communitcation_socket.send(b'END_OF_IMAGE')

# Connect to the network
do_connect()

# Create and bind the server socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)  # Number of connections can be set here
print(HOST)

while True:
    communitcation_socket, address = server.accept()
    print(f"Connected to {address}")
    while True:
        message = communitcation_socket.recv(1024).decode('utf-8')  # 1024 is the buffer size
        print(f"Message from client: {message}")
        if message == 'image':
            send_image(communitcation_socket)
            print(f"send image")
            imputcode= "10"
            check_zero_one(imputcode)

        elif message == 'disconnect':
            communitcation_socket.close()  # Close the socket when the client sends 'disconnect'
            break
        elif message == 'left':
            print(f"left")
            imputcode= "00111111"
            check_zero_one(imputcode)

        elif message == 'right':
            print(f"right")
            imputcode= "01111111"
            check_zero_one(imputcode)

        elif message == 'straight':
            print(f"straight")
            imputcode= "10111111"
            check_zero_one(imputcode)

        elif message == 'green':
            print(f"green")
            check_zero_one(message)
        elif message == 'orange':
            print(f"orange")
            check_zero_one(message)

        elif message == 'red':
            print(f"red")
            check_zero_one(message)





#    communitcation_socket.close()  # Ensure the socket is closed after the interaction
