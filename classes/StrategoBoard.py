import os
class StrategoBoard():
	def __init__(self):
		self.MapData = [[['N','N','N']for i in range(10)] for j in range(10)]
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
					#N stands for no one
					self.MapData[i][j] = ['N','N','N']


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
					#For testing purposes
					if data[line][col] == 'N':
						self.MapData[9-line][col] = (['N', data[line][col], 'N'])
					#Remove the above two lines. Unnecesary. 
					else:
						self.MapData[9-line][col] = (['Theirs', data[line][col], 'U'])


	

	def getPiece(self, x, y):
		return self.MapData[x][y][1]

	def getColor(self, x, y):
		return self.MapData[x][y][0]

	def isKnown(self,x,y):
		if self.MapData[x][y][2] == 'K': return True
		return False

	def isThere(self,x,y):
		if self.MapData[x][y] == ['N','N','N']: return False
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
	def getArmy(self, side):
		mine  = []
		for i in range(0, 10):
			for j in range (0, 10):
				if self.getColor(i, j) == side:
					mine.append([i,j])
		#Returns a list of locations for your pieces
		return mine

	#Returns if a piece can move or not
	def canMove(self, x, y):
		if self.getPiece(x, y) == 'B':
			return False
		if self.getPiece(x, y) == 'F':
			return False
		player = ''
		if self.getColor(x,y) =='Mine': player = 'Mine'
		else: player = 'Theirs'
		#Four directions. It doesn't matter if it's a 2 or not. If it's blocked in, it's blocked in
		possibleMoves = [[x+1, y], [x, y+1], [x-1, y], [x, y-1]]
		for i in possibleMoves:
			if i[0] >= 0 and i[0] < 10 and i[1] >= 0 and i[1] < 10:
				#If there's nothing there, it's possible to move there
				if self.isThere(i[0], i[1]) == False:
					return True
				#It's not a lake and it's not my piece
				if player == 'Theirs' and (self.getColor(i[0], i[1]) =='Mine'):
					return True

				if player == 'Mine' and (self.getColor(i[0], i[1]) =='Theirs'):
					return True
		return False

	#Returns all pieces in your army that can move
	def getMoving(self, side):
		army = self.getArmy(side)
		moving = []
		for i in army:
			if self.canMove(i[0], i[1]):
				moving.append(i)
		
		return moving

	#Returns a list of where a piece can move
	def moveWhere(self, x, y):
		if self.canMove(x, y) == False:
			return []
		possibleMoves = []
		#To distinguish between different players
		player = ''
		if self.getColor(x,y) =='Mine': player = 'Mine'
		else: player = 'Theirs'

		if self.getPiece(x, y) == '2':
			print(x, y)
			if x < 9:
				print('if 1 (2)\n')
				if player == 'Theirs' and (self.getColor(x+1, y) =='Mine' or self.getColor(x+1, y) == 'N'):
					too_far = False
					for i in range(x+1, 10):
						if self.getColor(i, y) != 'Theirs' and self.getColor(i,y) != 'L':
							if self.getColor(x-1, y) == 'Mine':
								too_far = True
							if(too_far):
								continue

							possibleMoves.append([i,y])
				elif player == 'Mine': 
					self.getColor(x+1, y)
					too_far = False
					for i in range(x+1, 10):
						print(i)
						if self.getColor(i, y) == 'Mine':
							break
						if self.getColor(i,y) == 'L':
							break
						if self.getColor(i, y) == 'Theirs':
							print(i, y)
							print("Break Theirs")
							possibleMoves.append([i, y])
							break
						print(self.getPiece(i, y))
						possibleMoves.append([i,y])				

			if x > 0:
				print('if 2 (2)\n')
				if player == 'Theirs' and (self.getColor(x-1, y) =='Mine' or self.getColor(x-1, y) == 'N'):
					too_far = False
					for i in range(x-1, -1, -1):
						if self.getColor(i, y) != 'Theirs' and self.getColor(i,y) != 'L':
							if self.getColor(i+1, y) == 'Mine':
								too_far = True
							if(too_far):
								continue
							possibleMoves.append([i,y])
				elif player == 'Mine':
					print(player)
					for i in range(x-1, -1, -1):
						print(i)
						if self.getColor(i, y) == 'Mine':
							break
						if self.getColor(i,y) == 'L':
							break
						if self.getColor(i, y) == 'Theirs':
							print(i, y)
							print("Break Theirs")
							possibleMoves.append([i, y])
							break
						print(self.getPiece(i, y))
						possibleMoves.append([i,y])
			if y < 9:
				print('if 3 (2)\n')
				if player == 'Theirs' and (self.getColor(x, y+1) =='Mine' or self.getColor(x, y+1) == 'N'):
					too_far = False
					for i in range(y+1, 10):
						if self.getColor(x, i) != 'Theirs' and self.getColor(x,i) != 'L':
							if self.getColor(x, i-1) == 'Theirs':
								too_far = True
							if(too_far):
								continue
							possibleMoves.append([x, i])

				elif player == 'Mine':
					for i in range(y+1, 10):
						if self.getColor(x, i) == 'Mine':
							break
						if self.getColor(x,i) == 'L':
							break
						if self.getColor(x, i) == 'Theirs':
							possibleMoves.append([x, i])
							break
						possibleMoves.append([x,i])
			if y > 0:
				print('if 4 (2)\n')
				if player == 'Theirs' and (self.getColor(x, y-1) =='Mine' or self.getColor(x, y-1) == 'N'):
					too_far = False
					for i in range(y-1, -1, -1):
						print(i)
						if self.getColor(x, i) == 'Theirs':
							break
						if self.getColor(x,i) == 'L':
							break
						if self.getColor(x, i+1) == 'Theirs':
							possibleMoves.append([x,i])
						possibleMoves.append([x,i])
				if player == 'Mine' and (self.getColor(x, y-1) == 'Theirs' or self.getColor(x, y-1) == 'N'):
					print(self.getColor(x, y-1))
					too_far = False
					for i in range(y-1, -1, -1):
						if self.getColor(x, i) == 'Mine':
							break
						if self.getColor(x,i) == 'L':
							break
						if self.getColor(x, i) == 'Theirs':
							possibleMoves.append([x, i])
							break
						possibleMoves.append([x,i])

		else:
			print(x, y)
			if x < 9:
				print('if 1\n')
				if player == 'Theirs' and (self.getColor(x+1, y) =='Mine' or self.getColor(x+1, y) == 'N'):
					possibleMoves.append([x+1, y])
				if player == 'Mine' and (self.getColor(x+1, y) == 'Theirs' or self.getColor(x+1, y) == 'N'):
					possibleMoves.append([x+1, y])

			if x > 0:
				print('if 2\n') 
				if player == 'Theirs' and (self.getColor(x-1, y) =='Mine' or self.getColor(x-1, y) == 'N'):
					possibleMoves.append([x-1, y])
				if player == 'Mine' and (self.getColor(x-1, y) == 'Theirs' or self.getColor(x-1, y) == 'N'):
					possibleMoves.append([x-1, y])

			if y < 9:
				print('if 3\n')
				if player == 'Theirs' and (self.getColor(x, y+1) =='Mine' or self.getColor(x, y+1) == 'N'):
					possibleMoves.append([x, y+1])
				if player == 'Mine' and (self.getColor(x, y+1) == 'Theirs' or self.getColor(x, y+1) == 'N'):
					possibleMoves.append([x, y+1])

			if y > 0:
				print('if 4\n')
				if player == 'Theirs' and (self.getColor(x, y+1) =='Mine' or self.getColor(x, y-1) == 'N'):
					possibleMoves.append([x, y-1])
				if player == 'Mine' and (self.getColor(x, y-1) == 'Theirs' or self.getColor(x, y-1) == 'N'):
					possibleMoves.append([x, y-1])

		return possibleMoves

	def printTensor(self):
		output = ""
		for i in range(0, 10):
			for j in range(0, 10):
				if self.getPiece(i, j) != 10:	
					#To make sure it lines up well
					output += "{:<10}".format(str(self.getPiece(i, j))+","+str(self.getColor(i,j))+" ")
				else:
					output += "{:<10}".format(str(self.getPiece(i, j))+","+str(self.getColor(i,j))+" ")

			output += '\n'
		return output

	def DidWin(self):
		flagCount = 0
		for i in range(0, 10):
			for j in range(0, 10):
				if self.getPiece(i, j) == 'F':
					flagCount += 1
					if i == 9 and j == 9:
						print("Tha99")
		if flagCount > 1:
			return False
		return True

	def WhoWon(self):
		for i in range(0, 10):
			for j in range(0, 10):
				if self.getPiece(i, j) == 'F':
					return self.getColor(i, j)


	#Should I make a print board function??

	#Maybe make a human interpretation??
		