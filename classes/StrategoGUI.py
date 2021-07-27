#from . import StrategoBoard, ActionManager
import pygame

pygame.init()
green, blue, black = (124,252,0), (0, 0, 255), (0,0,0)

gameDisplay = pygame.display.set_mode((300, 300))
# gameDisplay.fill(green)
Lakes = [[5,3], [5,4], [5,7], [5,8], [6,3], [6,4], [6,7], [6,8]]

size = 25

#board length, must be even
boardLength = 10
gameDisplay.fill(black)

for i in range(1,boardLength+1):
    for j in range(1,boardLength+1):
        #check if current loop value is even
        if [i,j] in Lakes:
            pygame.draw.rect(gameDisplay, blue,[size*j,size*i,size,size])
        else:
            pygame.draw.rect(gameDisplay, green, [size*j,size*i,size,size])
    #since theres an even number of squares go back one value
#Add a border
pygame.draw.rect(gameDisplay,black,[size,size,boardLength*size,boardLength*size],1)

pygame.display.update()
import time
time.sleep(10)
#pygame.display.iconify()

# class StrategoGUI():
# 	def __init__(self):

# 		pygame.init()
# 		green, blue = (124,252,0), (0, 0, 255)

# 		gameDisplay = pygame.display.set_mode((800,600))

# 		gameExit = False

# 		squareSize = 20
# 		board = Surface((squareSize* 10, squareSize * 10))
# 		board.fill(green)
# 		for x in range(0, 10, 2):
# 			for y in range(0, 10, 2):
# 				pygame.draw.rect(board, (0,0,0), (x*size, y*size, size, size))

# 		gameDisplay.blit(board, board.get_rect)

# 	def showBoard(self):
# 		...

