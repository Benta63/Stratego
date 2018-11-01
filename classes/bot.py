from ActionManager import PlaceManager
import StrategoBoard


#Testing 1 2 3
#Testing StrategoBoard
text = "BoardSetup.txt"
board = StrategoBoard.StrategoBoard()

board.ReadBoard(text, "Mine")
board.ReadBoard("DeboerOld.txt", "Theirs")

print (board.getArmy())
print(board.getPiece(3,0))
print(board.getColor(3,0))
print(board.getColor(7,0))
print(board.isKnown(3,0))
print(board.isKnown(7,0))
print(board.knownEnemy())
print(board.MapData[0][0])
print(board.isThere(0,0)) #True
print(board.isThere(5,0)) #False

print(board.MapData)
#Testing ActionManager
#ActionManager.ActionManager()
#ting = ActionManager.ActionManager()
PlaceManager.updateBoard(0,0,0,1,board) #Illegal
PlaceManager.updateBoard(0,3,0,3,board) #Illegal
PlaceManager.updateBoard(3,0,4,0,board) #Legal
PlaceManager.updateBoard(0,3,0,4,board) #Illegal

#Ecerything is tested
