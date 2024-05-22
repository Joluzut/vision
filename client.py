import socket
import tqdm

HOST = '192.168.1.100'  # Address of the server on the local network
PORT = 9090

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

client_socket.send("Hello server".encode('utf-8'))
print(repr(client_socket.recv(1024).decode('utf-8')))  # Print with equivalent for \n

file_name = client_socket.recv(1024).decode('utf-8')
print(repr(file_name))  # Print with equivalent for \n

file_size = client_socket.recv(1024).decode('utf-8')
print(repr(file_size))  # Print with equivalent for \n

file = open(file_name, "wb")

file_bytes = b""

done = False

progress = tqdm.tqdm(unit="B", unit_scale=True, unit_divisor=1000,
                      total=int(file_size))

while not done:
    data = client_socket.recv(1024).decode('utf-8')
    if(file_bytes[-5:] == b"<END>"):
        done = True
    else:
        file_bytes += data
    progress.update(1024)

file.write(file_bytes)
file.close()
