import random
import pygame
from pygame.locals import *
from time import sleep
from sys import stdin, exit
from PodSixNet.Connection import connection, ConnectionListener
from thread import *
import room

pygame.init()

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)

gameDisplay = pygame.display.set_mode((600, 400))

# pygame.display.update()

gameExit = False

font = pygame.font.SysFont(None,25)

class Client(ConnectionListener):
    nickname = random.randint(1000, 10000)
    room = random.randint(1000, 10000)
    listroom = {}
    def __init__(self, host, port):
        self.Connect((host, port))
        connection.Send({"action": "login", "nickname": Client.nickname})
	    #room = random.randint(1000, 10000)
        #nickname = random.randint(1000, 10000)
        #connection.Send({"action": "login", "nickname": Client.nickname})
        t = start_new_thread(self.InputLoop, ())

    def Loop(self):
        connection.Pump()
        self.Pump()

    def InputLoop(self):
        connection.Send({"action": "list"})

    #######################################
    ### Network event/message callbacks ###
    #######################################

    def Network_connected(self, data):
        print "Silahkan Pilih Room"

    def Network_error(self, data):
        print 'error:', data['error'][1]
        connection.Close()

    def Network_disconnected(self, data):
        print 'Server disconnected'
        #exit()

    def Network_listroom(self, data):
        Client.listroom = data['rooms']

def message_to_screen(msg,color):
	screen_text = font.render(msg,True,color)
	gameDisplay.blit(screen_text,[450,350])

def main():
    pygame.display.set_mode((600, 400))
    pygame.display.set_caption('Lobby')
    c = Client("192.168.1.25", 55555)
    joinlobby = 0
    while not gameExit:
        c.Loop()
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return

        gameDisplay.fill(black)
        roomlist = pygame.draw.rect(gameDisplay, (40,40,40), [10,10,580,300])
        rd_font = pygame.font.Font(None, 25)
        iterasi = 0
        screen_text_r = []
        cur = pygame.mouse.get_pos()
        for i in range(len(Client.listroom)):
            screen_text = rd_font.render((str(Client.listroom.items()[i]).strip('(').strip(')')), True, (255, 255, 255))
            screen_text_r.append(screen_text.get_rect())
            screen_text_r[i].x, screen_text_r[i].y = roomlist.x, roomlist.y+iterasi*20
            gameDisplay.blit(screen_text, (roomlist.x,roomlist.y+iterasi*20))
            if screen_text_r[i].collidepoint(cur):
                screen_text = rd_font.render((str(Client.listroom.items()[i]).strip('(').strip(')')), True,red)
                gameDisplay.blit(screen_text, (roomlist.x, roomlist.y + iterasi * 20))
                if pygame.mouse.get_pressed()[0] and joinlobby == 0:
                    joinlobby = 1
                    room.name(Client.nickname, Client.listroom.keys()[i], 1)
                    connection.Send({"action": "login", "nickname": Client.nickname})
                    joinlobby = 0
                    pygame.display.set_mode((600, 400))
            else:
                screen_text = rd_font.render((str(Client.listroom.items()[i]).strip('(').strip(')')), True,(255, 255, 255))
                gameDisplay.blit(screen_text, (roomlist.x, roomlist.y + iterasi * 20))
            iterasi+=1
        if cur[0] > 450 and cur[0] < 565 and cur[1] > 350 and cur[1] < 370:
            if pygame.mouse.get_pressed()[0]:
                room.name(Client.nickname, Client.room, 0)
                connection.Send({"action": "login", "nickname": Client.nickname})
                connection.Send({"action": "delroom", "roomname": Client.room})
                joinlobby = 0
                pygame.display.set_mode((600, 400))
            font.set_italic(True)
            message_to_screen("Create Room", red)
        else:
            font.set_italic(False)
            message_to_screen("Create Room", white)
        pygame.display.flip()

    pygame.quit()
    quit()
