from classes import StrategoBoard

board = StrategoBoard.StrategoBoard()

board.setBoard()

board.ReadBoard('Mine', 'BoardSetup1.txt')
board.ReadBoard('Theirs', 'BoardSetup2.txt')

print(board.getPiece(3, 8), board.getColor(3, 8))

print(board.getPiece(3, 5), board.getColor(3, 5))
