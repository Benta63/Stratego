import sys
import StategoBoard

class PlaceManager(object):
	def __init__():
		self.board = [10]
	
	#An error function for debugging
	def ErrorFunction(self, type):
		print("Error: {:s}".format(type))
		sys.exit()
	
	#For initial placing of troops on the board	
	def placeTroop(StrategoBoard, troop, x,y):
		#Can only place in rows 0-3
		if x == 4 or x == 5:
			self.ErrorFunction("Placing")

	#Returns True if the attacker wins and False if the defender wins. Also returns false if the defender is equal to the attacker
	def Attack(Attacker, Defender):
		#Edge cases of Spy, bomb or flag: 
		if Defender == 'S':
			return True
		elif Defender == 'B':
			return False
		elif Defender == 'F':
			return True #And Attacker wins the game
		else:
			return (int(Attacker) >= int(Defender))
			

	def updateBoard(xstart, ystart, xend, yend):
		if not islegal(xend, yend): self.ErrorFunction("Moving")
		#MAKE islegal function
		
		if StrategoBoard.MapData[xend, yend] != ['','']:
			#The location is empty, so we place the piece
			StrategoBoard.MapData[xend,yend] == [color,StrategoBoard.Piece(xstart,ystart)]
		else:
			#It's an attack
			if StrategoBoard.Piece(xend,yend) == 'F':
				print("You won!!!") 
				#Exit
			elif self.Attack(StrategoBoard.Piece(xstart,ystart), StrategoBoard.Piece(ystart,yend)):
				#Won the attack
				StrategoBoard.MapData[xend,yend] == [StrategoBoard.Color(xstart,ystart),StrategoBoard.Piece(xstart,ystart), 'M']
			else:
				#Lost the attack, but we know the piece
				StrategoBoard.MapData[xend,yend] == [StrategoBoard.Color(xstart,ystart),StrategoBoard.Piece(xstart,ystart),'K']
		#Whether the piece moving lives or dies, the place it came from will still be empty
		StrategoBoard.MapData([xstart,ystart]) = ['','']