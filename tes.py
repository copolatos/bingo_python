import pygame
# from pygame.locals import *

pygame.init()

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)

gameDisplay = pygame.display.set_mode((800,600))
pygame.display.set_caption('lobby')

# pygame.display.update()

gameExit = False

while not gameExit:
	for event in pygame.event.get():	
		if event.type == pygame.QUIT:
			gameExit == True
		# print(event)
	gameDisplay.fill(red)
	pygame.draw.rect(gameDisplay, black, [400,300,10,10])
	pygame.draw.rect(gameDisplay, black, [400,300,200,200])
	pygame.display.update()

pygame.quit()
quit()