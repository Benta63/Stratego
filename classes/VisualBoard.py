from classes import StrategoBoard
import wx
import wx.grid
import tkinter as tk


class VisualBoard(tk.Frame):
	#board is a StrategoBoard object
	def __init__(self, parent, board):
		tk.Frame.__init__(self, parent)

		#Create a canvas
		self.canvas = tk.Canvas(width = 500, height=500)
		self.canvas.pack(fill="both", expand=True)
		self.canvas.configure(background="green")
		#Let's make some lakes
		self.canvas.create_rectangle(100, 200, 200, 300, outline='blue', fill='blue')
		self.canvas.create_rectangle(300, 200, 400, 300, outline='blue', fill='blue')

		self.drag_data = {"x" : 0, "y" : 0, "item": None}
		self.board = board
		self.currentX = 0
		self.currentY = 0
		#Let's create some pieces on the board
		for x in range(0,10):
			#Let's draw some lines while we're here
			self.canvas.create_line(x*50, 0, x*50, 500)
			self.canvas.create_line(0, x*50, 500, x*50)

			for y in range(0,10):
				self.create_turtle(y*50, x*50, self.board.getColor(x, y), self.board.getPiece(x,y))
		

		#Adding bindings for clicking, dragging and releasing
		#We can move any turtle
		self.canvas.tag_bind("turtle", "<ButtonPress-1>", self.on_turtle_press)
		self.canvas.tag_bind("turtle", "<ButtonRelease-1>", self.on_turtle_release)
		self.canvas.tag_bind("turtle", "<B1-Motion>", self.on_turtle_motion)

	#Determine origin of mouse click
	def getOrigin(self, origin):
		self.currentX = origin.x
		self.currentY = origin.y


	#Creates a turtle
	#Only shows your pieces
	def create_turtle(self, x, y, color, num):
		text = ''
		if color == 'Mine':
			text = str(num)
		elif color == "Theirs":
			text = 'O' #O for opponent
		

		self.canvas.create_text(x+ 25, y + 25, anchor = 'center',font=('Helvetica', 30), text = text, tags = ("turtle", color))
		return text
	#Begin of dragging turtle

	def on_turtle_press(self, event):
		self.drag_data["item"] = self.canvas.find_closest(event.x, event.y)[0]
		self.drag_data["x"] = event.x
		self.drag_data["y"] = event.y
		self.canvas.bind("<ButtonPress-1>", self.getOrigin)

	#End of dragging the turtle
	def on_turtle_release(self, event):
		print (self.canvas.gettags("turtle"))
		if self.canvas.gettags(self.drag_data["item"])[1] == 'Theirs':
			print("ILLEGAL MOVE, MOVE YOUR OWN PIECE")
			self.drag_data["item"] = None
			print(self.currentX)
			self.drag_data["x"] = self.currentX
			self.drag_data["y"] = self.currentY

		else:

		#print(len(self.canvas.find_overlapping(0, 0, 500, 500)))
			#Reset drag info
		# print ("touching\n")
			
		# else:
		# 	print("Not touching\n")

			self.drag_data["item"] = None
			self.drag_data["x"] = 0
			self.drag_data["y"] = 0

	#Handling dragging an object
	def on_turtle_motion(self, event):
		d_x = event.x - self.drag_data["x"]
		d_y = event.y - self.drag_data["y"]

		#How much we move the piece
		self.canvas.move(self.drag_data["item"], d_x, d_y)
		#Going to the new positions
		self.drag_data["x"] = event.x
		self.drag_data["y"] = event.y
	
	#def PrintBoard(self):




		# wx.Frame.__init__(self, parent)
		# self.board = StrategoBoard.StrategoBoard()
		# #frame = wx.Frame(None, -1, "Stratego Board", size(100,100))
		# #app = wx.App(0)
		# print("In constructor")
		# size = wx.Size(10,10)
		# point = wx.Point()
		# self.grid = wx.grid.Grid(self, -1)
		# print("Grid Made")
		# self.grid.CreateGrid(10,10)
		# print("10 by 10")

	

