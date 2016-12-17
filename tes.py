import pygame
# from pygame.locals import *

pygame.init()

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)

gameDisplay = pygame.display.set_mode((600,400))
pygame.display.set_caption('lobby')

# pygame.display.update()

gameExit = False

font = pygame.font.SysFont(None,25)

def message_to_screen(msg,color):
	screen_text = font.render(msg,True,color)
	gameDisplay.blit(screen_text,[400,300])


while not gameExit:
	for event in pygame.event.get():	
		if event.type == pygame.QUIT:
			gameExit == True
		# if event.type == 
		# print(event)
	gameDisplay.fill(black)
	# pygame.draw.rect(gameDisplay, red, [0,0,800,300])
	# pygame.draw.rect(gameDisplay, white, [400,300,200,200])
	cur = pygame.mouse.get_pos()
	# if 400 >
	message_to_screen("Create Room", white)
	pygame.display.update()

pygame.quit()
quit()