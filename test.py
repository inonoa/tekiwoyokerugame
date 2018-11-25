#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame as pg
from pygame.locals import *
import sys
import os

pg.init()

screen = pg.display.set_mode((500,500))
pg.display.set_caption(u"2Daction")

heroImg = pg.image.load(os.path.join("images","testman.png")).convert_alpha()
heroImg.fill((255,0,0),special_flags = BLEND_ADD)
heroMaskmg = pg.image.load(os.path.join("images","mask.png")).convert_alpha()

while(True):
    screen.fill((0,0,255))

    for event in pg.event.get():
        if event.type == QUIT:
            sys.exit()
    
    screen.blit(heroImg,(100,100))
    # screen.blit(heroMaskmg,(100,100), special_flags = BLEND_RGBA_ADD),
    pg.display.update()