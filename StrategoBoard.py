
class StrategoBoard():
	def __init__(self):
		self.MapData = [10]
		#Going to be tuples, first color, second piece
	def setBoard(self):
		#Lakes are [4, 2] [4,3] [4,6] [4,7]
		#		   [5,2] [5,3] [5,6] [5,7] [row, column]
		#For each board space, it will be (color, piece, known). (L,L) in the case of lakes.
		#S = Spy, 1-10 (strings) = Numbers, B = Bomb, F = Flag
		#Get the coordinates of the lakes
		#First we initialize an empty board
		for i in range(0, 10):
			for j in range(0,10):
				if i == 4:
					#Is it a lake?
					if j == 2 or j == 3 or j == 6 or j == 7:
						self.MapData[i].append('L','L', 'L')
				elif i == 5:
					#It still could be a lake
					if j == 2 or j == 3 or j == 6 or j ==7:
						self.MapData[i].append('L','L', 'L')
				else:
					#It's not a lake
					self.MapData[i].append(['','',''])

	#Gets where your army is on the map
	def getArmy(self):
		mine  = []
		for i in range(0, len(self.MapData)):
			for j in range (0, len(self.MapData[i])):
				if self.MapData[i][j][0] == 'M':
					mine.append([i,j])
		#Returns a list of locations for your pieces
		return mine

	def getPiece(self, x, y):
		return self.MapData[x][y][1]

	def getColor(self, x, y):
		return self.MapData[x][y][0]

	def isKnown(self,x,y):
		if self.MapData[i][j][2] == 'K': return True
		return False

	def knownEnemy(self):
		theirs = []
		for i in range(0, len(self.MapData)):
			for j in range(0, len(self.MapData[i])):
				if isKnown[i][j]: #K is for known
					theirs.append(i,j)
		return theirs
		