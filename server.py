import socket  #die nicla word de server
import os
HOST = '192.168.2.18'  # dit moet prive ip adress zijn. CMD ipconfig en kijken voor resultaat. Kan ook local host zijn
PORT = 9090 # of andere port

server = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen() # je kunt hier cijfers in zetten om aantal connecties in te stellen

while True:
    communitcation_socket, address = server.accept() # 
    print (f"Connected to {address}")
    message = communitcation_socket.recv(1024).decode('utf-8') # 1024 is de buffer size
    print(f"Message from client: {message}")
    communitcation_socket.send("Message received".encode('utf-8'))
    communitcation_socket.close() # close the connection
    print(f"Connection with {address} closed")




# voor versturen van een file
# file = open("image.jpg", "rd") # open file in read mode
# file_size= os.path.getsize("image.jpg") # get the size of the file
# communitcation_socket.send("reciebed_imaga.png".encode()) # send the size of the file
# communitcation_socket.send(str(file_size).encode()) # send the size of the file
# data = file.read() # read the file
# communitcation_socket.sendall(data) # send the file
# communitcation_socket.send(b"<END>")
# file.close() # close the file