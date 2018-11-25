#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame as pg
from pygame.locals import *
import sys
import objects as ob
import keyholder as kh
import scene
import screen

time_is_stop_now = False
clock = pg.time.Clock()
pg.display.set_caption(u"敵を避ける遊戯")

nowScene = scene.TitleScene()
clockcount = 0
time = 0
seconds = 0

pg.mixer.music.play(-1)

# sizes = [[554,800],[720,1040],[640,480],[566,800],[1004,753],[429,600],[600,424],[660,500],[827,423]]
# for s in sizes:
#     if s[0] > s[1]:
#         x = 800/s[0]
#         s[0] = 800
#         s[1] = s[1] * x
#     else:
#         x = 600/s[0]
#         s[0] = 600
#         s[1] = s[1] * x
# print(sizes)

while screen.game_is_running:

    kh.keyHolder.updateStatus()

    # イベント処理ここから
    for event in pg.event.get():
        if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
            screen.game_is_running = False
        
        if (event.type == KEYDOWN and event.key == K_RETURN) or (event.type == JOYBUTTONDOWN and event.button in (6,7)):
            if nowScene.havePause:
                time_is_stop_now = True
                screen.screen.blit(ob.pauseImg,(-10,-10))
                pg.display.update()
                while time_is_stop_now and screen.game_is_running:
                    for event in pg.event.get():
                        if event.type == KEYDOWN and event.key == K_RETURN:
                            time_is_stop_now = False
                        if event.type == QUIT or event.type == KEYDOWN and event.key == K_SPACE:
                            screen.game_is_running = False

                    clock.tick(30)

        for lyr in nowScene.lyrs:
            for obj in lyr:
                obj.process(event)
    
    # updateしまくり

    if nowScene.isEnd:
        nowScene.makeNextScene()
        nowScene = nowScene.nextScns[nowScene.nextScnNum]

    for lyr in nowScene.lyrs:
        for obj in lyr:
            obj.update()

    # 衝突しまくり
    for enm in nowScene.enms:
        enm.collide()

    # 描画処理ここから
    for lyr in nowScene.lyrs:
        for obj in lyr:
            obj.render()
    
    pg.display.update()

    time += clock.tick(60)
    clockcount += 1
    if clockcount==60:
        # print(time)
        # print(seconds)
        time = 0
        clockcount = 0
        seconds += 1

sys.exit()