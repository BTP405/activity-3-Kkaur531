import os  # Importing the operating system module for interacting with the operating system
import socket  # Importing the socket module for networking
import pickle  # Importing the pickle module for object serialization
import time  # Importing the time module for timing operations
from multiprocessing import Pool  # Importing Pool from multiprocessing for parallel processing

# The TaskQueueClient class handles communication with the task queue server
class TaskQueueClient:
    def __init__(self, host, port):
        self.host = host  # Server's IP address
        self.port = port  # Server's port number
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Creating a TCP/IP socket
        self.socket.connect((host, port))  # Connecting to the task queue server

    # Method to send a task to the server
    def send_task(self, task):
        task_data = pickle.dumps(task)  # Pickling the task
        self.socket.sendall(task_data)  # Sending the pickled task to the server

    # Method to receive a result from the server
    def receive_result(self):
        result_data = self.socket.recv(4096)  # Receiving the result data from the server
        result = pickle.loads(result_data)  # Unpickling the result data
        return result  # Returning the unpickled result

    # Method to close the socket connection
    def close(self):
        self.socket.close()  # Closing the socket connection

# Main function to run the client application
def main():
    host = '127.0.0.1'  # Server's IP address (replace with the actual server's IP)
    port = 12345  # Server's port number (replace with the actual server's port)

    client = TaskQueueClient(host, port)  # Creating a TaskQueueClient instance to connect to the server

    # Define the tasks to be executed
    tasks = [
        (lambda: 1 + 1),  # Task to add 1 + 1
        (lambda: 2 * 2),  # Task to multiply 2 * 2
        (lambda: 3 ** 3),  # Task to calculate 3 raised to the power of 3
    ]

    # Use a process pool to execute the tasks in parallel
    with Pool() as pool:
        results = pool.imap_unordered(execute_task, tasks)  # Using parallel processing to execute tasks

    # Send the tasks to the task queue server
    for task in tasks:
        client.send_task(task)  # Sending each task to the server

    # Receive the results from the task queue server
    for _ in tasks:
        result = client.receive_result()  # Receiving the result for each task from the server
        print(f"Received result: {result}")  # Printing the received result

    client.close()  # Closing the client socket connection

# Function to execute a task
def execute_task(task):
    return task()  # Executing the task and returning the result

# Ensuring the main function is called when the script is executed
if __name__ == "__main__":
    main()
