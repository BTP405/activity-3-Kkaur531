import os  # Importing the operating system module for file handling
import socket  # Importing the socket module for networking
import pickle  # Importing the pickle module for object serialization
from pathlib import Path  # Importing Path class for handling file paths

BUFFER_SIZE = 4096  # Defining the buffer size for data transfer

def receive_file(server_socket, save_directory):
    try:
        file_data = server_socket.recv(BUFFER_SIZE)  # Receiving file data from the client
        while file_data:  # Continue until all file data is received
            file = pickle.loads(file_data)  # Unpickle the received file object
            file_name = file.name  # Extracting the file name from the file object
            file_path = os.path.join(save_directory, file_name)  # Constructing the file path in the save directory
            with open(file_path, 'wb') as file:  # Opening the file in binary write mode
                file.write(file.read())  # Writing the file data to the opened file
                print(f"Received {file_name}")  # Printing a message indicating successful file reception
            file_data = server_socket.recv(BUFFER_SIZE)  # Receiving more file data
    except EOFError:  # Handling end of file error
        print("File transfer complete")  # Printing message indicating file transfer completion
    except Exception as e:  # Handling other exceptions
        print(f"Error receiving file: {e}")  # Printing error message
        server_socket.close()  # Closing the server socket in case of error

def main():
    server_ip = '127.0.0.1'  # Server's IP address 
    server_port = 12345  # Server's port number
    save_directory = 'received_files'  # Directory to save received files

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Creating a TCP/IP socket
    server_socket.bind((server_ip, server_port))  # Binding the socket to the server IP and port
    server_socket.listen(1)  # Listening for incoming connections with a backlog of 1

    client_socket, client_address = server_socket.accept()  # Accepting a client connection

    receive_file(client_socket, save_directory)  # Calling function to receive file from client

    client_socket.close()  # Closing the client socket
    server_socket.close()  # Closing the server socket

if __name__ == "__main__":
    main()  # Calling the main function when the script is executed
