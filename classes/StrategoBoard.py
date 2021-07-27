# Defines the board of a stratego game
import os
class StrategoBoard():
	def __init__(self):
		self.MapData = [[['N','N','N']for i in range(10)] for j in range(10)]
		self.setBoard()
		#I may do something with this later. Idk
		self.attack_threshold = 0.0

		'''For each board space, it will be (color, piece, known). (L,L,L) in the 
		case of lakes.
		S = Spy, 1-10 (strings) = Numbers, B = Bomb, F = Flag
		Color is 'Mine' or 'Theirs'
		Known is True of False
		We automatically know our own pieces
		Get the coordinates of the lakes
		First we initialize an empty board'''
	
	def setBoard(self):
		'''Makes a blank board (with lakes)'''
		# Lakes are [4,2] [4,3] [4,6] [4,7]
		#		    [5,2] [5,3] [5,6] [5,7] 

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


	def ReadBoard(self, side, text):
		'''Reads in the board setup from a text file. Side is Mine or Theirs and
			is used to denote the Known Boolean. Also, which side of the board
			they are setup on.
		'''

		# First, we organize the file
		f = open(text)
		lines = f.readlines()
		data = [line.split() for line in lines]

		# Which pieces are we reading in?
		if side == "Mine":
			for line in range(0, len(data)):
				for col in range(0, 10):
					self.MapData[line][col] = (['Mine', data[line][col], 'K'])
		else:
			# First of all, their pieces are on the other side, so the first line 
			# is actually the tenth
			# So, 0 is 9, 1 is 8, 3 is 7
			for line in range(0, len(data)):
				for col in range(0, 10):
					#For testing purposes
					if data[line][col] == 'N':
						self.MapData[9-line][col] = (['N', data[line][col], 'N'])
					#Remove the above two lines. Unnecesary. 
					else:
						self.MapData[9-line][col] = (['Theirs', data[line][col], 'U'])
	
	#Accessors

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

	#To make lists of stuff for the Neural Net

	def knownEnemy(self):
		'''Returns a list of all known enemies' locations'''
		theirs = []
		for i in range(0, len(self.MapData)):
			for j in range(0, len(self.MapData[i])):
				if self.isKnown(i,j) and self.getColor(i,j) == "Theirs": #K is for known
					theirs.append([i,j])
		return theirs

	def totalEnemy(self):
		'''Returns a list of all the enemies' locations'''
		theirs = []
		for i in range(0, len(self.MapData)):
			for j in range(0, len(self.MapData[i])):
				theirs.append([i, j])
		return theirs

	def getFull(self, x, y):
		'''Returns the full board including how its populated.'''
		return self.MapData[x][y]

	def getArmy(self, side):
		'''Returns a list of locations for your pieces'''
		mine  = []
		for i in range(0, 10):
			for j in range (0, 10):
				if self.getColor(i, j) == side:
					mine.append([i,j])	
		return mine

	
	def canMove(self, x, y):
		'''Given a coordinate, returns if a piece can move or not in ANY direction
		 (Boolean)
		'''

		# Piece doesn't exist
		if self.getPiece(x, y) == 'N':
			return False

		# Bombs and flags can't move
		if self.getPiece(x, y) == 'B':
			return False
		if self.getPiece(x, y) == 'F':
			return False


		player = ''
		if self.getColor(x,y) =='Mine': player = 'Mine'
		else: player = 'Theirs'
		#Four directions. Check if its blocked in.
		possibleMoves = [[x+1, y], [x, y+1], [x-1, y], [x, y-1]]
		for i in possibleMoves:
			# Are we against a wall?
			if i[0] >= 0 and i[0] < 10 and i[1] >= 0 and i[1] < 10:
				#If there's nothing there, it's possible to move there
				if self.isThere(i[0], i[1]) == False:
					return True
				
				# You can take your opponent's piece. 
				if player == 'Theirs' and (self.getColor(i[0], i[1]) =='Mine'):
					return True

				if player == 'Mine' and (self.getColor(i[0], i[1]) =='Theirs'):
					return True
		return False

	def getMoving(self, side):
		'''Returns a list of all the pieces in your army (side) that can move.'''
		army = self.getArmy(side)
		moving = []
		for i in army:
			if self.canMove(i[0], i[1]):
				moving.append(i)
		
		return moving

	#Returns a list of where a piece can move
	def moveWhere(self, x, y):
		'''Returns a list of where a specific piece (denoted by x,y coords) can 
			move.
		'''

		if getPiece(x,y) == 'N':
			# There's no piece here
			return False
		if self.canMove(x, y) == False:
			return []
		possibleMoves = []
		#To distinguish between different players
		player = ''
		if self.getColor(x,y) =='Mine': player = 'Mine'
		else: player = 'Theirs'

		if self.getPiece(x, y) == '2':
			# 2s can move as far as they want in one direction. (Not diagonal!)
			# print(x, y)

			# We have four directions to check.

			# Right
			if x < 9:
				# We can go further right (If there's no pieces there)
				for space in range(x, 10):
					if getPiece(space, y) == 'N':
						possibleMoves.append([space, y])
					elif getPiece(space, y) == 'Theirs' and player == 'Mine':
						possibleMoves.append([space, y])
						# We stop here as there's a piece and we have to reveal
						break
					elif getPiece(space, y) == 'Mine' and player == 'Theirs':
						possibleMoves.append([space, y])
						# We stop here as there's a piece and we have to reveal
						break
			# Left
			if x > 0:
				# We can go further left (If there are no pieces there)
				for space in range(x, 0, -1):
					if getPiece(space, y) == 'N':
						possibleMoves.append([space, y])
					elif getPiece(space, y) == 'Theirs' and player == 'Mine':
						possibleMoves.append([space, y])
						# We stop here as there's a piece and we have to reveal
						break
					elif getPiece(space, y) == 'Mine' and player == 'Theirs':
						possibleMoves.append([space, y])
						# We stop here as there's a piece and we have to reveal
						break
			# Up
			if y < 9:
				for space in range(y, 10):
					if getPiece(x, space) == 'N':
						possibleMoves.append([x, space])
					elif getPiece(x, space) == 'Theirs' and player == 'Mine':
						possibleMoves.append([x, space])
						# We stop here as there's a piece and we have to reveal
						break
					elif getPiece(x, space) == 'Mine' and player == 'Theirs':
						possibleMoves.append([x, space])
						# We stop here as there's a piece and we have to reveal
						break

			# Down
			if y > 0:
				for space in range(y, 0, -1):
					if getPiece(x, space) == 'N':
						possibleMoves.append([x, space])
					elif getPiece(x, space) == 'Theirs' and player == 'Mine':
						possibleMoves.append([x, space])
						# We stop here as there's a piece and we have to reveal
						break
					elif getPiece(x, space) == 'Mine' and player == 'Theirs':
						possibleMoves.append([x, space])
						# We stop here as there's a piece and we have to reveal
						break

		else: #canMove already checks for bombs and flags
			if x < 9:
				if self.piece(x+1, y) == 'N':
				 	possibleMoves.append([x+1, y])
				if player == 'Theirs' and self.getColor(x+1, y) == 'Mine':
				 	possibleMoves.append([x+1], y)
				if player == 'Mine' and self.getColor(x+1, y) == 'Theirs':
					possibleMoves.append([x+1, y])

			if x > 0:
				if self.piece(x-1, y) == 'N':
				 	possibleMoves.append([x-1, y])
				if player == 'Theirs' and self.getColor(x-1, y) =='Mine':
					possibleMoves.append([x-1, y])
				if player == 'Mine' and self.getColor(x-1, y) == 'Theirs':
					possibleMoves.append([x-1, y])

			if y < 9:
				if self.piece(x, y+1) == 'N':
				 	possibleMoves.append([x, y+1])
				if player == 'Theirs' and self.getColor(x, y+1) =='Mine':
					possibleMoves.append([x, y+1])
				if player == 'Mine' and self.getColor(x, y+1) == 'Theirs':
					possibleMoves.append([x, y+1])

			if y > 0:
				if self.piece(x, y-1) == 'N':
				 	possibleMoves.append([x, y-1])
				if player == 'Theirs' and self.getColor(x, y+1) =='Mine':
					possibleMoves.append([x, y-1])
				if player == 'Mine' and self.getColor(x, y-1) == 'Theirs':
					possibleMoves.append([x, y-1])

		return possibleMoves

	# Prints the whole board (In the form of the [piece, side])
	def printTensor(self):
		output = ""
		for i in range(0, 10):
			for j in range(0, 10):
				# if self.getPiece(i, j) != 10:	
					#To make sure it lines up well
				output += "{:<10}".format(str(self.getPiece(i, j))+","+str(self.getColor(i,j))+" ")
				# else:
				# 	output += "{:<10}".format(str(self.getPiece(i, j))+","+str(self.getColor(i,j))+" ")
			output += '\n'
		return output

	#Returns if anyone won
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

	#Returns who won by scanning the board for the flag that is still standing
	#DO NOT CALL THIS IF FUNCTION DidWin RETURNS FALSE!!!
	def WhoWon(self):
		assert(self.DidWin() == True)
		for i in range(0, 10):
			for j in range(0, 10):
				if self.getPiece(i, j) == 'F':
					return self.getColor(i, j)

	#memorized is a boolean toggling if the player has to keep track of all of the opponents pieces
	def PrintMySide(self, side, memorized):
		output = ""

		for x in range(0,10):
			for y in range(0, 10):
				if self.getColor(x, y) == side:
					output += "{:<10}".format(str(self.getPiece(x,y))+","+str(self.getColor(x,y))+" ")
				elif self.getColor(x,y) != side and memorized == True:
					output += "{:<10}".format(str(self.getPiece(x,y))+","+str(self.getColor(x,y))+" ")
				elif self.getColor(x,y) != side and memorized == False:
					output += "{:<10}".format(str(self.getColor(x,y)) + " ")
				else:
					output += "{:<10}".format(str(self.getPiece(x,y)+",")+str(self.getColor(x,y))+" ")
			output += '\n'
		return output



		