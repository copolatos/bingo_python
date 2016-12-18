import random
import pygame
from pygame.locals import *
from time import sleep
from sys import stdin, exit

from PodSixNet.Connection import connection, ConnectionListener

# This example uses Python threads to manage async input from sys.stdin.
# This is so that I can receive input from the console whilst running the server.
# Don't ever do this - it's slow and ugly. (I'm doing it for simplicity's sake)
from thread import *

pygame.init()

screen = pygame.display.set_mode((480, 480), 0, 32)


class Client(ConnectionListener):
    def __init__(self, host, port):
        self.Connect((host, port))
        nickname = random.randint(1000, 10000)
        connection.Send({"action": "login", "nickname": nickname})
        t = start_new_thread(self.InputLoop, ())

    def Loop(self):
        connection.Pump()
        self.Pump()

    def InputLoop(self):
        connection.Send({"action": "list"})
        while 1:
            connection.Send({"action": "message", "message": stdin.readline().rstrip("\n")})

    #######################################
    ### Network event/message callbacks ###
    #######################################

    def Network_connected(self, data):
        print "Selamat Datang, Selamat Bermain"

    def Network_error(self, data):
        print 'error:', data['error'][1]
        connection.Close()

    def Network_disconnected(self, data):
        print 'Server disconnected'
        exit()

class BoardItem(pygame.font.Font):
    def __init__(self, text, font=None, font_size=96,
                 font_color=(255, 255, 255), (pos_x, pos_y)=(0, 0)):
        pygame.font.Font.__init__(self, font, font_size)
        self.text = str(text)
        self.font_size = font_size
        self.font_color = font_color
        self.label = self.render(self.text, 1, self.font_color)
        self.width = self.label.get_rect().width
        self.height = self.label.get_rect().height
        self.dimensions = (self.width, self.height)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.position = pos_x, pos_y
        self.handle = False

    def set_position(self, x, y):
        self.position = (x, y)
        self.pos_x = x
        self.pos_y = y

    def is_mouse_selection(self, (posx, posy)):
        if (posx >= self.pos_x and posx <= self.pos_x + self.width) and \
                (posy >= self.pos_y and posy <= self.pos_y + self.height):
            return True
        return False


class Board():
    def __init__(self, screen, items, bg_color=(0, 0, 0), font=None, font_size=30,
                 font_color=(255, 255, 255)):
        self.screen = screen
        self.scr_width = self.screen.get_rect().width
        self.scr_height = self.screen.get_rect().height

        self.bg_color = bg_color
        self.clock = pygame.time.Clock()

        self.items = []
        i = 0
        j = 0
        for index, item in enumerate(items):
            menu_item = BoardItem(item)

            if i == 5:
                i = 0
                j += 1
            pos_x = i * (self.scr_width / 5) + (self.scr_width / 10) - (menu_item.width / 2)
            pos_y = j * (480 / 5) + (self.scr_width / 10)  - (menu_item.height / 2)

            menu_item.set_position(pos_x, pos_y)
            self.items.append(menu_item)
            i += 1
    def run(self):
        mainloop = True
        c = Client("localhost", 55555)
        score = ""
        while mainloop:
            c.Loop()
            # self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    mainloop = False

            self.screen.fill(self.bg_color)

            font = pygame.font.Font(None, 96)

            for item in self.items:
                bingo = 0
                if item.handle == True:
                    pygame.draw.polygon(screen, (255, 255, 255), ((item.pos_x/96*96+1, item.pos_y/96*96), (item.pos_x/96*96, item.pos_y/96*96 + 1), (item.pos_x/96*96 + 94, item.pos_y/96*96 + 95), (item.pos_x/96*96 + 95, item.pos_y/96*96 + 94)), 0)
                    pygame.draw.polygon(screen, (255, 255, 255), ((item.pos_x/96*96+94, item.pos_y/96*96), (item.pos_x/96*96+96, item.pos_y/96*96+1),(item.pos_x / 96 * 96 + 1, item.pos_y / 96 * 96 + 96),(item.pos_x/96*96, item.pos_y/96*96+95)), 0)
                if item.is_mouse_selection(pygame.mouse.get_pos()):
                    if pygame.mouse.get_pressed()[0] and item.handle == False:
                        connection.Send({"action": "message", "message": item.text})
                        item.handle=True
                        state[item.pos_x / 96 + (item.pos_y / 96) * 5] = 0
                        for i in range(0, 5):
                            if state[0 + i] == 0 and state[5 + i] == 0 and state[10 + i] == 0 and state[15 + i] == 0 and state[20 + i] == 0:
                                bingo += 1
                            if state[i * 5 + 0] == 0 and state[i * 5 + 1] == 0 and state[i * 5 + 2] == 0 and state[i * 5 + 3] == 0 and state[i * 5 + 4] == 0:
                                bingo += 1
                        if state[0] == 0 and state[6] == 0 and state[12] == 0 and state[18] == 0 and state[24] == 0:
                            bingo += 1
                        if state[4] == 0 and state[8] == 0 and state[12] == 0 and state[16] == 0 and state[20] == 0:
                            bingo += 1
                if bingo >= 5:
                    score = "B I N G O !"
                elif bingo == 4:
                    score = "B I N G "
                elif bingo == 3:
                    score = "B I N "
                elif bingo == 2:
                    score = "B I"
                elif bingo == 1:
                    score = "B"
                self.screen.blit(font.render(score, True, (255, 255, 255)), (25, 520))
                self.screen.blit(item.label, item.position)

            for i in xrange(0, 5):
                pygame.draw.polygon(screen, (255, 255, 255), ((95 + 96 * i, 0), (97 + 96 * i, 0), (97 + 96 * i, 480), (95 + 96 * i, 480)), 0)
            for i in xrange(0, 5):
                pygame.draw.polygon(screen, (255, 255, 255), ((0, 95 + 96 * i), (0, 97 + 96 * i), (480, 97 + 96 * i), (480, 95 + 96 * i)), 0)
            pygame.display.flip()


def board_numbers():
    number = ""
    font = pygame.font.Font(None, 96)
    # board = [0, 0, 0, 0, 0,
    #          0, 0, 0, 0, 0,
    #          0, 0, 0, 0, 0,
    #          0, 0, 0, 0, 0,
    #          0, 0, 0, 0, 0]
    board = [1, 2, 3, 4, 5,
             16, 17, 18, 19, 6,
             15, 24, 25, 20, 7,
             14, 23, 22, 21, 8,
             13, 12, 11, 10, 9]
    global state
    state = board
    i = 0
    j = 0
    while sum(board) < 325:
        if pygame.mouse.get_pressed()[0]:
            tempi = pygame.mouse.get_pos()[0] / 96
            tempj = pygame.mouse.get_pos()[1] / 96
            if board[tempj*5 + tempi] == 0:
                i = tempi
                j = tempj
        for evt in pygame.event.get():
            if evt.type == KEYDOWN:
                if not evt.unicode.isalpha():
                    if len(number) < 2 and evt.key != K_BACKSPACE and evt.key != K_RETURN and evt.key != K_KP_ENTER:
                        if len(number) == 0 and (evt.key == K_0 or evt.key == K_KP0):
                            pass
                        else:
                            number += evt.unicode
                    elif evt.key == K_BACKSPACE:
                        number = number[:-1]
                    elif (evt.key == K_RETURN or evt.key == K_KP_ENTER) and number != "":
                        if int(number) not in board and int(number) < 26:
                            board[j*5 + i] = int(number)
                            state[j * 5 + i] = int(number)
                            if j*5 + i < 24:
                                if i == 4:
                                    i = 0
                                    j+= 1
                                else:
                                    i+=1
                                if board[j*5 + i] != 0:
                                    reccur = 0
                                    while 1:
                                        if reccur >= 24:
                                            break
                                        elif board[reccur] == 0:
                                            j = reccur / 5
                                            i = reccur - j * 5
                                            break
                                        reccur += 1
                            else:
                                reccur = 0
                                while 1:
                                    if reccur >= 24:
                                        break
                                    elif board[reccur] == 0:
                                        j = reccur / 5
                                        i = reccur - j*5
                                        break
                                    reccur+=1
                        number = ""
            elif evt.type == QUIT:
                return
        screen.fill((0, 0, 0))
        k = 0
        l = 0
        m = 0
        while m < len(board):
            if board[m] != 0:
                block = font.render(str(board[m]), True, (255, 255, 255))
                screen.blit(block, (k * screen.get_rect().width / 5, l * screen.get_rect().height / 5))
            if k == 4:
                k = 0
                l += 1
            else:
                k+=1
            m+=1
        block = font.render(number, True, (255, 255, 255))
        screen.blit(block, (i * screen.get_rect().width/5, j*screen.get_rect().height/5))
        for i in xrange(0, 5):
            pygame.draw.polygon(screen, (255, 255, 255),((95 + 96 * i, 0), (97 + 96 * i, 0), (97 + 96 * i, 480), (95 + 96 * i, 480)), 0)
        for i in xrange(0, 5):
            pygame.draw.polygon(screen, (255, 255, 255),((0, 95 + 96 * i), (0, 97 + 96 * i), (480, 97 + 96 * i), (480, 95 + 96 * i)), 0)
        pygame.display.flip()
    gm = Board(screen, board)
    gm.run()

def main():
    pygame.display.set_caption('BINGO BOARD')
    pygame.display.set_mode((480, 640), 0, 32)
    board_numbers()