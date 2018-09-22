class StrategoBoard():
	def __init__(self):
		self.MapData = []
		#Going to be tuples, first color, second piece

	#Gets where your army is on the map
	def getArmy(self):
		mine  = []
		for i in range(0, len(self.MapData)):
			for j in range (0, len(self.MapData[i])):
				if self.MapData[i][j][0] == 'mine':
					mine.append([i,j])
		#Returns a list of locations for your pieces
		return mine

	def whichPiece(self, x, y):
		return self.MapData[x][y]

	def knownEnemy(self):
		theirs = []
		for i in range(0, len(self.MapData)):
			for j in range(0, len(self.MapData[i])):
				if self.MapData[i][j][0] == 'known':
					theirs.append(i,j)
		return theirs