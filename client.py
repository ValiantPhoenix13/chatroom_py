# This will be the client side of the program
# The program will continuously ask for inputs for the server 

# Import required libraries
import sys
import socket
import threading

# The main function that will operate as a client
def main():
    # Check to see if the inputs are valid
    if (len(sys.argv) != 3):
        print("Usage: python client.py <server_ip> <server_port>")
        sys.exit(1)
    host = sys.argv[1]
    # Define the port
    port = int(sys.argv[2])
    # Create a network connection using TCP
    svr_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server via localhost/local computer
    svr_socket.connect((host, port))
    # List the possible actions in the chatroom
    print("You've connected to the server that is a chatroom.")
    print("Possible actions are as follows:")
    print("JOIN <username>: Allows you to join the chatroom if there's space with the provided username.")
    print("LIST: Shows all current active users and their usernames in the chatroom.")
    print("MESG <username> <message>: Allows you to privately message a specific user uses their username and sending them the provided message.")
    print("BCST <message>: Will broadcast the provided message to all users in the chatroom")
    print("QUIT: Will remove you from the chatroom, if you're an active user, and the server will disconnect you from the user")
    

    # Defining a function to accept broadcast
    def receive():
        while True:
            try:
                message = svr_socket.recv(1024).decode('ascii')
                print(message)
                # Check to see if the QUIT command was sent
                if (str(message) == "Disconnecting"):
                    svr_socket.close()
                    print("Disconnected")
                    break
                else:
                    continue
            except Exception as e:
                print(e)
                svr_socket.close()
                break

    # Define the actions the user can do
    def write():
        while True:
            # Define the request to be sent to the server
            command = input("")
            # Send to the server
            svr_socket.send(command.encode('ascii'))
            # Receive the server response
            # response = svr_socket.recv(1024)
            # print(str(response.decode('ascii')))

            # Check use case errors in commands/request
            if sys.argv[0] == "JOIN":
                if sys.argv != 1:
                    print("To use JOIN must provide a username with no special characters or spaces. \nUsage: JOIN <username>")
            if sys.argv[0] == "LIST":
                if sys.argv != 0:
                    print("To use LIST no other words or spaces should be provided. \nUsage: LIST")
            if sys.argv[0] == "BCST":
                if sys.argv < 1:
                    print("To use BCST you must provide a message of somekind. \nUsage: BCST <message>")
            if sys.argv[0] == "MESG":
                if sys.argv < 2:
                    print("To use MESG a username and message must be provided, be sure that the start of the message is seperated from the username with a space.\n Usage: MESG <username> <message>")
            

    
    # Start both threads, one for receiving and one for commands
    thread_receive = threading.Thread(target=receive)
    thread_command = threading.Thread(target=write)
    thread_command.start()
    thread_receive.start()



if __name__ == '__main__':
    main()