import socket
import threading

# Function to handle client connections
def handle_client(client_socket, client_address):
    print(f"Connection from {client_address}")

    while True:
        # Receive message from client
        message = client_socket.recv(1024).decode()
        if not message:
            break

        print(f"{client_address[0]}: {message}")

        # Check if client wants to exit
        if message.strip() == "exit":
            break

        # Broadcast message to all clients except the sender
        broadcast(message, client_socket)

    print(f"Connection with {client_address} closed.")
    client_socket.close()

# Function to broadcast message to all clients
def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode())
            except:
                client.close()
                remove(client)

# Function to remove a client from the list
def remove(client):
    if client in clients:
        clients.remove(client)

# Server configuration
HOST = '127.0.0.1'  # Localhost
PORT = 12345

# Create socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind socket to address and port
server_socket.bind((HOST, PORT))

# Listen for incoming connections
server_socket.listen(2)
print(f"Server listening on {HOST}:{PORT}")

clients = []

while True:
    # Accept incoming connection
    client_socket, client_address = server_socket.accept()

    # Add client socket to the list
    clients.append(client_socket)

    # Create a new thread to handle client connection
    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.start()
