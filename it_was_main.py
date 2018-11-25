#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import sys
 
SCREEN_SIZE = (640, 480)

pygame.init()
game_is_running = True
clock = pygame.time.Clock()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption(u"2Daction")

mainfont = pygame.font.SysFont(None, 100)
lifefont = pygame.font.SysFont(None, 50)
 
# イメージを用意
backImg = pygame.image.load("background.png").convert()
backReImg = pygame.image.load("background_reversed.png").convert()
heroImg = pygame.image.load("testman.png").convert_alpha()
heroPhImg = pygame.image.load("testman-phantom.png").convert_alpha()
enemyImg = pygame.image.load("naitram.png").convert_alpha()
enemyImg1 = pygame.image.load("naitram1.png").convert_alpha()
enemyImg2 = pygame.image.load("naitram2.png").convert_alpha()
enemyImg3 = pygame.image.load("naitram3.png").convert_alpha()
enemyImg4 = pygame.image.load("naitram4.png").convert_alpha()
heroLifeImg = heroImg
gameoverImg = heroImg

groundHeight = 300 # これはクソ実装で、多分x座標ごとに設定すべき？

heroRunSpeed = 8
heroJumpForce = 17
heroWarpSpeed = 150

heroPosition = [300, groundHeight - 100]
heroJumpSpeed = 0
heroIsOnGround = True
heroIsVisible = True
heroDiggingCount = 0
heroJumpCount = 2
heroLife = 100

phantomPosition = [300,groundHeight - 100]
phantomCount = 0
phantomLife = 10

phantomToHero = 100

enemyPosition = [100,groundHeight - 50]
enemySpeed = 3
enemyCount = 0

while game_is_running:

    # イベント処理ここから
    for event in pygame.event.get():
        if event.type == QUIT:
            game_is_running = False
        if event.type == KEYDOWN:

            # リセット。変数増やしたらここもチェックすること！！！！
            if event.key == K_RETURN:
                heroPosition = [300, groundHeight - 100]
                heroJumpSpeed = 0
                heroIsOnGround = True
                heroIsVisible = True
                phantomPosition = [300,groundHeight - 100]
                phantomCount = 0
                phantomLife = 10
                heroJumpCount = 2
                enemyPosition = [100,groundHeight - 50]
                heroLife = 100
                heroDiggingCount = 0
            
            if event.key == K_ESCAPE:
                game_is_running = False

            if heroLife > 0:

                # ジャンプ
                if event.key == K_w and heroJumpCount > 0 and heroDiggingCount == 0:
                    heroJumpSpeed = heroJumpForce
                    heroIsOnGround = False
                    heroJumpCount -= 1

                # 瞬間移動、これだと走る必要がなくなるので工夫を
                if event.key == K_d and heroIsVisible and heroPosition[0] < 600 and heroDiggingCount == 0 and groundHeight == 300:
                    heroIsVisible = False
                    phantomCount = phantomLife
                    phantomPosition[0] = heroPosition[0]
                    phantomPosition[1] = heroPosition[1]
                    if heroPosition[0] < 600 - heroWarpSpeed:
                        heroPosition[0] += heroWarpSpeed
                        phantomToHero = heroWarpSpeed
                    else:
                        heroPosition[0] = 600
                        phantomToHero = heroPosition[0] - phantomPosition[0]

                if event.key == K_a and heroIsVisible and heroPosition[0] > 0 and heroDiggingCount == 0 and groundHeight == 300:
                    heroIsVisible = False
                    phantomPosition[0] = heroPosition[0]
                    phantomPosition[1] = heroPosition[1]
                    phantomCount = phantomLife
                    if heroPosition[0] > heroWarpSpeed:
                        heroPosition[0] -= heroWarpSpeed
                        phantomToHero = -heroWarpSpeed
                    else:
                        heroPosition[0] = 0
                        phantomToHero = heroPosition[0] - phantomPosition[0]
                
                if event.key == K_s and heroIsOnGround:
                    heroDiggingCount = 10

    # イベント処理ここまで


    if heroLife > 0:
        if pygame.key.get_pressed()[K_RIGHT] and heroPosition[0] < 600 and heroDiggingCount == 0 and groundHeight == 300:
            heroPosition[0] = heroPosition[0] + heroRunSpeed
        if pygame.key.get_pressed()[K_LEFT] and heroPosition[0] > 0 and heroDiggingCount == 0 and groundHeight == 300:
            heroPosition[0] = heroPosition[0] - heroRunSpeed
        if not heroIsOnGround:
            heroPosition[1] -= heroJumpSpeed
            heroJumpSpeed -= 1
            if heroPosition[1] >= groundHeight - 100:
                heroIsOnGround = True
                heroPosition[1] = groundHeight - 100
                heroJumpSpeed = 0
                heroJumpCount = 2
        
        if enemyPosition[0] > -100:
            enemyPosition[0] -= enemySpeed
        else:
            enemyPosition[0] = 800
        
        # 穴掘り中の沈む挙動
        if heroDiggingCount > 0:
            heroDiggingCount -= 1
            heroPosition[1] += 10
            groundHeight += 10
        
        # 穴消滅
        if heroPosition[1] <= 200:
            groundHeight = 300
            
        if (heroPosition[0]-enemyPosition[0]-5)**2 + 2*(heroPosition[1]-enemyPosition[1]+25)**2 < 2000:
            heroLife -= 1
        
        enemyCount += 2
        if enemyCount > 40:
            enemyCount = 2
        


    
    # 描画処理ここから

    if heroLife > 0:

        screen.blit(backImg, (-106,0))        

        if phantomCount > 0:
            phantomCount -= 1

            pygame.draw.line(screen, (200,255,255), (phantomPosition[0]+20,phantomPosition[1]), \
            (phantomPosition[0]+20+phantomToHero,phantomPosition[1]))

            pygame.draw.line(screen, (200,255,255), (phantomPosition[0]+20,phantomPosition[1]+100), \
            (phantomPosition[0]+20+phantomToHero,phantomPosition[1]+100))

            screen.blit(heroPhImg, (phantomPosition[0],phantomPosition[1]))

        if heroIsVisible:
            screen.blit(heroImg, (heroPosition[0],heroPosition[1]))
        else:
            heroIsVisible = True

        if enemyCount <= 10:
            screen.blit(enemyImg1,(enemyPosition[0],enemyPosition[1]))
        elif enemyCount <= 20:
            screen.blit(enemyImg2,(enemyPosition[0],enemyPosition[1]))
        elif enemyCount <= 30:
            screen.blit(enemyImg3,(enemyPosition[0],enemyPosition[1]))
        else:
            screen.blit(enemyImg4,(enemyPosition[0],enemyPosition[1]))

        # heroLifeImg = mainfont.render(str(heroLife), False, (0,0,0))
        # screen.blit(heroLifeImg,(10,380))
        pygame.draw.rect(screen, (252,0,0), Rect(10,430,200,40))
        heroLifeImg = lifefont.render("YOUR LIFE", False, (0,252,0))
        screen.blit(heroLifeImg,(20,435))
        pygame.draw.rect(screen, (252,252,0), Rect(10,430,2*heroLife,40))
        pygame.draw.rect(screen, (0,0,252), Rect(10,430,200,40),2)
    
    else:
        screen.blit(backReImg,(-106,0))
        gameoverImg = mainfont.render("GAME OVER", False, (252,0,50))
        screen.blit(gameoverImg,(110,200))

    pygame.display.update()

    heroLastPosition = heroPosition

    clock.tick(60)

sys.exit()