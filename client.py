import socket
import threading
import sys

def receive_messages():
    while True:
        try:
            # Receive message from server
            message = client_socket.recv(1024).decode()
            if not message:
                break

            print(message)
        except ConnectionAbortedError:
            # Connection was closed by the server or server terminated unexpectedly
            break

# Client configuration
HOST = '127.0.0.1'  # Localhost
PORT = 12345

# Connect to server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# Receive username from user
username = input("Enter your username: ")
client_socket.send(username.encode())

# Start a thread to receive messages from the server
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

# Send messages to server
while True:
    message = input()
    if message.lower() == 'exit':
        client_socket.sendall(message.encode())
        print("Exiting chat.")
        client_socket.close()
        sys.exit(0)
    else:
        client_socket.sendall(f"{username}: {message}".encode())
