import socket
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