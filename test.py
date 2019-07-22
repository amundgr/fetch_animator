import sys
import pygame as pg
import numpy as np
import copy as cp
from time import time

#Pygame init and config
pg.init()
pg.event.set_blocked(pg.MOUSEMOTION)
myfont = pg.font.SysFont('Arial', 20)
textsurface = myfont.render('Some Text', False, (0, 0, 0))

#Color
black =   np.array([  0,   0,   0])
white =   np.array([255, 255, 255])
grey = white/2
magenta = np.array([  0, 255, 255])
red =     np.array([255,   0,   0])
green =   np.array([  0, 255,   0])
blue =    np.array([  0,   0, 255])

window = pg.display.set_mode((200, 200))
window.fill(white)
rect = pg.draw.circle(window, [0,0,0], (100, 100), 50)

window.blit(textsurface,(0,0))

print(textsurface.get_size())
pg.display.flip()
if  __name__ == '__main__':

    pressed = False
    while True:
        #Wait for input
        pg.event.wait()

        key_events = pg.key.get_pressed()

        if key_events[pg.K_SPACE]:
            if rect.collidepoint(pg.mouse.get_pos()):
                print("HIT!")
        if key_events[pg.K_ESCAPE]:
            #TODO: Add other escape options (look into interupts?)
            pg.display.quit()
            pg.quit()
            sys.exit()