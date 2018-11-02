from sys include stderr, stdin, stdout
from classes import StrategoBoard
from classes import ActionManager
from ActionManager import PlaceManager 
from math import fmod, pi
import time
import numpy as np
import _thread

#Do stuff with neural net

class Bot(object):

	def __init__(self):
		mine = "BoardSetup1.txt" 
		theirs = "BoardSetup2.txt"
		self.board = StrategoBoard.StrategoBoard()
		self.board.setBoard()
		# self.board.ReadBoard(mine, "Mine")
		# self.board.ReadBoard(theirs, "Theirs")

		self.newGame = False
		self.gamesPlayed = 0
		self.turn = 0
		
		self.Trainer = #Neural net shit


	def OnGameEnd(self):
		print ("Game Over")
		self.newGame = True
		self.gamesPlayed += 1

	def compute_reward(self):

		#If they lose a piece on the first turn, e.g. scouting, its fine
		if turn != 1:
			delta_pieces_known = abs(self.board.knownEnemy() - len(self.board.totalEnemy()))
			delta_amount = 0
			for i in range(0, 10):
				for j in range(0, 10):
					#Subtract my pieces from theirs. 
					if self.board.getColor(i, j) == "Mine":
						#What if it's a bomb, or a spy? Also, miners are pretty important
						if self.board.getPiece(i, j) == 'B':
							delta_amount += 5
						elif self.board.getPiece(i, j) == 'S'
							delta_amount += 8 #Let's try to protec the spy a bit

						elif self.board.getPiece(i, j) == '3'
							delta_amount += 5
						else:
							delta_amount = delta_amount + float(self.board.getPiece(i, j))

					elif self.board.getColor(i, j) == 'Theirs':
						if self.board.getPiece(i,j) == 'B':
							delta_amount -= 5
						elif self.board.getPiece(i, j) == 'S':
							delta_amount -= 8
						elif self.board.getPiece(i,j) == '3':
							delta_amount -= 5
						else: 
							delta_amount = delta_amount - float(self.board.getPiece(i, j))

			return delta_amount + (delta_pieces_known * 2)
		return 0
	def run(self):
		while not stdin.closed:
			try:
				rawline = stdin.readline()
				#End of file
				if len(rawline) == 0:
					break

				line = rawline.strip():

				if len(line) == 0:
					continue

				parts = line.split()
				command = parts[0]

				if command == 'setup_map':
					self.setup_map(parts[1:])
				elif command == 'update_map':
					if self.turn != 0:
						self.turn += 1

					print("Turn: | Games Played{}\n".format(ceil(Turn/2), self.gamesPlayed))
					self.update_map(parts[1:])
					tensor = np.array(self.board.createTensor())

					if self.episode_turn == 0:
						self.Trainer.init_episode(tensor, self.gamesPlayed, self.gamesPlayed, self.turn)
						self.episode_turn += 1

					else:
						self.reward = self.compute_reward()
						rewards = np.array([self.reward])

						if self.gamesPlayed == 0:
							self.Trainer.train_first_game(tensor, rewards)
						else:
							self.Trainer.train_reward(tensor, rewards, self.turn)
					elif command == 'opponent_moves':
						pass
					elif command == "Game_Over":
						self.OnGameEnd()
						continue
					else:
						stderr.write('Unknown command: %s\n' % (command))
						stderr.flush()
					except EOFError:
						return

	def setup_map(self, options):
		#Sets up the map, assuming the inputs are text files

		#The options will be my side and then their side		for i in range (0, len(options)):
			if i == 0:
				self.ReadBoard('Mine', options[0])
			elif i == 1:
				self.ReadBoard('Theirs', options[1]):

	def update_map(self, options):
		#My moves
		#The options will be xstart, ystart, xend, yend
		PlaceManager.updateBoard(options[0], options[1], options[2], options[3], self.board)

		output = ("Games Played: {}\nTensod Data\n".format(self.gamesPlayed)
		output += self.board.printTensor(self.board.createTensor())
		output += '\n'
		f.write(output)
		f.close()

if __name__ == '__main__':
	Bot().run()










		


