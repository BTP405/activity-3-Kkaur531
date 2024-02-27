import os  # Importing the operating system module for interacting with the operating system
import socket  # Importing the socket module for networking
import pickle  # Importing the pickle module for object serialization
import threading  # Importing the threading module for concurrent execution

# The ChatClient class represents a client for the chat server
class ChatClient:
    def __init__(self, host, port):
        self.host = host  # Server's IP address
        self.port = port  # Server's port number
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Creating a TCP/IP socket
        self.socket.connect((host, port))  # Connecting to the chat server

    # Method to receive messages from the chat server
    def receive_messages(self):
        while True:  # Loop to continuously receive messages
            try:
                message = pickle.loads(self.socket.recv(4096))  # Receiving a message from the server
                if message:  # Checking if the message is not empty
                    print(f"Received message: {message}")  # Printing the received message
                else:
                    break  # Exiting the loop if the message is empty
            except EOFError:  # Handling end of file error (server closed the connection)
                break  # Exiting the loop
            except Exception as e:  # Handling other exceptions
                print(f"Error receiving message: {e}")  # Printing the error message
                break  # Exiting the loop

        self.socket.close()  # Closing the client socket

# Main function to run the chat client
def main():
    host = '127.0.0.1'  # Server's IP address (replace with the actual server's IP)
    port = 12345  # Server's port number (replace with the actual server's port)

    client = ChatClient(host, port)  # Creating a ChatClient instance

    # Receive messages from the chat server in a separate thread
    receive_thread = threading.Thread(target=client.receive_messages)  # Creating a thread to receive messages
    receive_thread.start()  # Starting the thread

    # Send messages to the chat server
    while True:  # Loop to continuously prompt the user for messages to send
        message = input("Enter a message to send: ")  # Prompting the user to enter a message
        if message:  # Checking if the message is not empty
            client.socket.sendall(pickle.dumps(message))  # Sending the message to the server

# Ensuring the main function is called when the script is executed
if __name__ == "__main__":
    main()
