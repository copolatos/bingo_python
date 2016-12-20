import random
import pygame
from pygame.locals import *
from time import sleep
from sys import stdin, exit
from PodSixNet.Connection import connection, ConnectionListener
from thread import *
import BOARDCLIENT

flag=0

pygame.init()

class Client(ConnectionListener):
    listplayer = []

    def __init__(self, host, port):
        self.Connect((host, port))
        # connection.Send({"action": "joinroom" })
        #connection.Send({"action": "login", "nickname": Client.nickname})
	    #room = random.randint(1000, 10000)
        #nickname = random.randint(1000, 10000)
        t = start_new_thread(self.InputLoop, ())

    def Loop(self):
        connection.Pump()
        self.Pump()

    def InputLoop(self):
        connection.Send({"action": "list"})

    #######################################
    ### Network event/message callbacks ###
    #######################################

    def Network_listroom(self, data):
	print data["room"]

    def Network_users(self, data):
        print data["users"]

    def Network_connected(self, data):
        print "Selamat Datang, Selamat Bermain"

    def Network_error(self, data):
        print 'error:', data['error'][1]
        connection.Close()

    def Network_disconnected(self, data):
        print 'Server disconnected'
        exit()

def render_textrect(string, font, rect, text_color, background_color, justification=0):
    
    final_lines = []

    requested_lines = string.splitlines()
    global flag
    for requested_line in requested_lines:
        if font.size(requested_line)[0] > rect.width:
            words = requested_line.split(' ')
            
            for word in words:
                if font.size(word)[0] >= rect.width:
                    flag=1
                    word=word.strip('|')
                    word=word[:-1]
                    return
            
            
            accumulated_line = ""
            for word in words:
                test_line = accumulated_line + word + " "
                if font.size(test_line)[0] < rect.width:
                    accumulated_line = test_line 
                else: 
                    final_lines.append(accumulated_line) 
                    accumulated_line = word + " " 
            final_lines.append(accumulated_line)
        else: 
            final_lines.append(requested_line) 

    surface = pygame.Surface(rect.size) 
    surface.fill(background_color) 

    accumulated_height = 0 
    for line in final_lines: 
        if accumulated_height + font.size(line)[1] > rect.height:
            flag=1
            line=line.strip('|')
            line=line[:-1]
            return
            
        if line != "":
            tempsurface = font.render(line, 1, text_color)
            if justification == 0:
                surface.blit(tempsurface, (0, accumulated_height))
            elif justification == 1:
                surface.blit(tempsurface, ((rect.width - tempsurface.get_width()) / 2, accumulated_height))
            elif justification == 2:
                surface.blit(tempsurface, (rect.width - tempsurface.get_width(), accumulated_height))
        accumulated_height += font.size(line)[1]

    return surface

def name(nickname, roomnumber, jorc):
    d = Client("localhost", 55555)
    connection.Send({"action": "listlobby"})
    #print str(roomnumber) + " " + str(nickname)

    connection.Send({"action": "createlobby", "room": roomnumber, "user": nickname})

    if jorc == 0:
        connection.Send({"action": "createlobby", "room": roomnumber, "user": nickname})
    else:
        connection.Send({"action": "joinlobby", "room": roomnumber, "user": nickname})

    IMAGE_FILE = "avatar.png"
    image = pygame.image.load(IMAGE_FILE)
    display = pygame.display.set_mode((480, 480))
    my_font = pygame.font.Font(None, 30)

    my_string = "" 

    pygame.draw.polygon(display, (255, 255, 255), ((0, 250), (0, 255), (480, 255), (480, 250)), 0)
    pygame.draw.polygon(display, (255, 255, 255), ((0, 405), (0, 410), (480, 410), (480, 405)), 0)
    pygame.draw.polygon(display, (48,48,48), ((10, 265), (10, 395), (470, 395), (470, 265)), 0)

    p1_s=pygame.draw.polygon(display, (48,48,48), ((10, 240), (10, 152), (94, 152), (94, 240)), 0)
    p2_s=pygame.draw.polygon(display, (48,48,48), ((104, 240), (104, 152), (188, 152), (188, 240)), 0)
    p3_s=pygame.draw.polygon(display, (48,48,48), ((198, 240), (198, 152), (282, 152), (282, 240)), 0)
    p4_s=pygame.draw.polygon(display, (48,48,48), ((292, 240), (292, 152), (376, 152), (376, 240)), 0)
    p5_s=pygame.draw.polygon(display, (48,48,48), ((386, 240), (386, 152), (470, 152), (470, 240)), 0)

    tes_surface=pygame.draw.polygon(display, (48,48,48), ((10, 142), (10, 40), (470, 40), (470, 142)), 0)

    rd_font = pygame.font.Font(None, 70)
    screen_text = rd_font.render("READY",True,(255,255,255))
    screen_text_r=screen_text.get_rect()
    screen_text_r.x,screen_text_r.y=160,70
    tes_surface.top=20
    tes_surface.left = 160
    #pygame.display.update()
    display.blit (image, p1_s)
    display.blit (image, p2_s)
    display.blit (image, p3_s)
    display.blit (image, p4_s)
    display.blit (image, p5_s)
    my_rect = pygame.Rect((40, 45, 460, 45))
    my_rect.left = 10
    my_rect.bottom = 470
    tes=-1
    global flag
    while True:
        d.Loop()
        for evt in pygame.event.get():
            my_string=my_string.strip('|')
            if evt.type == KEYDOWN:
                if evt.unicode.isalpha():
                    if flag==0:
                        my_string += evt.unicode
                elif evt.key == K_BACKSPACE:
                    flag=0
                    my_string = my_string[:-1]
                elif evt.key == K_RETURN:
                    flag=0
                    #connection.Send({"action": "playermove", "message": my_string})
                    my_string = ""
                elif evt.key == K_SPACE:
                    if flag==0:
                        my_string += " "
                elif evt.key == K_ESCAPE:
                    return
        if screen_text_r.collidepoint(pygame.mouse.get_pos()):
            screen_text = rd_font.render("READY",True,(0,0,0))
            display.blit(screen_text,tes_surface.midleft)
            if pygame.mouse.get_pressed()[0]:
                BOARDCLIENT.main(nickname, roomnumber)
                return
        else:
            screen_text = rd_font.render("READY",True,(255,255,255))
            display.blit(screen_text,tes_surface.midleft)
        #if screen_text.is_mouse_selection(pygame.mouse.get_pos()):
         #   screen_text.set_font_color((255, 0, 0))
          #  screen_text.set_italic(True)
        tes+=1
        if tes%5000==0:
            my_string+='|'
        elif tes%1000==700:
            my_string=my_string.strip('|')
        rendered_text = render_textrect(my_string, my_font, my_rect, (255, 255, 255), (48, 48, 48), 0)
        #print my_string
        if rendered_text:
            display.blit(rendered_text, my_rect.topleft)
            pygame.display.update()
        

# if __name__ == '__main__':
#     display = pygame.display.set_mode((480, 480))
#     name()

    
