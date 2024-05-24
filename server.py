import socket  #de nicla word de server
import os
import network
import sensor, image, time
HOST = '192.168.1.100'  # dit moet prive ip adress zijn. CMD ipconfig en kijken voor resultaat. Kan ook local host zijn
PORT = 9090 # of andere port
ssid ="ICIDU"
key = "ICIDUAVANS"

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)
clock = time.clock()

def do_connect():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        print(ssid)
        print(key)
        sta_if.active(True)
        sta_if.connect('ICIDU', 'ICIDUAVANS')
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())

def send_image():
    img = sensor.snapshot()
    img.rotation_corr(z_rotation=180)  # Rotate the image 180 degrees
    compressed_img = img.compress(35)
    communitcation_socket.send(compressed_img)
    communitcation_socket.send(b'END_OF_IMAGE')


do_connect()


server = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1) # je kunt hier cijfers in zetten om aantal connecties in te stellen
print(HOST)

while True:
    communitcation_socket, address = server.accept() #
    print (f"Connected to {address}")
    message = communitcation_socket.recv(1024).decode('utf-8') # 1024 is de buffer size
    print(f"Message from client: {message}")
#    communitcation_socket.send("Message received".encode('utf-8'))
    send_image()


#    # voor versturen van een file

