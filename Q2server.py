#Distributed Task Queue with Pickling:

#Create a distributed task queue system where tasks are sent from a client to multiple worker nodes for processing using sockets. 
#Tasks can be any Python function that can be pickled. Implement both the client and worker nodes. 
#The client sends tasks (pickled Python functions and their arguments) to available worker nodes, and each worker node executes the task and returns the result to the client.

#Requirements:
#Implement a protocol for serializing and deserializing tasks using pickling.
#Handle task distribution, execution, and result retrieval in both the client and worker nodes.
#Ensure fault tolerance and scalability by handling connection errors, timeouts, and dynamic addition/removal of worker nodes.


import os  # Importing the operating system module for interacting with the operating system
import socket  # Importing the socket module for networking
import pickle  # Importing the pickle module for object serialization
import time  # Importing the time module for timing operations

# The TaskQueueWorker class represents a worker that communicates with the task queue server
class TaskQueueWorker:
    def __init__(self, worker_id, host, port):
        self.worker_id = worker_id  # Worker's ID
        self.host = host  # Server's IP address
        self.port = port  # Server's port number
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Creating a TCP/IP socket
        self.socket.connect((host, port))  # Connecting to the task queue server

    # Method to receive a task from the server
    def receive_task(self):
        task_data = self.socket.recv(4096)  # Receiving task data from the server
        task = pickle.loads(task_data)  # Unpickling the task data to get the actual task
        return task  # Returning the received task

    # Method to send a result back to the server
    def send_result(self, result):
        result_data = pickle.dumps(result)  # Pickling the result
        self.socket.sendall(result_data)  # Sending the pickled result to the server

    # Method to close the socket connection
    def close(self):
        self.socket.close()  # Closing the socket connection

# Main function to run the worker application
def main():
    worker_id = input("Enter worker ID: ")  # Getting the worker ID from the user
    host = '127.0.0.1'  # Server's IP address (replace with the actual server's IP)
    port = 12345  # Server's port number (replace with the actual server's port)

    worker = TaskQueueWorker(worker_id, host, port)  # Creating a TaskQueueWorker instance

    while True:  # Loop to continuously receive and execute tasks
        try:
            task = worker.receive_task()  # Receiving a task from the server
            result = task()  # Executing the received task and getting the result
            worker.send_result(result)  # Sending the result back to the server
        except EOFError:  # Handling end of file error (server closed the connection)
            print("Task queue server closed the connection")  # Printing a message
            break  # Exiting the loop
        except Exception as e:  # Handling other exceptions
            print(f"Error executing task: {e}")  # Printing the error message
            break  # Exiting the loop

    worker.close()  # Closing the worker's socket connection

# Ensuring the main function is called when the script is executed
if __name__ == "__main__":
    main()
