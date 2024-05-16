import socket

HOST = '192.168.2.18'   #moet adderss zijn van de server op local network
PORT = 9090

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect((HOST, PORT))

socket.send("Hello server".encode('utf-8'))
print(socket.recv(1024).decode('utf-8'))    # 1024 is de buffer size