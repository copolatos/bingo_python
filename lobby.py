import pygame
from pygame.locals import *
import room

pygame.init()

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)

gameDisplay = pygame.display.set_mode((600, 400))

# pygame.display.update()

gameExit = False

font = pygame.font.SysFont(None,25)

def message_to_screen(msg,color):
	screen_text = font.render(msg,True,color)
	gameDisplay.blit(screen_text,[450,350])

def main():
    pygame.display.set_mode((600, 400))
    pygame.display.set_caption('Lobby')
    while not gameExit:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    exit()

        gameDisplay.fill(black)
        pygame.draw.rect(gameDisplay, (40,40,40), [10,10,580,300])
        cur = pygame.mouse.get_pos()
        if cur[0] > 450 and cur[0] < 565 and cur[1] > 350 and cur[1] < 370:
            if pygame.mouse.get_pressed()[0]:
                room.name()
                pygame.display.set_mode((600, 400))
            font.set_italic(True)
            message_to_screen("Create Room", red)
        else:
            font.set_italic(False)
            message_to_screen("Create Room", white)
        pygame.display.update()

    pygame.quit()
    quit()