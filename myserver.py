#imports
import sys
from ex2utils import Server

#create server class
class MyServer(Server):


    def onStart(self):
        self.clientCount = 0
# error codes: 0 no no erroor     1 error in users name
        self.client_store = {}
        self.txt = "Total Clients = {}"
        self.txr = "MESSAGE FROM {}"
        self.c1 = "NAME"
        self.c2 = "MSGALL"
        self.c3 = "MSGIND"
        self.c4 = "LIST"
        self.c5 = "CLOSE"
        print("My server has started")

    def onConnect(self, socket):
        print("Client has connected")
        self.clientCount+=1
        print(self.txt.format(self.clientCount))
        socket.send(b"WELCOME TO CHAT CLIENT!!!\n \n please use one of the following commands... \n NAME <register your name> \n MSGALL <add msg here> \n MSGIND <USER> <add msg here> \n LIST \n CLOSE\n\n")

    def onMessage(self, socket, message):
        print("Message Recieved:")
        # print("stripping up message from client")
        (command, sep, parameter) = message.strip().partition(' ')

# save the name of the sender if the message is a 'send message type'
        if(command == self.c2 or command == self.c3):
# store senders name
            self.sender = self.client_store[socket]
# store senders address
            self.senderSocket = socket
        # print('Command is ', command)
        # print ('Message is ',parameter)

# save names to server
        if (command == self.c1):
            print("saving name to server...")
            self.client_store[socket] = parameter
            str = "client {} = {}"
            print(str.format(self.clientCount, self.client_store[socket]))

# message all clients connected
        elif (command == self.c2):
            print("sending message to all clients")
            for x in self.client_store:
                if(self.client_store[x] != self.sender):
                    x.send((b"MESSAGE FROM "+ self.sender.encode()+b"\n"))
                    x.send(parameter.encode())

# message one client specifiec
        elif (command == self.c3):
            self.errorCode = 1
            print("sending message to individual client")
# the message will be split with users iD then message after
            (user, sep, msg) = parameter.strip().partition(' ')
            for x in self.client_store:
                if (self.client_store[x] == user):
                    x.send((b"MESSAGE FROM "+ self.sender.encode()+b"\n"))
                    x.send(msg.encode())
                    self.errorCode = 0
# if user specified doesnt exist send sender clear error msg
            if(self.errorCode == 1):
                (self.senderSocket).send(b"ERROR - user "+ user.encode()+ b" does not exist please use LIST command to check who is connected \n")

# print all client names in a list
        elif (command == self.c4):
            print("printing list of clients...")
            str = "CLIENT :      {}"
            for x in self.client_store:
                string = str.format(self.client_store[x])
                socket.send(string.encode())

        elif (command == self.c5):
            print("closing connection for requested client")
            del self.client_store[socket]
            socket.close()
            return False

# else if the command is none of the above error has occured ask client to retry
        else:
            socket.send(b"ERROR\n - command does not exist please use one of the following commands... \n NAME <register your name> \n MSGALL <add msg here> \n MSGIND <USER> <add msg here> \n LIST \n CLOSE\n\n")

        return True

    def onDisconnect(self, socket):
        print("Client has disconnected")
        self.clientCount-=1
        print(self.txt.format(self.clientCount))

    def onStop(self):
        print("server has stopped")


#parse IP address and port you wish to listen to
ip = sys.argv[1]
port = int(sys.argv[2])

# Create my server.
server = MyServer()

# Start server
server.start(ip, port)
