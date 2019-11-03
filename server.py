from socket import *
import threading
import random
myClients = []
users = []
wrongGuesses = []
wrongPhrases = []

class ThreadedServer():
	allowedAttempt = 7
	playerCount = 0
	currentPlayers = 0
	gameStart = False

	def game(self, client, addr):
		global users
		global myClients
		global wrongGuesses
		global wrongPhrases

		if self.gameStart:
			word = random.choice(open("words.txt").readlines())
			word = word[:-1]
			word = word.lower()
			secretWord = "_|" * len(word)
			secretWord = secretWord[:-1]
			info = "Game is starting...\nPlayer orders: "
			for name in users:
				info = info + name + "---"
			for clientx in myClients:
				clientx.send(info.encode())

		else:
			info = "Waiting for players..."
			for clientx in myClients:
				clientx.send(info.encode())
			
		counter = 0
		while self.gameStart:
			found = False
			currentUser = str(users[counter % self.currentPlayers])
			info = "\n" + "Current word: " + secretWord + "\n" + currentUser + " is about to play...\nRemaining lives: " + str(self.allowedAttempt)
			info = info + "\nWrong LetterGuesses: " + str(wrongGuesses) + "\nWrong Phrase Guesses: " + str(wrongPhrases)
			
			self.sendAllClientsExceptSender(None, info)

			privateMessage = "\nPlease make a guess for phrase or a letter?"
			privateTaker = myClients[counter % self.playerCount]
			privateTaker.send(privateMessage.encode())
			guess = privateTaker.recv(1024)
			guess = guess.decode()
			guess = guess.lower()
			
			if guess == word:
				secretWord = word
				print ("\nEnd")
			elif len(guess) > 1 or not guess:
				wrongPhrases += [guess]
				self.allowedAttempt -= 1
			elif len(guess) == 1:
				for pos, char in enumerate(word):
					if char == guess:
						found = True
						tempList = list(secretWord)
						tempList[pos*2] = word[pos]
						secretWord = ''.join(tempList)
				if found == False and guess not in wrongGuesses:
					wrongGuesses += guess
					self.allowedAttempt -= 1
			

			if self.allowedAttempt == 0:
				info = "\nYOU HUNG THE MAN!!! Word was: " + word
				self.sendAllClientsExceptSender(None, info)	
				break	
			elif secretWord.find("_") == -1:
				info = "\nGame is finished. \nWord: " + word + "\nWinner: " + currentUser
				self.sendAllClientsExceptSender(None, info)
				break
			counter += 1

		if self.gameStart == True:
			self.gameStart = False
			wrongGuesses = []
			wrongPhrases = []
			self.allowedAttempt = 7
			self.playAgain(client,addr)

		

	def playAgain(self, client, addr):
		global myClients
		global users 
		counter = 0

		temp = self.currentPlayers
		self.currentPlayers = 0
		
		while True:
			if counter == temp:
				break

			privateMessage = "\nContinue? Y OR N?"
			privateTaker = myClients[counter % temp]
			privateTaker.send(privateMessage.encode())
			answer = privateTaker.recv(1024)
			answer = answer.decode()
			print ("\nMyclients: \n" + str(myClients))

			print(answer)
			if answer == "Y" or answer == "y":
				self.currentPlayers += 1
				if self.currentPlayers == self.playerCount:
					self.gameStart = True

				print (self.currentPlayers)
				self.game(client,addr)
			else:
				privateMessage = "\nBye!"
				privateTaker.send(privateMessage.encode())
				users.remove(users[myClients.index(privateTaker)])
				myClients.remove(privateTaker)
				counter -= 1
				temp -= 1
			counter += 1

		
	def sendAllClientsExceptSender(self, client, message):
		tempClients = myClients.copy()
		if client != None:
			tempClients.remove(client)
		for clientx in tempClients:
			clientx.send(message.encode())

	def listenToClient(self, client, addr):
		global myClients
		global users
	 
		welcomeMessage = "\nWelcome. To register, press R. To login, press any key?"
		client.send(welcomeMessage.encode())
		message = client.recv(1024)
		message = message.decode()
		if 	message == "R" or message == "r":
			askusername = "Choose a username?"
			client.send(askusername.encode())
			username = client.recv(1024)
			username = username.decode()
			askpassword = "Choose a password?"
			client.send(askpassword.encode())
			password = client.recv(1024)
			password = password.decode()

			db = open("idpw.txt","a")
			db.write("\n" + username)
			db.write("#" + password + "\n")
			db.close()

		isValidUsername = False
		while (not isValidUsername):
			pleaseLogin = "\nPlease type your username to login?"
			client.send(pleaseLogin.encode())
			username = client.recv(1024)
			username = username.decode()

			openfile = open("idpw.txt", "r")
			for line in openfile:
				realusername = line.partition("#")[0]
				if username == realusername:
					isValidUsername = True
					realpassword = line.partition("#")[2]
					realpassword = realpassword[:-1]
				
		while True:
			typePassword = "\nPlease type your password?"
			client.send(typePassword.encode())
			password = client.recv(1024)
			password = password.decode()

			if realpassword == password:
				self.currentPlayers = self.currentPlayers + 1
				welcomeMessage = "\nWelcome " + username + ". You logged in successfully."
				welcomeMessage = welcomeMessage + "\nThere are now " + str(self.currentPlayers) + " players on the server."
				welcomeMessage = welcomeMessage + "\nPlayerCount: " + str(self.playerCount)
				client.send(welcomeMessage.encode())
				users += [username]
				break

		if self.currentPlayers == self.playerCount:
			self.gameStart = True
		self.game(client, addr)
		
			
						

	def __init__(self,serverPort, playerCount):
		global myClients
		global users
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
	
