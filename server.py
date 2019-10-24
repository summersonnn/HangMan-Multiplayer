from socket import *
import threading
myClients = []

class ThreadedServer():
	
	playerCount = 0
	currentPlayers = 0
	gameStart = False

	def game(self, client, addr):
		global myClients
		if self.gameStart:
			print("Game is starting...")
		else:
			print("Waiting for players...")
		while True:
			data = client.recv(1024)
			if not data:
				break
			for client in myClients:
				client.send(data)

	def sendAllClients(self, message):
		global myClients
		for client in myClients:
			client.send(message.encode())

	def listenToClient(self, client, addr):
		global myClients
	    
	        
		welcomeMessage = "Welcome. To register, press R. To login, press any key.\n"
		client.send(welcomeMessage.encode())
		message = client.recv(1024)
		message = message.decode()
		if 	message == "R" or message == "r":
			askusername = "Choose a username"
			client.send(askusername.encode())
			username = client.recv(1024)
			username = username.decode()
			askpassword = "Choose a password"
			client.send(askpassword.encode())
			password = client.recv(1024)
			password = password.decode()

			db = open("idpw.txt","a")
			db.write("\n" + username)
			db.write("#" + password + "\n")
			db.close()

		isValidUsername = False
		while (not isValidUsername):
			pleaseLogin = "Please type your username to login\n"
			client.send(pleaseLogin.encode())
			username = client.recv(1024)
			username = username.decode() + "#"

			openfile = open("idpw.txt", "r")
			for line in openfile:
				for part in line.split():
					if username in part:
						realpassword = part.partition("#")[2]
						username = part.partition("#")[0]
						isValidUsername = True
				
		while True:
			typePassword = "Please type your password\n"
			client.send(typePassword.encode())
			password = client.recv(1024)
			password = password.decode()

			if realpassword == password:
				self.currentPlayers = self.currentPlayers + 1
				welcomeMessage = "Welcome " + username + ". You logged in successfully."
				welcomeMessage = welcomeMessage + "\nThere are now " + str(self.currentPlayers) + " players on the server."
				welcomeMessage = welcomeMessage + "\nPlayerCount: " + str(self.playerCount) + "\n"
				client.send(welcomeMessage.encode())
				break

		if self.currentPlayers == self.playerCount:
			self.gameStart = True
		self.game(client, addr)
		
			
						

	def __init__(self,serverPort, playerCount):
		global myClients
		self.playerCount = playerCount

		try:
			serverSocket=socket(AF_INET,SOCK_STREAM)

		except:

		    print ("Socket cannot be created!!!")
		    exit(1)
            
		print ("Socket is created...")

		try:
		    serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
		except:

		    print ("Socket cannot be used!!!")
		    exit(1)

		print ("Socket is being used...")

		try:
		    serverSocket.bind((host,serverPort))
		except:

		    print ("Binding cannot de done!!!")
		    exit(1)

		print ("Binding is done...")

		try:
		    serverSocket.listen(playerCount)
		except:

		    print ("Server cannot listen!!!")
		    exit(1)

		print ("The server is ready to receive")


		while True:
			connectionSocket,addr=serverSocket.accept()
			myClients += [connectionSocket]
			threading.Thread(target=self.listenToClient, args = (connectionSocket,addr)).start()
            

if __name__=="__main__":
	serverPort=12000
	playerCount=int(input("How many players?"))
	host = ''
	ThreadedServer(serverPort, playerCount)
	
