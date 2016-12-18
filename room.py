import pygame
from pygame.locals import *

flag=0
pygame.init()

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

def name():

    my_font = pygame.font.Font(None, 30)

    my_string = "" 

    my_rect = pygame.Rect((40, 45, 460, 45))
    my_rect.left = 10
    my_rect.bottom = 470
    tes=-1
    global flag
    while True:
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
                    my_string = ""
                elif evt.key == K_SPACE:
                    if flag==0:
                        my_string += " "
                elif evt.key == K_ESCAPE:
                    return
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
        

if __name__ == '__main__':
    display = pygame.display.set_mode((480, 480))
    name()

    
