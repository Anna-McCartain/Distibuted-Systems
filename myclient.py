"""

IRC client exemplar.

"""

import sys
from ex2utils import Client

import time


class IRCClient(Client):

	def onMessage(self, socket, message):
		print(message)
		return True


# Parse the IP address and port you wish to connect to.
ip = sys.argv[1]
port = int(sys.argv[2])
screenName = sys.argv[3]

# Create an IRC client.
client = IRCClient()

# Start server
client.start(ip, port)

# *** register your client here, e.g. ***
message="NAME "+screenName
client.send(message.encode())
print("Welcome " + screenName)

while client.isRunning():
	try:
		command = input("> ").strip()
		client.send(command.encode())

	except:
		client.stop();

client.stop()
