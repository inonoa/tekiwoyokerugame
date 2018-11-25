import pygame as pg
from pygame.locals import *

class KeyHolder():
    def __init__(self,):
        self.l_pressed = False
        self.r_pressed = False
        self.u_pressed = False
        self.d_pressed = False

    def updateStatus(self,):
        if pg.key.get_pressed()[K_LEFT]:
            self.l_pressed = True
        else:
            self.l_pressed = False

        if pg.key.get_pressed()[K_RIGHT]:
            self.r_pressed = True
        else:
            self.r_pressed = False

        if pg.key.get_pressed()[K_UP]:
            self.u_pressed = True
        else:
            self.u_pressed = False

        if pg.key.get_pressed()[K_DOWN]:
            self.d_pressed = True
        else:
            self.d_pressed = False

keyHolder = KeyHolder()