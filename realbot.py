import sys
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
import io
from io import StringIO

#IF YOU CAN'T MOVE ANY PIECES, ITS ALSO A DRAW
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
		self.data = 'data\\output.txt'
		self.reward_place = 'data\\rewards.txt'
		self.reward = 0
		self.opponent_reward = 0
		self.side = ''
		self.Trainer = NeuralNet.Trainer() #Neural net shit
		self.OpponentTrainer = NeuralNet.Trainer()

		self.numGames = 2



	def OnGameEnd(self):
		print ("Game Over")
		self.newGame = True
		self.gamesPlayed += 1


	def onSessionEnd(self):
		print("Done")
		self.Trainer.saveTensor()
		self.OpponentTrainer.saveTensor()

	def compute_reward(self):

		#If they lose a piece on the first turn, e.g. scouting, its fine
		#I may want to change this to the first few turns.
		delta_amount = 0
		delta_pieces_known = 0

		if self.turn > 2:
			delta_pieces_known = abs(len(self.board.knownEnemy()) - len(self.board.totalEnemy()))
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
						#Need to implement winning game before this function
						elif self.board.getPiece(i, j) == 'F':
							delta_amount += 1000
						#DO Stuff with flag before calling this, or redirect to winnin/losing game
						 
						else:
							delta_amount = delta_amount + float(self.board.getPiece(i, j))

					elif self.board.getColor(i, j) == 'Theirs':
						if self.board.getPiece(i,j) == 'B':
							delta_amount -= 5
						elif self.board.getPiece(i, j) == 'S':
							delta_amount -= 8
						elif self.board.getPiece(i,j) == '3':
							delta_amount -= 5
						elif self.board.getPiece(i, j) == 'F':
							delta_amount -= 1000
						else: 
							delta_amount = delta_amount - float(self.board.getPiece(i, j))
		return delta_amount + (delta_pieces_known * 2.1)
		

	# def readStdin(self):
	# 	#self.run()
	# 	stdin.write('setup_map BoardSetup1 BoardSetup2o')
	# 	stdin.flush()
	# 	line = stdin.readline()
	# 	while line:
	# 		readline = stdin.readline()
	# 		self.run()
	# 		for line in self.readStdin():
	# 			line = line.split()
	# 			stdout(line)
	# 			stdout.flush()

	def run(self):
		#print("Running")
		

		print ("Start of while")
		while not sys.stdin.closed:
			if self.gamesPlayed > self.numGames:
				self.onSessionEnd()
				sys.exit()
			try:
				rawline = sys.stdin.readline()
				#End of file
				if len(rawline) == 0:
					return

				line = rawline.strip()

				if len(line) == 0:
					return

				parts = line.split()
				command = parts[0]

				if command == 'setup_map':
					self.setup_map(parts[1:])
				elif command == 'go':

					#If we won, then we want to reset. 
					if self.board.DidWin() == True:
						winner = self.board.WhoWon()
						self.gamesPlayed += 1
						self.turn = 0

						#Updating the reward
						if winner == 'Mine': 
							self.reward += 1000
							self.opponent_reward -= 1000 #Is this neccesary??
						else: 
							self.reward -= 1000
							self.opponent_reward += 1000

						#Some output
						output = "The Winner is: {}\n".format(winner)
						sys.stdout.write(output)
						sys.stdout.flush()
						f = open(self.data, 'a+')
						f.write(output)
						f.close()

						#Let's set the board up again
						self.setup_map(self.map)



					print("Turn: {} | Games Played: {}\n".format(math.ceil(self.turn), self.gamesPlayed))

					if self.turn == 0:
						self.Trainer.init_episode(self.board, self.gamesPlayed, self.turn)
						self.turn += 1
					elif self.turn != 0:
						self.turn += 1
					#Something over here????
					self.side = 'Mine' #In the opponent it will be 'Theirs'
					moves = self.Trainer.get_moves(self.turn, self.side)
					print("Moves: " + str(moves))
					self.side = 'Theirs'
					xBegin, yBegin = self.board.getMoving('Mine')[moves[0]]
					print("befor ")
					print("Moves: " + str(self.board.moveWhere(xBegin, yBegin)))
					print("end: "+ str(self.board.moveWhere(xBegin, yBegin)[moves[1]]))

					xend, yend = self.board.moveWhere(xBegin, yBegin)[moves[1]]
					print("Move Where?")

					#print (xBegin, yBegin, xend, yend)
					updatelst = [xBegin, yBegin, xend, yend]
					#a1 is in the getMoving array and the second is in the get
					print("Update: " + str(updatelst))
					output = self.update_map(updatelst)
					#stdout.write(output)
					#stdout.flush()
					
					self.reward = self.compute_reward()

					rewards = np.array([self.reward])
					print(rewards)
					if self.gamesPlayed == 0:
						self.Trainer.first_game(self.board, rewards)
					else:
						self.Trainer.trainReward(self.board, rewards, self.turn)
					f = open(self.reward_place, 'a+')
					sys.stdout.write("Reward: " + str(self.reward) + "\n" + str(self.board.DidWin()))

					write_str = str(self.reward)+"\n"
					f.write(write_str)
					f.close()
					f = open(self.data, 'a+')
					f.write(str(self.board.printTensor())+"\n")
					f.close()
					sys.stdin.flush()

					

					
					if self.gamesPlayed < self.numGames: 
						sys.stdout.write('opponent_moves')
						sys.stdout.flush()


					if command == 'opponent_moves':
						#Train the fight network
						
						oldstdin = stdin
						sys.stdin = io.StringIO('go')
						sys.stdin.flush()
						#print (raw_input('.'))


					elif command == "Game_Over":
						self.OnGameEnd()
						continue
					oldstdin = stdin
					#strip?
					sys.stdin = io.StringIO('go')
					sys.stdin.flush()
					#print (raw_input('.'))
					# else:
					# 	stderr.write('Unknown command: %s\n' % (command))
					# 	stderr.flush()


			except EOFError:
				print("EOFError")
				return
		print ("End of While")

	def setup_map(self, options):
		#Sets up the map, assuming the inputs are text files

		#The options will be my side and then their side		
		#for i in range (0, len(options)):
		self.board.ReadBoard('Mine', options[0])
		self.board.ReadBoard('Theirs', options[1])
		self.map = options

	def update_map(self, options):
		sys.stdout.write("Updating a map\n")
		sys.stdout.flush()
		#My moves
		#The options will be xstart, ystart, xend, yend
		PlaceManager.updateBoard(int(options[0]), int(options[1]), int(options[2]), int(options[3]), self.board)

		output = ("Games Played: {}\nTensod Data\n".format(self.gamesPlayed))
		output += self.board.printTensor()
		output += '\n'
		f = open(self.data, 'a+')
		f.write(output)
		f.close()
		print(output)
		return output

if __name__ == '__main__':
	#Remember to load (restore) the tensor
	game = Bot()
	game.run()
	#game.Trainer.saveTensor()
	#game.OpponentTrainer.saveTensor()













		


