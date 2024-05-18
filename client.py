import socket
import tqdm
HOST = '192.168.2.18'   #moet adderss zijn van de server op local network
PORT = 9090

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect((HOST, PORT))

socket.send("Hello server".encode('utf-8'))
print(socket.recv(1024).decode('utf-8'))    # 1024 is de buffer size


file_name = socket.recv(1024).decode('utf-8')
print(file_name)
file_size = (socket.recv(1024).decode('utf-8'))
print(file_size)
file = open(file_name, "wb")

file_bytes = b""
done = False

# file ontvangen

# progress = tqdm.tqdm(unit="B", unit_scale=True, unit_divisor=1000,
#                       total=int(file_size))
# while not done:
#     data = socket.recv(1024)
#     if file_bytes[-5:] == b"<END>": # -5 is stel dat END in verschillende keren word over gestuurd
#         done = True
#     else:
#         file_bytes += data
#     progress.update(1024)

# file.write(file_bytes)
# file.close()
