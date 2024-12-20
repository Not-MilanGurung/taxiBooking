import socket
import threading
import pickle
import Database.query as Query
import tkinter as tk
from tkinter import messagebox


HEADER = 64 # First message length in bytes
PORT = 5020 
SERVER = socket.gethostbyname(socket.gethostname()) # Get this computer's local IPv4 
FORMAT = 'utf-8'
# Keywords
DISCONNECT = 'DISCONNECT!#'
REGISTER = 'REGISTER'


class Server(socket.socket):

    def __init__(self, family: socket.AddressFamily = socket.AF_INET, type: socket.SocketKind = socket.SOCK_STREAM, port: int = PORT , server: str = SERVER):
        super().__init__(family, type)
        self.bind((server, port))   # Binding the socket to the server ip and port
        self.server = server
        self.port = port
        self.started = False
        self.settimeout(1.0)    # Setting the timeout to 1 seconds

    # Making sure the input matches the user identifier keyword 
    def classify_user(self, message):
        if message[0] in ('CUSTOMER' ,'DRIVER' ,'ADMIN'):
            return message[0], message[1:]
        return False, None

    # Handles the first identifying message
    def identify_client(self, con: socket.socket, addr):
        user = False
        id = None
        msg_arr = list

        # Classifying the type of user
        while True:
            msg = self.recive(con)      # Receving the message
            if msg is None: continue    # Checking if the message is empty

            if msg == DISCONNECT:       # Breaking the loop 
                break
                
            user, msg_arr = self.classify_user(msg) # Identifying user type
            if user == False:
                self.send('INCORRECT USER TYPE', con)
                continue

            if msg_arr[0] == REGISTER:      # Registering 
                res = Query.register(user, msg_arr) # Quering the database with the recived data
                self.send(res,con)  # Send the response back
                continue

            id = Query.login(user, msg_arr) # Quering databse for login operation
            # If the login was not scuessful, sending the error message back
            if type(id) != int:
                self.send(id, con)
                continue

            self.send('Sucess', con)    # Login successful message
            self.handle_client(con, addr, user, id) # Calling the function that handles the operations after login
            break
        
        con.close() # Closing the connection after disconnecting

    
    def handle_client(self, con, addr, user, id):
        # Sending the profile info
        # Operation handling loop
        while True:
            msg = self.recive(con)  # Recive message

            if msg == DISCONNECT:   # Disconnect 
                break 
            match msg[0]:
                case 'BOOK':      # Customer booking request
                    res = Query.book(id, msg)
                    self.send(res, con)
                case 'PROFILE':     # Returns user's profile info
                    self.send(Query.profile_info(user, id), con)

                case 'CURRENT_RIDE':  # Driver and Customer current ride info
                    self.send(Query.current_ride(user, id), con)
                    
                case 'ASSIGINED':   # Driver assigined rides list
                    self.send(Query.assigined_rides_driver(user, id), con)   

                case 'CANCEL':      # Customer cancel ride
                    self.send(Query.cancel_ride(user, id), con)

                case 'HISTORY':     # Driver and Customer ride history 
                    self.send(Query.ride_history(user, id), con)

                case 'DRIVER_STATUS':   # Driver status update
                    self.send(Query.driver_status(id, msg[1]), con)

                case 'SELECT':   # Driver select current ride
                    self.send(Query.select_ride_driver(msg[1], id), con)

                case 'CHANGE':   # Driver change current ride
                    self.send(Query.change_current_ride(id), con)

                case 'COMPLETED':   # Driver: Mark the current ride completed
                    self.send(Query.complete_ride(user, id), con)
                case _:
                    pass


    def recive(self, con):
        # Reciving the message of HEADER length about the length of upcoming message in bytes
        msg_len = con.recv(HEADER).decode(FORMAT)
        # checking msg_len is not null
        if msg_len:
            msg_len = int(msg_len) # Converting from string to integer

            msg = pickle.loads(con.recv(msg_len)) # Decoding the message
            # print(msg, con) For debugging
            return msg

    def send(self, msg, con):
        # Encoding the message to bytes
        message = pickle.dumps(msg)

        msg_len = len(message)

        # Encoding the length into format
        msg_len = str(msg_len).encode(FORMAT)

        # Padding the message to equal the right length
        msg_len += b' ' * (HEADER - len(msg_len))

        # Sending the server the length of the message
        con.send(msg_len)
        # print(msg) For debugging
        # Sending the message
        con.send(message)

    def start(self):
        print (f'[SERVER]: Server started {self.server} {self.port}')   # Give the server ip and port
        self.listen()   # Listen for connection
        self.started = True # Set the server status as started
        while self.started:
            try:
                con, addr = self.accept()   # Wait and accept connection
                # Start a thread that handles the above connection
                thread = threading.Thread(target=self.identify_client, args=(con, addr))   
                thread.daemon = True    # Close thread when the main program closes
                thread.start()

            except socket.timeout:  # Stop and loop to allow the self.started variable to be checked
                pass

        self.close()    # Close server
        print('Stopped server')

    # Function to stop the Server socket
    def stop(self):
        print('Stopping server')
        self.started = False

# Function to start the server
def start_server():
    # Using the global variables
    global server, thread, started
    # Checking the server status
    if not(started):
        server = Server()   # Creating a server object
        thread = threading.Thread(target=server.start)  # Defining the thread that will handle server
        thread.daemon = True    # Closes the thread with the main program
        thread.start()          # Starting the tread
        started = True          # Setting server status
    else:
        messagebox.showinfo('Already running', 'The server is already running')

# Function that stops the server
def stop_server():
    # Using the global variables
    global server, thread, started
    #Checking if the server is running or not
    if started:
        server.stop()   # Closing the server socket
        thread.join()   # Waiting for the connection accepting thread to close
        started = False # Setting server status as stopped
        messagebox.showinfo('Stopped', 'Server stopped')
    else:
        messagebox.showinfo('Not started', 'The server has not been started')
        
    

if __name__ == '__main__':
    # Defining the root application and setting a title
    root = tk.Tk()
    root.title('Server')
    # Global variable linked with the status of the server
    global started
    started = False

    # Button to start the server
    start = tk.Button(root, text='Start the server', command=start_server)
    start.grid(row=0, column=0, padx= 20, pady=20, sticky='')
    # Button to stop the server
    stop = tk.Button(root, text='Stop server', command=stop_server)
    stop.grid(row=1, column=0, padx= 20, pady=20, sticky='')

    # Starting the tk mainloop
    root.mainloop()


