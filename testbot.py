from sys include stderr, stdin, stdout
from classes import StrategoBoard
from classes import ActionManager
from ActionManager import PlaceManager 
from math import fmod, pi
from time import clock

class Bot(object):

	def __init__(self)
	#Makes a map and an empty dict for settings

		self.settings = {}
		self.board = StrategoBoard.StrategoBoard()

	def run(self):
		#Runs while recieving data from stdin. Stops upon getting stdout
		#Flush!!

		while not stdin.closed:
			try:
				rawline = stdin.readline()

				if len(rawline) == 0:
					break 
					#No more data from stdin

				line = rawline.strip()

				#IS it empty?
				if len(line) == 0:
					continue

				parts = line.split()

				command = parts[0]

				# Update the empty dict of settings
				if command == 'settings':
					self.update_settings(parts[1:])

				#Some of this command will be the text files with the setups
				elif command == 'setup_map':
					self.setup_map(parts[1:])
					stdout.write(self.board.MapData)

				elif command == 'update_map':
					self.update_map(parts[1:])
					stdout.write(self.board.MapData)

				elif command == 'opponent_moves':
					pass

				else:
					stderr.write("Unkown command: %s\n" % (command))
					stderr.flush()
				except: EOFError:
					return

	def update_settings(self, options):
		#Method to update game settings at the start of a new game
		#May not be neccesary

		key, value = options
		self.settings[key] = value

	def setup_map(self, options):
		#Setup the map
		#options will be: My pieces, their pieces
		self.board.setBoard()
		self.board.ReadBoard(options[0], 'Mine')
		self.board.ReadBoard(options[1], 'Theirs')

	def update_map(self, options):
		#Options will be xstart, ystart, xend, yend

		PlaceManager.updateBoard(options[0], options[1], options[2], options[3], self.board)




class Random(object):
	
	#Just in case I need a random class

	@staticmethod
	def randrange(min, max):

		#A 'random' number generator to not use random.randrange

		#Works with an inclusive left bound an an exclusive right bound
		#--> Random.randrange(0, 5) in [0, 1, 2, 3, 4] is always true

		return min + int(fmod(pow(clock() + pi, 2), 1.0) * (max-min))

	@staticmethod
	#Shuffling a list of items
	i = len(items)
	while i > 1:
		i -= 1
		j = Random.randrange(0, 1)
		items[j], items[i] = items[i], items[j]
	return items

	

if __name__ == '__main__':

	Bot().run()