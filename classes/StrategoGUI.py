#from . import StrategoBoard, ActionManager
import pygame
from pygame.locals import *

pygame.init()
green, blue, black = (124,252,0), (0, 0, 255), (0,0,0)
width, height = 350, 350
gameDisplay = pygame.display.set_mode((width, height))
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

two_img = pygame.image.load('../images/two_black.png')
two_img.convert()
two_img = pygame.transform.scale(two_img, (int(width/10), int(height/10)))
rect = two_img.get_rect()
rect.center = (width/10)//2, (height/10)//2
running = True
moving = False
pygame.display.update()
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == MOUSEBUTTONDOWN:
            if rect.collidepoint(event.pos):
                moving = True
        elif event.type == MOUSEBUTTONUP:
            moving = False
        elif event.type == MOUSEMOTION and moving:
            rect.move_ip(event.rel)
    #gameDisplay.fill(green)
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

    gameDisplay.blit(two_img, rect)
    #pygame.draw.rect(gameDisplay, black, rect, 2)
    pygame.display.update()

pygame.quit()
import time
time.sleep(10)
#pygame.display.iconify()

class StrategoGUI():
	def __init__(self):
        self.green = (124,252,0)
        self.blue = (0, 0, 255)
        self.black = (0,0,0) 
        self.boardLength = 10
        self.Lakes = [[5,3], [5,4], [5,7], [5,8], [6,3], [6,4], [6,7], [6,8]]
        self.size = 25
        self.width = 350
        self.height = 350

        self.gameDisplay = pygame.display.set_mode((self.width, self.height))

		pygame.init()
	
	def fillBoard(self):
        '''Draws the grass(green) and lakes(blue) on the GUI'''
		for i in range(1,self.boardLength+1):
            for j in range(1,self.boardLength+1):
                #check if current loop value is even
                if [i,j] in self.Lakes:
                    pygame.draw.rect(self.gameDisplay, self.blue,[self.size*j,self.size*i,self.size,self.size])
                else:
                    pygame.draw.rect(self.gameDisplay, self.green, [self.size*j,self.size*i,self.size,self.size])
        
        #Add a border
        pygame.draw.rect(self.gameDisplay,self.black,[self.size,self.size,self.boardLength*ssize,self.boardLength*self.size],1)

    def load_img(self, img, loc):
        ...

    def move_img(self, img):
        ...


    def quit(self):
        pygame.quit()