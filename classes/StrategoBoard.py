import os
class StrategoBoard():
	def __init__(self):
		self.MapData = [[['','','']for i in range(10)] for j in range(10)]
		self.setBoard()
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
	def ReadBoard(self,text, side):
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


	#Gets where your army is on the map
	def getArmy(self):
		mine  = []
		for i in range(0, len(self.MapData)):
			for j in range (0, len(self.MapData[i])):
				if self.MapData[i][j][0] == 'Mine':
					mine.append([i,j])
		#Returns a list of locations for your pieces
		return mine

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

	def knownEnemy(self):
		theirs = []
		for i in range(0, len(self.MapData)):
			for j in range(0, len(self.MapData[i])):
				if self.isKnown(i,j) and self.getColor(i,j) == "Theirs": #K is for known
					theirs.append([i,j])
		return theirs
		