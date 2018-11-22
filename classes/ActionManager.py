import sys
from . import StrategoBoard

class PlaceManager(object):
	#board is a StrategoBoard object


	def islegal(xstart, ystart, xend, yend, board):
		#Can't move into a lake
		if board.getPiece(xend, yend) == 'L':
			return False
		#Did they even move?
		if xstart == xend and ystart == yend:
			return False
		piece = board.getPiece(xstart, ystart)
		#You can't attack your own pieces
		if board.getColor(xstart,ystart) == board.getColor(xend,yend):
			return False
		#The bomb and flag can't move
		if piece == 'F' or piece == 'B':
			return False
		if piece != '2':
			#If we move more than one spot it's illegal
			if abs(xstart-xend) > 1 or abs(ystart-yend) > 1:
				return False
		#Diagonal is a no go
		if abs(xstart-xend) > 0 and abs(ystart-yend) > 0:
			return False
		#A two can't move through pieces if it is moving multiple spaces
		if piece == '2':
			if abs(xstart-xend) > 0:
				#We go through this row
				i = xstart + 1
				#+1 because we don't want to run into ourselves
				while i != xend:
					i = i + 1
					if board.getPiece(i, ystart) != '':
						return False

			elif abs (ystart-yend) > 0:
				i = ystart + 1
				while i != yend:
					i = i + 1
					if board.getPiece(i, xstart) != '':
						return False
		
		##ADD MORE ILLEGAL MOVES HERE
							
		return True

	#An error function for debugging
	def ErrorFunction(type):
		print("Error: {:s}".format(type))
		#Taking out exit for testing purposes
		#sys.exit()
	
	#For initial placing of troops on the board	
	def placeTroop(board, troop, x,y):
		#Can only place in rows 0-3
		if x == 4 or x == 5:
			PlaceManager.ErrorFunction("Placing")

	#Returns True if the attacker wins and False if the defender wins. Also returns false if the defender is equal to the attacker
	def Attack(Attacker, Defender):
		#Edge cases of Spy, bomb or flag: 
		if Defender == 'S':
			#The spy always loses an attack
			return True
		elif Attacker == '3' and Defender == 'B':
			#The 3 is the miner and beats the bomb
			return True
		elif Defender == 'B':
			return False
		elif Defender == 'F':
			return True #And Attacker wins the game
		#The spy wins against the 10 and loses against everything else.
		elif Attacker == 'S' and Defender == '10':
			return True
		else:
			return (int(Attacker) > int(Defender))
			

	def updateBoard(xstart, ystart, xend, yend, board):
		if not PlaceManager.islegal(xstart, ystart, xend, yend, board):
			#This move is illegal, try something else
			PlaceManager.ErrorFunction("Illegal Move")
			return False

		if board.MapData[xend][yend] != ['','','']:
			#The location is empty, so we place the piece
			board.MapData[xend][yend] = [color,board.getPiece(xstart,ystart), "K"]
		
		else:
			#It's an attack

			#We know it's their flag because we already checked in islegal
			if board.getPiece(xend,yend) == 'F':
				print ("Winner Winner")
				return("You Won!!")
				#Exit
			#We will handle edge cases like equivalent pieces here as then they are both removed
			elif board.getPiece(xstart,ystart) == board.getPiece(xend,yend):
				board.MapData[yend][xend] = ['','','']

			elif PlaceManager.Attack(board.getPiece(xstart,ystart), board.getPiece(ystart,yend)):
				#Won the attack
				board.MapData[xend][yend] = [board.getColor(xstart,ystart),board.getPiece(xstart,ystart), 'M']
			else:
				#Lost the attack, but we know the piece
				board.MapData[xend][yend] = [board.Color(xstart,ystart),board.Piece(xstart,ystart),'K']
	
		#Whether the piece moving lives or dies, the place it came from will still be empty
		board.MapData[xstart][ystart] = ['','','']
		return True