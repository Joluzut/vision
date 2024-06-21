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

# Sensor/ camera initialization
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time=2000)
clock = time.clock()

def check_zero_one(input_string): # fucntion to send data to zumo
    toZumo.low()
    for char in input_string:
        time.sleep_us(500)
        if char == '0':
            toZumo.high()
        else:
            toZumo.low()

    time.sleep_us(500)
    toZumo.high()


def do_connect():   #funtion to connect to wifi network
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

def send_image(communication_socket): #funtion to send image
    img = sensor.snapshot()
    img.rotation_corr(z_rotation=180)  # Rotate the image 180 degrees
    compressed_img = img.compress(quality=15)  # Compress the image
    communication_socket.send(compressed_img)
    communication_socket.send(b'END_OF_IMAGE')
    print("Sent image")
    communication_socket.send(b'END_OF_IMAGE') #extra end of image if the first one didn't work


# Connect to the network
do_connect()

# Create and bind the server socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen(5)  # Number of connections can be set here
print(HOST)

while True:
    print(f"waiting for socket")
    communication_socket, address = server.accept() #accept conection from client
    print(f"Connected to {address}")
    try: #if there is a socket connectet than
        message = communication_socket.recv(1024).decode('utf-8')  #recieve message from client with a 1024 buffer
        print(f"Message from client: {message}")
        message = str(message)  #convert message to string
                                #Nessisary for the check_zero_one funtion

        if message == 'image':
            send_image(communication_socket) # send image to client
#            inputcode = "10010000"
#            check_zero_one(inputcode)

        elif message == 'disconnect':
            print("Disconnecting")

        elif message == 'stop': #when there is a time out
            print("stop")
            input = "100000000"
            check_zero_one(input)

        else:
            check_zero_one(message) #send message to zumo
            time.sleep_us(100)

    except Exception as e:
        print(f"Exception: {e}") #print exception
        communication_socket.close()
    finally:
#        print(f"communication_socket closed")
        communication_socket.close() #close communication_socket
