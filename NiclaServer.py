import socket  # The Nicla will be the server
import os
import network
import sensor, image, time
from machine import Pin

toZumo = Pin("PA9", Pin.OUT_PP)

# Configuration
HOST = '192.168.1.100'  # This should be the private IP address of the Nicla
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

def send_image(communication_socket):
    img = sensor.snapshot()
    img.rotation_corr(z_rotation=180)  # Rotate the image 180 degrees
    compressed_img = img.compress(quality=15)  # Compress the image
    communication_socket.send(compressed_img)
    communication_socket.send(b'END_OF_IMAGE')

# Connect to the network
do_connect()

# Create and bind the server socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)  # Number of connections can be set here
print(HOST)

while True:
    print(f"waiting for socket")
    communication_socket, address = server.accept()
    print(f"Connected to {address}")
    try:
        message = communication_socket.recv(1024).decode('utf-8')  # 1024 is the buffer size
        print(f"Message from client: {message}")

        if message == 'image':
            send_image(communication_socket)
            print("Sent image")
            inputcode = "10010000"
            check_zero_one(inputcode)

        elif message == 'left':
            print("left")
            inputcode = "00010000"
            check_zero_one(inputcode)

        elif message == 'right':
            print("right")
            inputcode = "01001000"
            check_zero_one(inputcode)

        elif message == 'straight':
            print("straight")
            inputcode = "10001000"
            check_zero_one(inputcode)

        elif message == 'green':
            print("green")
            check_zero_one(message)

        elif message == 'orange':
            print("orange")
            check_zero_one(message)

        elif message == 'red':
            print("red")
            check_zero_one(message)

        elif message == 'disconnect':
            print("Disconnecting")

        else:
            print(f"Unknown message: {message}")

    except Exception as e:
        print(f"Exception: {e}")
    finally:
#        print(f"communication_socket closed")
        communication_socket.close()
