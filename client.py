from socket import *
serverName="192.168.50.1"
serverPort=12000

try:
	clientSocket=socket(AF_INET,SOCK_STREAM)
except:
	print("Failed to connect!")

print("Socket created!")

clientSocket.connect((serverName,serverPort))
print("Socket connected using ip " + serverName)


while(True):
	message = clientSocket.recv(1024)
	message = message.decode()
	print(message)
	if (message[-1] == '?'):
		response=input()
		clientSocket.send(response.encode())

	
clientSocket.close()

