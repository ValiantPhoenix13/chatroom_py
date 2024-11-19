# This will be the server side of the program
# The program will start once a port number is provided
# If a port number isn't provided a usage statement will be printed
# The server will support up to 10 active users
# The server will establish a network socket with a TCP connection 
# When a client connects a new thread should be started using POSIX
# The server will provide status updates as functions are called
# The server has the following functions:
# JOIN <username>
# LIST
# MESG <username><message>
# BCST <message>
# QUIT
# Any unknown request should be repsonded with "Unknown request"

# Import necessary libraries
import socket
import threading
import sys

active_count = 0
active_clients = []
usernames = []
clients = []

# Method used for the server to receive request
def handle(client_socket):
    while True:
        data = client_socket.recv().decode()
        if data.startswith("JOIN "):
            username = data[5:]
            JOIN(username)
            

# Creating the server
def create_server(port):
    # Creating a socket on the network with a TCP connection
    svr_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Binding the server to an address and port
    svr_socket.bind("127.0.0.1", port)
    # Server will start listening
    svr_socket.listen(1)
    
    print("The server is listening on port: ", port)
    
    # Continuously search for clients
    while True:
        client_socket, client_address = svr_socket.accept()
        print(f"Accepted connection from: {client_address}")
        
        # Create a thread for this specific client
        client_thread = threading.Thread(target=handle, args=(client_socket,))
        client_thread.start()

# The main function will be used to start the server
def main():
    # Check that the number of arguments provided is legal
    if len(sys.argv) != 2:
        print("Usage: python server.py <port>")
        sys.exit(1)
    # If the arguments are valid turn on the server using the procided port
    port = int(sys.argv[1])
    create_server(port)
    
if __name__=='__main__':
    main()

# The JOIN function will add a client to the chatroom
def JOIN(username):
    return

# The LIST function will display all active users in the chatroom
def LIST():
    return

# The MESG function will send a private message to the username provided
def MESG(username, message):
    return

# The BCST function will broadcast a message to all active users
def BCST(message):
    return

# The QUIT function will disconnect the user and remove them from the active 10 users
def QUIT():
    return

