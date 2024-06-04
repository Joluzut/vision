import socket
from PIL import Image
from linedetection import LineDetection
import io
import cv2
import numpy as np
from io import BytesIO
import time
from bordenherkenningtop import show

HOST = '192.168.1.101'  # Address of the server on the local network
PORT = 9090

foto = 0
prev = "" 
tick = 0
temp = ""
flag = 0

def make_socket():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    return client_socket

import socket
import time

def receive_image(client_socket):
        image_data = b""
        start_time = time.time()  # Record the start time

        while True:
            try:
                packet = client_socket.recv(1024)  # Receive 1024 bytes from the socket
                if b'END_OF_IMAGE' in packet:  # Check if the end of image sequence is in the received packet
                    image_data += packet[:-len(b'END_OF_IMAGE')]  # Remove the end of image sequence from the image data

                    break
                image_data += packet
            except socket.timeout:
                elapsed_time = time.time() - start_time  # Calculate elapsed time
                if elapsed_time > 0.2:  # If more than 500ms has passed
                    print("Timeout occurred, resending image request.")
                    #  client_socket.send("image".encode('utf-8'))  # Resend image request
                    newSocket = make_socket()
                    newSocket.send("stop".encode("utf-8"))
                    newSocket.close()
                    start_time = time.time()  # Reset the start time
                    exit 

        return image_data

def ask_image():
    
    while True:
        client_socket = make_socket()
        client_socket.settimeout(0.2)  # Set timeout to 500ms

        try:
            client_socket.send("image".encode('utf-8'))
            # print("asked image")

            image_data = receive_image(client_socket)
            # print("received image")

            # Validate the received image data
            image = Image.open(BytesIO(image_data))
            image.verify()  # Verify that it is, indeed, an image
            return image_data  # Return the valid image data

        except (socket.error, socket.timeout) as e:
            print("Connection error occurred: {e}")
            client_socket.close()
            time.sleep(1)  # Wait before retrying

        except (IOError, SyntaxError) as e:
            print(f"Image validation error: {e}")
            client_socket.close()
            time.sleep(1)  # Wait before retrying

        finally:
            client_socket.close()
        # print("received image")




def senCommand(myCommand):
    try:
        command = myCommand
        client_socket = make_socket()
        
        if client_socket is None:
            print("Failed to create or connect the socket.")
            return
        
        # Send the command
        client_socket.send(command.encode('utf-8'))
        
        # Close the socket
        client_socket.close()
           
        # print("Command sent successfully.")
    except Exception as e:
        a = 1+ 1
        # print(f"Error sending command: {e}")
     
try: 
    while True:
        image_data = ask_image()
        image = Image.open(io.BytesIO(image_data))  # Open the image from the received data
        
        filename = f"14received_image_{foto}.jpg"
        print("image: "+ str(foto))
        image.save(filename)
        image.save('afbeelding.jpg')
        #senCommand("stop")
        newimage = cv2.imread('afbeelding.jpg')
        # Increment the variable
        foto += 1
        
        image_np = np.array(newimage)
      
        # Convert the image from RGB (PIL format) to BGR (OpenCV format)
        image_np = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
                
        # Convert the image from BGR to HSV
        hsv = cv2.cvtColor(image_np, cv2.COLOR_BGR2HSV)
                
        # detect_traffic_light(hsv)
        antwoord = LineDetection(hsv, prev)

                
        bord = show(image_np)
        senCommand(bord)
        print("bord:",bord)

        if antwoord == '00000000' or antwoord == '01000000':
            print("bocht")
            temp = antwoord
            antwoord = '10000001'
            flag = 1

        if flag == 1:
            tick += 1
            print("gewoon tick" + str(tick))
            antwoord = '10000001'
            if tick == 12:
                antwoord = temp
            elif tick == 15:
                flag = 0
                tick = 0
        
        senCommand(antwoord)   
        
        time.sleep(0.15)
           
except Exception as e:
    print(f"An error occurred: {e}")
    client_socket = make_socket()
    client_socket.send("disconnect".encode('utf-8'))
    client_socket.close()
