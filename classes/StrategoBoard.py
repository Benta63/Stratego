import os
class StrategoBoard():
	def __init__(self):
		self.MapData = [[['','','']for i in range(10)] for j in range(10)]
		self.setBoard()
		#I may do something with this later. Idk
		self.attack_threshold = 0.0
		#Going to be tuples, first color, second piece
	
	#Makes a blank board
	#Call this first before anything else
	def setBoard(self):
		#Lakes are [4, 2] [4,3] [4,6] [4,7]
		#		   [5,2] [5,3] [5,6] [5,7] [row, column]
		#For each board space, it will be (color, piece, known). (L,L,L) in the case of lakes.
		#S = Spy, 1-10 (strings) = Numbers, B = Bomb, F = Flag
		#Color is 'Mine' or 'Theirs'
		#Get the coordinates of the lakes
		#First we initialize an empty board
		for i in range(0, 10):
			for j in range(0,10):
				if i == 4:
					#Is it a lake?
					if j == 2 or j == 3 or j == 6 or j == 7:
						self.MapData[i][j] =['L','L', 'L']
				elif i == 5:
					#It still could be a lake
					if j == 2 or j == 3 or j == 6 or j ==7:
						self.MapData[i][j] = ['L','L', 'L']
				else:
					#It's not a lake
					self.MapData[i][j] = ['','','']


	#Reads in the board setup from a text file
	def ReadBoard(self, side, text):
		#First, we organize the file
		f = open(text)
		lines = f.readlines()
		data = [line.split() for line in lines]

		#Which pieces are we reading in?
		if side == "Mine":
			for line in range(0, len(data)):
				for col in range(0, 10):
					self.MapData[line][col] = (['Mine', data[line][col], 'K'])
		else:
			#First of all, their pieces are on the other side, so the first line is actually the tenth
			#So, 0 is 9, 1 is 8, 3 is 7
			for line in range(0, len(data)):
				for col in range(0, 10):
					self.MapData[9-line][col] = (['Theirs', data[line][col], 'U'])

	

	def getPiece(self, x, y):
		return self.MapData[x][y][1]

	def getColor(self, x, y):
		return self.MapData[x][y][0]

	def isKnown(self,x,y):
		if self.MapData[x][y][2] == 'K': return True
		return False

	def isThere(self,x,y):
		if self.MapData[x][y] == ['','','']: return False
		return True

	#To make lists of stuff


	def knownEnemy(self):
		theirs = []
		for i in range(0, len(self.MapData)):
			for j in range(0, len(self.MapData[i])):
				if self.isKnown(i,j) and self.getColor(i,j) == "Theirs": #K is for known
					theirs.append([i,j])
		return theirs

	def totalEnemy(self):
		theirs = []
		for i in range(0, len(self.MapData)):
			for j in range(0, len(self.MapData[i])):
				theirs.append([i, j])
		return theirs

	#Returns the full tuple behind the list
	def getFull(self, x, y):
		return self.MapData[x][y]

	#Gets where your army is on the map
	def getArmy(self):
		mine  = []
		for i in range(0, len(self.MapData)):
			for j in range (0, len(self.MapData[i])):
				if self.MapData[i][j][0] == 'Mine':
					mine.append([i,j])
		#Returns a list of locations for your pieces
		return mine

	#Returns if a piece can move or not
	def canMove(self, x, y):
		if self.getPiece(x, y) == 'B':
			return False
		if self.getPiece(x, y) == 'F':
			return False
		#Four directions. It doesn't matter if it's a 2 or not. If it's blocked in, it's blocked in
		possibleMoves = [[x+1, y], [x, y+1], [x-1, y], [x, y-1]]
		for i in possibleMoves:
			if i[0] >= 0 and i[0] < 10 and i[1] >= 0 and i[1] < 10:
				if self.isThere(i[0], i[1]) == False:
					return True
				if self.getColor(i[0], i[1]) != 'L' and self.getColor(i[0], i[1]) != self.getColor(x, y):
					return True
		return False

	#Returns all pieces in your army that can move
	def getMoving(self):
		army = self.getArmy()
		moving = []
		for i in army:
			if self.canMove(i[0], i[1]):
				moving.append(i)
		return moving

	#Returns a list of where a piece can move
	def moveWhere(self, x, y):
		print("PLACEHOLDER")
		if canMove(x, y) == False:
			return []
		if self.getPiece(x, y) == '2':
			possibleMoves = [[i, y] for i in range(0, 10)]
			possibleMoves += [[x, i] for i in range(0, 10)]
			for move in possibleMoves:
				if self.getColor(move[0], move[1]) != self.getColor(x, y) and self.getColor(move[0], move[1]) != 'L':
					possibleMoves.remove(move)
			return possibleMoves
		else:
			possibleMoves = [[x+1, y], [x, y+1], [x-1, y], [x, y-1]]
			for move in possibleMoves:
				if self.getColor(move[0], move[1]) != self.getColor(x, y) and self.getColor(move[0], move[1]) != 'L':
					possibleMoves.remove(move)
			return possibleMoves

	def printTensor(self):
		output = ""
		for i in range(0, 10):
			for j in range(0, 10):
				output += str(self.getPiece(i, j))+","+str(self.getColor(i,j))+" "
			output += '\n'
		return output



			

		return inputTensor


	#Should I make a print board function??

	#Maybe make a human interpretation??
		