import pygame
from pygame.locals import *

pygame.init()

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

    def set_position(self, x, y):
        self.position = (x, y)
        self.pos_x = x
        self.pos_y = y

    def set_font_color(self, rgb_tuple):
        self.font_color = rgb_tuple
        self.label = self.render(self.text, 1, self.font_color)

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
            pos_y = j * (self.scr_height / 5) + (self.scr_width / 10)  - (menu_item.height / 2)
            menu_item.set_position(pos_x, pos_y)
            self.items.append(menu_item)
            i += 1
    def run(self):
        mainloop = True
        while mainloop:
            self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    mainloop = False

            self.screen.fill(self.bg_color)

            for item in self.items:
                if item.is_mouse_selection(pygame.mouse.get_pos()):
                    item.set_font_color((255, 0, 0))
                    item.set_italic(True)
                else:
                    item.set_font_color((255, 255, 255))
                    item.set_italic(False)
                self.screen.blit(item.label, item.position)
            pygame.draw.polygon(screen, (255, 255, 255), ((95, 0), (97, 0), (97, 480), (95, 480)), 0)
            pygame.draw.polygon(screen, (255, 255, 255), ((191, 0), (193, 0), (193, 480), (191, 480)), 0)
            pygame.draw.polygon(screen, (255, 255, 255), ((287, 0), (289, 0), (289, 480), (287, 480)), 0)
            pygame.draw.polygon(screen, (255, 255, 255), ((383, 0), (385, 0), (385, 480), (383, 480)), 0)
            pygame.draw.polygon(screen, (255, 255, 255), ((0, 95), (0, 97), (480, 97), (480, 95)), 0)
            pygame.draw.polygon(screen, (255, 255, 255), ((0, 191), (0, 193), (480, 193), (480, 191)), 0)
            pygame.draw.polygon(screen, (255, 255, 255), ((0, 287), (0, 289), (480, 289), (480, 287)), 0)
            pygame.draw.polygon(screen, (255, 255, 255), ((0, 383), (0, 385), (480, 385), (480, 383)), 0)
            pygame.display.flip()


def board_numbers():
    pygame.draw.polygon(screen, (255, 255, 255), ((95, 0), (97, 0), (97, 480), (95, 480)), 0)
    number = ""
    font = pygame.font.Font(None, 96)
    board = [0, 0, 0, 0, 0,
             0, 0, 0, 0, 0,
             0, 0, 0, 0, 0,
             0, 0, 0, 0, 0,
             0, 0, 0, 0, 0]
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
        pygame.draw.polygon(screen, (255, 255, 255), ((95, 0), (97, 0), (97, 480), (95, 480)), 0)
        pygame.draw.polygon(screen, (255, 255, 255), ((191, 0), (193, 0), (193, 480), (191, 480)), 0)
        pygame.draw.polygon(screen, (255, 255, 255), ((287, 0), (289, 0), (289, 480), (287, 480)), 0)
        pygame.draw.polygon(screen, (255, 255, 255), ((383, 0), (385, 0), (385, 480), (383, 480)), 0)
        pygame.draw.polygon(screen, (255, 255, 255), ((0, 95), (0, 97), (480, 97), (480, 95)), 0)
        pygame.draw.polygon(screen, (255, 255, 255), ((0, 191), (0, 193), (480, 193), (480, 191)), 0)
        pygame.draw.polygon(screen, (255, 255, 255), ((0, 287), (0, 289), (480, 289), (480, 287)), 0)
        pygame.draw.polygon(screen, (255, 255, 255), ((0, 383), (0, 385), (480, 385), (480, 383)), 0)
        pygame.display.flip()
    gm = Board(screen, board)
    gm.run()


if __name__ == "__main__":
    screen = pygame.display.set_mode((480, 480), 0, 32)
    pygame.display.set_caption('BINGO BOARD')

    board_numbers()
