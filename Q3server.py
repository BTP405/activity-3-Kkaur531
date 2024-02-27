#Real-Time Chat Application with Pickling:

#Develop a simple real-time chat application where multiple clients can communicate with each other via a central server using sockets. 
#Messages sent by clients should be pickled before transmission. The server should receive pickled messages, unpickle them, and broadcast them to all connected clients.


#Requirements:
#Implement separate threads for handling client connections and message broadcasting on the server side.
#Ensure proper synchronization to handle concurrent access to shared resources (e.g., the list of connected clients).
#Allow clients to join and leave the chat room dynamically while maintaining active connections with other clients.
#Use pickling to serialize and deserialize messages exchanged between clients and the server.


import os  # Importing the operating system module for interacting with the operating system
import socket  # Importing the socket module for networking
import pickle  # Importing the pickle module for object serialization
import threading  # Importing the threading module for concurrent execution

# The ChatServer class represents a simple chat server
class ChatServer:
    def __init__(self, host, port):
        self.host = host  # Server's IP address
        self.port = port  # Server's port number
        self.clients = []  # List to store client sockets
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Creating a TCP/IP socket
        self.socket.bind((host, port))  # Binding the socket to the server IP and port
        self.socket.listen(5)  # Listening for incoming connections with a backlog of 5
        self.lock = threading.Lock()  # Creating a lock for thread safety

    # Method to broadcast a message to all clients except the sender
    def broadcast_message(self, message, sender):
        with self.lock:  # Acquiring the lock to ensure thread safety
            for client in self.clients:  # Iterating over all connected clients
                if client != sender:  # Checking if the client is not the sender
                    client.sendall(pickle.dumps(message))  # Sending the message to the client

    # Method to handle communication with a client
    def handle_client(self, client_socket):
        while True:  # Loop to continuously receive messages from the client
            try:
                message = pickle.loads(client_socket.recv(4096))  # Receiving a message from the client
                if message:  # Checking if the message is not empty
                    print(f"Received message from {client_socket.getpeername()}: {message}")  # Printing the received message
                    self.broadcast_message(message, client_socket)  # Broadcasting the message to all clients
                else:
                    break  # Exiting the loop if the message is empty
            except EOFError:  # Handling end of file error (client closed the connection)
                break  # Exiting the loop
            except Exception as e:  # Handling other exceptions
                print(f"Error handling client: {e}")  # Printing the error message
                break  # Exiting the loop

        with self.lock:  # Releasing the lock to modify the clients list
            self.clients.remove(client_socket)  # Removing the client socket from the list
        client_socket.close()  # Closing the client socket

    # Method to accept incoming client connections
    def accept_clients(self):
        while True:  # Loop to continuously accept client connections
            client_socket, client_address = self.socket.accept()  # Accepting a new client connection
            print(f"New connection from {client_address}")  # Printing a message indicating the new connection

            with self.lock:  # Acquiring the lock to ensure thread safety
                self.clients.append(client_socket)  # Adding the client socket to the clients list

            thread = threading.Thread(target=self.handle_client, args=(client_socket,))  # Creating a new thread to handle the client
            thread.start()  # Starting the thread

# Main function to run the chat server
def main():
    host = '127.0.0.1'  # Server's IP address (replace with the actual server's IP)
    port = 12345  # Server's port number (replace with the actual server's port)

    server = ChatServer(host, port)  # Creating a ChatServer instance

    # Handle new client connections in a separate thread
    accept_thread = threading.Thread(target=server.accept_clients)  # Creating a thread to accept client connections
    accept_thread.start()  # Starting the thread

    # Wait for user input to broadcast messages
    while True:  # Loop to continuously prompt the user for messages
        message = input("Enter a message to broadcast: ")  # Prompting the user to enter a message
        if message:  # Checking if the message is not empty
            server.broadcast_message(message, server.socket)  # Broadcasting the message to all clients

# Ensuring the main function is called when the script is executed
if __name__ == "__main__":
    main()
