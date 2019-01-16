from classes import StrategoBoard
from classes import VisualBoard
import wx
import tkinter as tk
board = StrategoBoard.StrategoBoard()

board.setBoard()

board.ReadBoard('Mine', 'BoardSetup1.txt')
board.ReadBoard('Theirs', 'BoardSetup2.txt')

root = tk.Tk()
#app = wx.App(0)
Visual = VisualBoard.VisualBoard(root, board)

root.mainloop()
#Visual.MakeEmpty()
#Visual.PrintBoard()

