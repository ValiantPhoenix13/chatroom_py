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

# Method used for the server to receive request
def handle(client_socket, client_address):
    global active_count
    while True:
        data = client_socket.recv(1024).decode('ascii')

        # Defining the JOIN command
        if (data.startswith("JOIN ") and len(active_clients) < 10):
            # Check to see if the username is taken
            if data[5:] in usernames:
                client_socket.send((f"Unfortunately {data[5:]} is already taken, please choose a different username").encode('ascii'))
                print(f"{client_address} tried to use the username {data[5:]}, but it was already taken.")
            elif client_socket in active_clients:
                client_socket.send((f"You are already an active chatter").encode('ascii'))
                print(f"{client_address} tried to JOIN, but he was already active.")
            else:
                username = data[5:]
                active_count += 1
                usernames.append(username)
                active_clients.append(client_socket)
                # Send a status to the client
                client_socket.send((f"You've joined the chatroom with the username: {username}").encode('ascii'))
                # Display the status on the server side
                print(f"{username} has joined the chatroom with address {client_address}")

        # Defining the LIST command
        if (data == "LIST" and (client_socket in active_clients) and data[5] != " "):
            # Send the client who requested the active users a list of active users
            list = "The active users include: " # Can only send one response per command str to be sent
            for clients in range(len(active_clients)):
                list = list + usernames[clients] + ", "
            client_socket.send(f"{list}".encode('ascii'))
            # Dispaly the status on the server side
            index = active_clients.index(client_socket)
            print(f"{usernames[index]} requested a list of active users.")

        # Defining the BCST command
        if (data.startswith("BCST ") and (client_socket in active_clients)):
            index = active_clients.index(client_socket)
            username = str(usernames[index])
            broadcast = username + ": " + str(data[5:])
            # Send a message to each active client
            for clients in active_clients:
                clients.send((f"{broadcast}").encode('ascii'))

            # Display the status on the server
            index = active_clients.index(client_socket)
            print(f"{usernames[index]} broadcasted a message.")

        # Defining the MESG command
        if (data.startswith("MESG ") and (client_socket in active_clients)):
            contents = data[5:]
            # Seperate the username from the message
            contents_list = contents.split()
            if contents_list[0] in usernames:
                # Find the address of the recipient
                index_recipient = usernames.index(contents_list[0])
                recipient = active_clients[index_recipient]
                # Find the index of the sender
                index_sender = active_clients.index(client_socket)
                sender = usernames[index_sender]
                # Build the message
                message = (" ".join(str(words) for words in contents_list[1:]))
                to_send = sender + ": " + message
                # Send the message
                recipient.send((to_send).encode('ascii'))
                client_socket.send((f"Your message was sent.").encode('ascii'))
                # Display the status on the server side
                print(f"{sender} sent a private message to {usernames[index_recipient]}.")
            else:
                # The username is not an active user
                client_socket.send((f"{contents_list[0]} is not an active user."))
                # Display the status on the server side
                index = active_clients.index(client_socket)
                print(f"{usernames[index]} tried to send a private message to an unactive user.")

        # Catch any users trying to use chatroom commands when not an active user
        if (data.startswith("LIST") and (client_socket not in active_clients)):
            # Tell client how to join chatroom
            client_socket.send((f"To use LIST you must be an active user. Use JOIN <username> to become active and if there's space you will be added.").encode('ascii'))
            # Display status on server
            print(f"{client_socket} attempted to use a command that required them to be an active chatter.")
        if (data.startswith("BCST") and (client_socket not in active_clients)):
            # Tell client how to join chatroom
            client_socket.send((f"To use BCST you must be an active user. Use JOIN <username> to become active and if there's space you will be added.").encode('ascii'))
            # Display status on server
            print(f"{client_socket} attempted to use a command that required them to be an active chatter.")
        if (data.startswith("MESG") and (client_socket not in active_clients)):
            # Tell client how to join chatroom
            client_socket.send((f"To use MESG you must be an active user. Use JOIN <username> to become active and if there's space you will be added.").encode('ascii'))
            # Display status on server
            print(f"{client_socket} attempted to use a command that required them to be an active chatter.")

        # Defining the QUIT command
        if (data.startswith("QUIT")):
            # Decrement active users
            active_count -= 1
            # Remove active user's data from chatroom
            index = active_clients.index(client_socket)
            active_clients.remove(index)
            usernames.remove(index)

            # Send status to client
            client_socket.send(("Disconnecting").encode('ascii'))
            # Display status on server
            print(f"{client_socket} has disconnected from the chatroom. There are now {active_count} active users.")
            break

        else:
            client_socket.send(("Unknown command").encode('ascii'))
    client_socket.close()
            

# Creating the server
def create_server(port):
    # Creating a socket on the network with a TCP connection
    svr_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Binding the server to an address and port
    svr_socket.bind(("127.0.0.1", port))
    # Server will start listening
    svr_socket.listen(5)
    
    print("The server is listening on port: ", port)
    
    # Continuously search for clients
    while True:
        client_socket, client_address = svr_socket.accept()
        slots_available = 10 - len(active_clients)
        print(f"Accepted connection from: {client_address}")
        print(f"There are {slots_available} spots available in the chatroom!")
        # client_socket.send(("Joined the server").encode('ascii'))
        
        # Create a thread for this specific client
        client_thread = threading.Thread(target=handle, args=(client_socket, client_address,))
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
