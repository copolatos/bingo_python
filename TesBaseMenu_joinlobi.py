import pygame
import BOARDCLIENT_joinlobi

pygame.init()

class MenuItem(pygame.font.Font):
    def __init__(self, text, font=None, font_size=30,
                 font_color=(255, 255, 255), (pos_x, pos_y)=(0, 0)):
        pygame.font.Font.__init__(self, font, font_size)
        self.text = text
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

    def set_index(self, index):
        self.indexpos = index

    def check_index(self):
        return self.indexpos

class GameMenu():
    def __init__(self, screen, items, bg_color=(0, 0, 0), font=None, font_size=30,
                 font_color=(255, 255, 255)):
        self.screen = screen
        self.scr_width = self.screen.get_rect().width
        self.scr_height = self.screen.get_rect().height

        self.bg_color = bg_color
        self.clock = pygame.time.Clock()

        self.items = []
        i = 1
        for index, item in enumerate(items):
            menu_item = MenuItem(item)

            # t_h: total height of text block
            t_h = len(items) * menu_item.height
            pos_x = (self.scr_width / 2) - (menu_item.width / 2)
            pos_y = (self.scr_height / 2) - (t_h / 2) + ((index * 2) + index * menu_item.height)

            menu_item.set_position(pos_x, pos_y)
            menu_item.set_index(i)
            self.items.append(menu_item)
            i+=1

    def run(self):
        mainloop = True
        while mainloop:
            # Limit frame speed to 60 FPS
            self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    mainloop = False

            self.screen.fill(self.bg_color)

            for item in self.items:
                if item.is_mouse_selection(pygame.mouse.get_pos()):
                    item.set_font_color((255, 0, 0))
                    item.set_italic(True)
                    if item.check_index() == 1 and pygame.mouse.get_pressed()[0]:
                        BOARDCLIENT_joinlobi.main()
                        pygame.display.set_mode((320, 240), 0, 32)
                    elif item.check_index() == 2 and pygame.mouse.get_pressed()[0]:
                        exit()
                else:
                    item.set_font_color((255, 255, 255))
                    item.set_italic(False)
                self.screen.blit(item.label, item.position)

            pygame.display.flip()


if __name__ == "__main__":
    screen = pygame.display.set_mode((320, 240), 0, 32)

    menu_items = ('PLAY', 'QUIT')

    pygame.display.set_caption('SIMPLE BINGO')
    gm = GameMenu(screen, menu_items)
    gm.run()
