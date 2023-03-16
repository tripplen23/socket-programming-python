import socket
import threading

HEADER = 64
#Pick the port and the server
PORT = 5050
#SERVER = "192.168.0.53"
SERVER = socket.gethostbyname(socket.gethostname()) #Get the IP address automatically
print(SERVER)
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

#Socket that's going to allow us to open up kind of this device to other connections
#Pick the socket 
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Bind the socket to the address
server.bind(ADDR)


#Handle client
def handle_client(connection, address):
    print(f"[NEW CONNECTION] {address} connected.")

    connected = True
    while connected:
        msg_length = connection.recv(HEADER).decode(FORMAT)
        if msg_length: 
            msg_length = int(msg_length)
            msg = connection.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False

            print(f"[{address}] {msg}")
            connection.send("Message receive".encode(FORMAT))
    
    connection.close()
        

#Handle new connections 
def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        connection, address = server.accept()
        thread = threading.Thread (target=handle_client, args=(connection, address)) #Threading module in Python3
        thread.start()
        print(f"[ACTIVE CONNECTION] {threading.activeCount() - 1}") #How many thread are on active process in this Python process
        #There is 1 active connection when there is 2 threads running


print("[STARTING] server is starting...")
start()



