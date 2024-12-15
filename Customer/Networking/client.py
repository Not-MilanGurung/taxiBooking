import socket
import pickle

HEADER = 64     # Byte size for the first message
PORT = 5020
FORMAT = 'utf-8'
DISCONNECT = 'DISCONNECT!#'     # Keyword used to signal server to disconnect
SERVER = socket.gethostbyname(socket.gethostname())     # When used in the same computer

class Client(socket.socket):
    def __init__(self, family: socket.AddressFamily = socket.AF_INET, type: socket.SocketKind = socket.SOCK_STREAM, serverIP: str= SERVER):
        super().__init__(family, type)
        self.addr = (serverIP, PORT)    # Assigining the address of the server to connect to
        self.connectToServer()

    def connectToServer(self):
        self.connect(self.addr)

    def sendToServer(self, msg: list | str):
        # Encode the message into bytes with pickle
        message = pickle.dumps(msg)
        msg_len = len(message)

        # Encoding the length into format
        msg_len = str(msg_len).encode(FORMAT)

        # Padding the message to equal the right length
        msg_len += b' ' * (HEADER - len(msg_len))

        # Sending the server the length of the message
        self.send(msg_len)
        # Sending the message
        self.send(message)

    def recive(self):
        msg_len = self.recv(HEADER).decode(FORMAT)
        if msg_len:     # Checking if the message is blank 
            msg_len = int(msg_len)

            msg = pickle.loads(self.recv(msg_len))      # Decode the message encode through pickle
            return msg

    def disconnect(self):
        self.sendToServer(DISCONNECT)
