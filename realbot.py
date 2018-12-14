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
		self.data = 'data\\output.txt'
		self.reward_place = 'data\\rewards.txt'

		self.side = ''
		self.Trainer = NeuralNet.Trainer() #Neural net shit

		self.numGames = 100



	def OnGameEnd(self):
		print ("Game Over")
		self.newGame = True
		self.gamesPlayed += 1

	def compute_reward(self):

		#If they lose a piece on the first turn, e.g. scouting, its fine
		#I may want to change this to the first few turns.
		if self.turn > 2:
			delta_pieces_known = abs(len(self.board.knownEnemy()) - len(self.board.totalEnemy()))
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
		return 0

	def readStdin(self):
		self.run()
		stdin.write('setup_map BoardSetup1 BoardSetup2o')
		stdin.flush()
		# line = stdin.readline()
		# while line:
		# 	readline = stdin.readline()
		# 	self.run()
		# 	for line in self.readStdin():
		# 		line = line.split()
		# 		stdout(line)
		# 		stdout.flush()

	def run(self):
		#print("Running")
		

		#print ("Start of while")

		try:
			#while(self.readStdin()):
			rawline = stdin.readline()
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
				if self.board.DidWin() == True:
					winner = self.board.WhoWon()
					self.gamesPlayed += 1
					self.turn = 0
					output = "The Winner is: {}\n".format(winner)
					stdout.write(output)
					stdout.flush()
					f = open(self.data, 'a+')
					f.write(output)
					f.close()



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
				stdin("Reward: " + str(self.reward) + "\n")
	
				f.write(write_str)
				f.close()
				f.open(self.output, 'a+')
				f.write(str(self.board.printTensor())+"\n")
				f.close()
				print("Open and closed \n")
				stdin.flush()
				write_str = str(self.reward)

				
				if self.gamesPlayed < self.numGames: 
					stdout.write('opponent_moves')
					stdout.flush()


				elif command == 'opponent_moves':
					#Train the fight network
					
					stdout.write('go')
					stdout.flush()


				elif command == "Game_Over":
					self.OnGameEnd()
					
				stdin.write('go')
				stdin.flush()
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

	def update_map(self, options):
		stdout.write("Updating a map\n")
		stdout.flush()
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
	#Bot().run()
	Bot().readStdin()
	stdout.write('setup_map BoardSetup1.txt BoardSetup2')
	stdout.flush()
	stdout.write('go')
	# def readStdin(self):
	# 	line = stdin.readline()
	# 	while line:
	# 		readline = stdin.readline()
			
	# 		for line in self.readStdin():
	# 			line = line.split()
	# 			stdout(line)
	# 			stdout.flush()













		


