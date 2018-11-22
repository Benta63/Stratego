from sys import stderr, stdin, stdout
from classes import StrategoBoard
from classes import ActionManager
from classes.ActionManager import PlaceManager 
from classes import helper
from math import fmod, pi
import math
import time
import numpy as np
import _thread
import NeuralNet
import os
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

		self.Trainer = NeuralNet.Trainer() #Neural net shit


	def OnGameEnd(self):
		print ("Game Over")
		self.newGame = True
		self.gamesPlayed += 1

	def compute_reward(self):

		#If they lose a piece on the first turn, e.g. scouting, its fine
		#I may want to change this to the first few turns.
		if self.turn > 2:
			delta_pieces_known = abs(self.board.knownEnemy() - len(self.board.totalEnemy()))
			delta_amount = 0
			for i in range(0, 10):
				for j in range(0, 10):
					#Subtract my pieces from theirs. 
					if self.board.getColor(i, j) == "Mine":
						#What if it's a bomb, or a spy? Also, miners are pretty important
						if self.board.getPiece(i, j) == 'B':
							delta_amount += 5
						elif self.board.getPiece(i, j) == 'S':
							delta_amount += 8 #Let's try to protec the spy a bit
						elif self.board.getPiece(i, j) == '3':
							delta_amount += 5
						#Flag or not? 
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
		print("Running")
		while not stdin.closed:
			print ("Start of while")
			try:
				rawline = stdin.readline()
				#End of file
				if len(rawline) == 0:
					break

				line = rawline.strip()

				if len(line) == 0:
					continue

				parts = line.split()
				command = parts[0]

				if command == 'setup_map':
					self.setup_map(parts[1:])
				elif command == 'go':
					print("Turn: {} | Games Played: {}\n".format(math.ceil(self.turn), self.gamesPlayed))

					if self.turn == 0:
						self.Trainer.init_episode(self.board, self.gamesPlayed, self.turn)
						self.turn += 1
					elif self.turn != 0:
						self.turn += 1
					#Something over here????
					
					moves = self.Trainer.get_moves(self.turn)
					output = self.update_map(moves)
					stdout.write(output)
					stdout.flush()
					
					self.reward = self.compute_reward()
					rewards = np.array([self.reward])

					if self.gamesPlayed == 0:
						self.Trainer.first_game(self.board, rewards)
					else:
						self.Trainer.trainReward(self.board, rewards, self.turn)

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
			print ("End of While")

	def setup_map(self, options):
		#Sets up the map, assuming the inputs are text files

		#The options will be my side and then their side		for i in range (0, len(options)):
		self.board.ReadBoard('Mine', options[0])
		self.board.ReadBoard('Theirs', options[1])
		print(self.board.MapData)

	def update_map(self, options):
		#My moves
		#The options will be xstart, ystart, xend, yend
		PlaceManager.updateBoard(int(options[0]), int(options[1]), int(options[2]), int(options[3]), self.board)

		output = ("Games Played: {}\nTensod Data\n".format(self.gamesPlayed))
		output += self.board.printTensor()
		output += '\n'
		f = open('data\\output.txt', 'a+')
		f.write(output)
		f.close()

if __name__ == '__main__':
	Bot().run()










		


