import socket
import threading
import pickle
import Database.query as Query
import sys


HEADER = 64
PORT = 5020
SERVER = socket.gethostbyname(socket.gethostname()) # Get this computer's local IPv4 
FORMAT = 'utf-8'
DISCONNECT = 'DISCONNECT!#'
REGISTER = 'REGISTER'
BOOK = 'BOOK'
CURRENT_RIDE = 'CURRENT_RIDE'
CANCEL = 'CANCEL'
HISTORY = 'HISTORY'
ASSIGINED = 'ASSIGINED'

class Server(socket.socket):

    def __init__(self, family: socket.AddressFamily = socket.AF_INET, type: socket.SocketKind = socket.SOCK_STREAM, port: int = PORT , server: str = SERVER):
        super().__init__(family, type)
        self.bind((server, port))

        print (f'[SERVER]: Server started {server} {port}')
        self.start()

    def singal_handler(sig, frame):
        print('Keyboard')
        sys.exit(0)

    def classify_user(self, message):
        if message[0] in ('CUSTOMER' ,'DRIVER' ,'ADMIN'):
            return message[0], message[1:]
        return False, None

    def identify_client(self, con: socket.socket, addr):

        user = False
        id = None
        msg_arr = list


        # Classifying the type of user
        while True:
            msg = self.recive(con)
            if msg is None: continue
            if msg == DISCONNECT:
                break
                
            user, msg_arr = self.classify_user(msg)
            if user == False:
                self.send('INCORRECT USER TYPE', con)
                continue
            if msg_arr[0] == REGISTER:
                res = Query.register(user, msg_arr) 
                self.send(res,con)
                continue

            id = Query.login(user, msg_arr)
            if type(id) != int:
                self.send(id, con)
                continue

            self.send('Sucess', con)
            self.handle_client(con, addr, user, id)
            break

        con.close()

    
    def handle_client(self, con, addr, user, id):
        self.send(Query.profile_info(user, id), con)
        while True:
            msg = self.recive(con)
            if msg == DISCONNECT:
                break 
            if msg[0] == BOOK:
                res = Query.book(id, msg)
                self.send(res, con)
                continue
            if msg[0] == CURRENT_RIDE:
                self.send(Query.current_ride(user, id), con)
            if msg[0] == ASSIGINED:
                self.send(Query.current_rides_driver(user, id), con)    
            if msg[0] == CANCEL:
                self.send(Query.cancel_ride(user, id), con)
            if msg[0] == HISTORY:
                self.send(Query.ride_history(user, id), con)


    def recive(self, con):
        msg_len = con.recv(HEADER).decode(FORMAT)

        if msg_len:
            msg_len = int(msg_len)

            msg = pickle.loads(con.recv(msg_len))
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

        # Sending the message
        con.send(message)

    def start(self):
        self.listen()
        while True:
            try:
                print('Hello')
                con, addr = self.accept()
                print('Hello')
            except KeyboardInterrupt:
                print('Hello')
                break
            thread = threading.Thread(target=self.identify_client, args=(con, addr))
            thread.daemon = True
            thread.start()




    def stop(self):
        print('Stopping server')
        self.close()

if __name__ == '__main__':
    server = Server()
    server.stop()

    print('[SERVER STOPPED]')


