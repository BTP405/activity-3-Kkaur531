#Implement a client-server file transfer application where the client sends a file to the server using sockets. 
#Before transmitting the file, pickle the file object on the client side. On the server side, receive the pickled file object, unpickle it, and save it to disk.


#Requirements:
#The client should provide the file path of the file to be transferred.
#The server should specify the directory where the received file will be saved.
#Ensure error handling for file I/O operations, socket connections, and pickling/unpickling.


import os  # Importing the operating system module for file handling
import socket  # Importing the socket module for networking
import pickle  # Importing the pickle module for object serialization
from pathlib import Path  # Importing Path class for handling file paths

BUFFER_SIZE = 4096  # Defining the buffer size for data transfer

def send_file(client_socket, file_path):
    try:
        with open(file_path, 'rb') as file:  # Opening the file in binary read mode
            file_data = file.read()  # Reading the file data
            file_obj = Path(file_path)  # Creating a Path object for the file
            file_info = {'name': file_obj.name, 'data': file_data}  # Creating a dictionary with file information
            file_data_pickle = pickle.dumps(file_info)  # Pickling the file information
            client_socket.sendall(file_data_pickle)  # Sending the pickled data
            print(f"Sent {file_path}")  # Printing a message indicating successful file transmission
    except FileNotFoundError:  # Handling file not found error
        print(f"File not found: {file_path}")  # Printing error message
        client_socket.close()  # Closing the client socket
    except Exception as e:  # Handling other exceptions
        print(f"Error sending file: {e}")  # Printing error message
        client_socket.close()  # Closing the client socket

def main():
    server_ip = '127.0.0.1'  # Server's IP address (change this to the server's actual IP)
    server_port = 12345  # Server's port number (change this to the server's actual port)
    file_path = 'test.txt'  # Path to the file to be sent

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Creating a TCP/IP socket
    client_socket.connect((server_ip, server_port))  # Connecting to the server

    send_file(client_socket, file_path)  # Calling function to send file to server

    client_socket.close()  # Closing the client socket

if __name__ == "__main__":
    main()  # Calling the main function when the script is executed
