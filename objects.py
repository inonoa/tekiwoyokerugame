import time

import pygame as pg
from pygame.locals import *
import keyholder as kh
import screen
import random
import math
import sounds_and_musics as sams
from imagegroups import *
import joystick as js
import os

iconImg = pg.image.load(os.path.join("images","icon.png")).convert_alpha()
pg.display.set_icon(iconImg)

scsho = 0 # スクショ

class GameObject():
    def __init__(self,imgGrp,scn,lyrNum,position):
        self.imgGrp = imgGrp # 画像(複数枚かも)をまとめるオブジェクト
        self.scn = scn
        self.lyrNum = lyrNum
        scn.lyrs[lyrNum].append(self)
        self.imgNum = 0 # ImageGroupの何番目の画像を表示するかを決定する
        self.position = position # [0]:x座標, [1]:y座標

    def process(self,inpt):
        pass

    def update(self,):
        pass
    
    def render(self,):
        self.imgGrp.scrn.blit(self.imgGrp.imgs[self.imgNum],(self.position[0],self.position[1]))

class Phantom(GameObject):

    MAX_LIFE = 10

    def __init__(self,imgGrp,scn,position):
        super().__init__(imgGrp,scn,2,position)
        self.life = Phantom.MAX_LIFE
        self.isVisible = True
    
    def update(self,):
        if self.life > 0:
            self.life -= 1
        if self.life == 0 and self.isVisible:
            self.isVisible = False
    
    def render(self,):
        if self.isVisible:
            super().render()

class Hero(GameObject):


    RUN_SPEED = 8
    JUMP_FORCE = 17
    WARP_SPEED = 150
    MAX_LIFE = 100
    JUMP_CHARGE = 5

    def __init__(self,scn):
        super().__init__(heroImgGrp,scn,4,[300,200])

        self.speed = [0,0]
        self.isOnGround = True
        self.isVisible = True
        self.diggingCount = 0
        self.diggingState = 0
        self.jumpCount = 2
        self.life = Hero.MAX_LIFE
        self.fromPhantom = 0
        self.directionIsRight = True
        self.state = "standing"
        self.stateNum = 0 # stateの補助？
        self.jumpNum = 0 # 複数のstateで変数を共有するのは面倒でした
        self.stateBeforeDash = "standing"
        self.isDamaged = False
        self.footings = [] # 足場
    
    def changeImgNum(self,num):
        self.imgNum = num
        if self.directionIsRight:
            self.imgNum += 13
        # standing : 0
        # running : 1 ~ 4
        # jumping : 5 ~ 7
        # dashing : 8 ~ 9
        # digging : 10 ~ 12
    
    def process(self,inpt):
        if inpt.type == KEYDOWN:

            if self.life > 0:

                # ジャンプ
                if (inpt.key == K_w or inpt.key == K_UP) and self.jumpCount > 0 and self.diggingCount == 0:
                    self.jumpCount -= 1
                    self.state = "jumping"
                    sams.jumpsound.play()

                    if self.jumpCount == 1:
                        self.speed[1] = -Hero.JUMP_FORCE
                        self.isOnGround = False
                        self.jumpNum = 0
                    else:
                        self.jumpNum = 1

                # 瞬間移動
                if inpt.key == K_d and self.isVisible and self.position[0] < 600\
                   and self.diggingCount == 0 and self.diggingState == 0:
                    self.isVisible = False
                    phantom = Phantom(phantomIMG,self.scn,[self.position[0],self.position[1]])
                    phantom.imgNum = 1
                    if self.state != "dashing":
                        self.stateBeforeDash = self.state
                    self.state = "dashing"
                    self.stateNum = 0
                    self.directionIsRight = True
                    sams.dashsound.play()

                    if self.position[0] < 560 - Hero.WARP_SPEED:
                        self.position[0] += Hero.WARP_SPEED
                        self.fromPhantom = Hero.WARP_SPEED
                    else:
                        self.position[0] = 560
                        self.fromPhantom = self.position[0] - phantom.position[0]

                if inpt.key == K_a and self.isVisible  and self.position[0] > 0\
                   and self.diggingCount == 0 and self.diggingState == 0:
                    self.isVisible = False
                    phantom2 = Phantom(phantomIMG,self.scn,[self.position[0],self.position[1]])
                    if self.state != "dashing":
                        self.stateBeforeDash = self.state
                    self.state = "dashing"
                    self.stateNum = 0
                    self.directionIsRight = False
                    sams.dashsound.play()

                    if self.position[0] > Hero.WARP_SPEED - 20:
                        self.position[0] -= Hero.WARP_SPEED
                        self.fromPhantom = -Hero.WARP_SPEED
                    else:
                        self.position[0] = -20
                        self.fromPhantom = self.position[0] - phantom2.position[0]
                    
                # 穴掘り
                if (inpt.key == K_s or inpt.key == K_DOWN) and self.isOnGround and self.position[1] == 200:
                    self.diggingCount = 10
                    self.diggingState = 1
                    self.changeImgNum(10)
                    self.state = "digging"

        elif inpt.type == JOYBUTTONDOWN and self.life > 0:
            if inpt.button == 2 and self.jumpCount > 0 and self.diggingCount == 0:
                # ジャンプ間違ってたらこの数字を修正
                self.jumpCount -= 1
                self.state = "jumping"
                sams.jumpsound.play()

                if self.jumpCount == 1:
                    self.speed[1] = -Hero.JUMP_FORCE
                    self.isOnGround = False
                    self.jumpNum = 0
                else:
                    self.jumpNum = 1

            if inpt.button in (0,5) and self.isVisible and self.position[0] < 600\
                and self.diggingCount == 0 and self.diggingState == 0:
                # 瞬間移動(右)

                self.isVisible = False
                phantom = Phantom(phantomIMG,self.scn,[self.position[0],self.position[1]])
                phantom.imgNum = 1
                if self.state != "dashing":
                    self.stateBeforeDash = self.state
                self.state = "dashing"
                self.stateNum = 0
                self.directionIsRight = True
                sams.dashsound.play()
                if self.position[0] < 560 - Hero.WARP_SPEED:
                    self.position[0] += Hero.WARP_SPEED
                    self.fromPhantom = Hero.WARP_SPEED
                else:
                    self.position[0] = 560
                    self.fromPhantom = self.position[0] - phantom.position[0]
            
            if inpt.button in (3,4) and self.isVisible  and self.position[0] > 0\
                and self.diggingCount == 0 and self.diggingState == 0:
                # 瞬間移動(左)

                self.isVisible = False
                phantom2 = Phantom(phantomIMG,self.scn,[self.position[0],self.position[1]])
                if self.state != "dashing":
                    self.stateBeforeDash = self.state
                self.state = "dashing"
                self.stateNum = 0
                self.directionIsRight = False
                sams.dashsound.play()

                if self.position[0] > Hero.WARP_SPEED - 20:
                    self.position[0] -= Hero.WARP_SPEED
                    self.fromPhantom = -Hero.WARP_SPEED
                else:
                    self.position[0] = -20
                    self.fromPhantom = self.position[0] - phantom2.position[0]
            
            if inpt.button == 1 and self.isOnGround and self.position[1] == 200:
                # 穴掘り
                self.diggingCount = 10
                self.diggingState = 1
                self.changeImgNum(10)
                self.state = "digging"

        elif inpt.type == JOYAXISMOTION and self.life > 0:
            pass
            # if js.up() and self.jumpCount > 0 and self.diggingCount == 0:
            #     # ジャンプ(方向ボタンの方)間違ってたらこのへんを修正
            #     self.jumpCount -= 1
            #     self.state = "jumping"
            #     sams.jumpsound.play()
            # 
            #     if self.jumpCount == 1:
            #         self.speed[1] = -Hero.JUMP_FORCE
            #         self.isOnGround = False
            #         self.jumpNum = 0
            #     else:
            #         self.jumpNum = 1
            # 
            # if js.down() and self.isOnGround and self.position[1] == 200:
            #     # 穴掘り(方向ボタンの方)
            #     self.diggingCount = 10
            #     self.diggingState = 1
            #     self.changeImgNum(10)
            #     self.state = "digging"
      
    def update(self,):

        if self.life <= 0:
            self.scn.isEnd = True
            pg.mixer.music.stop()
            pg.mixer.music.load(os.path.join("musics_and_sounds","避けきれなかったらしい.ogg"))
            pg.mixer.music.play()
            pg.mixer.music.set_endevent()
            sams.beamsound.stop()
        
        else:

            self.isDamaged = False

            if not self.isVisible:
                self.isVisible = True
            
            if kh.keyHolder.r_pressed:
                self.directionIsRight = True
                if self.imgNum < 13:
                    self.imgNum += 13
            elif kh.keyHolder.l_pressed:
                self.directionIsRight = False
                if self.imgNum > 12:
                    self.imgNum -= 13
            
            if js.right():
                self.directionIsRight = True
                if self.imgNum < 13:
                    self.imgNum += 13
            elif js.left():
                self.directionIsRight = False
                if self.imgNum > 12:
                    self.imgNum -= 13
            
            # dashの後処理
            if self.state == "dashing":
                self.stateNum += 1
                if self.stateNum in range(1,10):
                    self.changeImgNum(8)
                elif self.stateNum in range(10,19):
                    self.changeImgNum(9)
                else:
                    self.state = self.stateBeforeDash

            
            # ジャンプ中の処理
            if self.state == "jumping":
                if self.jumpNum == 0:
                    if kh.keyHolder.r_pressed or kh.keyHolder.l_pressed:
                        self.changeImgNum(5)
                    else:
                        self.changeImgNum(6)
                elif self.jumpNum in range(1,Hero.JUMP_CHARGE):
                    self.jumpNum += 1
                    self.changeImgNum(7)
                elif self.jumpNum == Hero.JUMP_CHARGE:
                    self.speed[1] = -Hero.JUMP_FORCE
                    self.jumpNum += 1
                    if kh.keyHolder.r_pressed or kh.keyHolder.l_pressed:
                        self.changeImgNum(5)
                    else:
                        self.changeImgNum(6)


            # 左右移動
            if (kh.keyHolder.r_pressed or js.right()) and self.position[0] < 560 and self.diggingCount == 0 and self.diggingState == 0:
                self.position[0] += Hero.RUN_SPEED
                if self.state in ("standing","running"):
                    if self.state != "running":
                        self.state = "running"
                        self.stateNum = 0
                        self.changeImgNum(1)
                    else:
                        self.stateNum += 1
                        if self.stateNum in range(0,5):
                            self.changeImgNum(1)
                        elif self.stateNum in range(5,10):
                            self.changeImgNum(2)
                        elif self.stateNum in range(10,15):
                            self.changeImgNum(3)
                        elif self.stateNum in range(15,20):
                            self.changeImgNum(4)
                        else:
                            self.stateNum = 0
                            self.changeImgNum(1)

            elif (kh.keyHolder.l_pressed or js.left()) and self.position[0] > -20 and self.diggingCount == 0 and self.diggingState == 0:
                self.position[0] -= Hero.RUN_SPEED
                if self.state in ("standing","running"):
                    if self.state != "running":
                        self.state = "running"
                        self.stateNum = 0
                        self.changeImgNum(1)
                    else:
                        self.stateNum += 1
                        if self.stateNum in range(0,5):
                            self.changeImgNum(1)
                        elif self.stateNum in range(5,10):
                            self.changeImgNum(2)
                        elif self.stateNum in range(10,15):
                            self.changeImgNum(3)
                        elif self.stateNum in range(15,20):
                            self.changeImgNum(4)
                        else:
                            self.stateNum = 0
                            self.changeImgNum(1)
            
            # 何もしてなければstanding
            elif self.state == "running":
                self.state = "standing"


            # 落下と着地
            if not self.isOnGround and not (self.state == "jumping" and self.jumpNum in range(1,Hero.JUMP_CHARGE)):
                self.position[1] += self.speed[1]
                self.speed[1] += 1

                if self.speed[1] > 2:
                    self.changeImgNum(7)
                    self.state = "jumping"

                if self.position[1] >= 300 - 100 and self.speed[1] > 0:
                    self.isOnGround = True
                    self.position[1] = 300 - 100
                    self.speed[1] = 0
                    self.jumpCount = 2
                    self.changeImgNum(0)
                    self.state = "standing"
                
                for ft in self.footings:
                    if ft.isActive:
                        if ft.position[0]-20 < self.position[0]+50 < ft.position[0]+80:
                            if -1 < self.position[1]+100 - ft.position[1]-12 < self.speed[1]:
                                self.position[1] = ft.position[1] - 88
                                self.speed[1] = 0
                                self.jumpCount = 2
                                if ft.walksLeft:
                                    if self.position[0] > -20:
                                        self.position[0] -= 5
                                else:
                                    if self.position[0] < 560:
                                        self.position[0] += 5
                                if self.state == "jumping":
                                    self.state = "standing"
                                    self.changeImgNum(0)
                
            # 穴掘り中の沈む挙動
            if self.diggingCount > 0:
                self.diggingCount -= 1
                self.position[1] += 10
                self.imgNum += 1
                if self.imgNum in (13,26):
                    self.changeImgNum(10)
                if self.diggingCount <= 0:
                    self.state = "standing"

            if self.position[1] <= 200:
                self.diggingState = 0

            if self.state == "standing":
                self.changeImgNum(0)
            
    def render(self,):
        if self.isVisible:
            if self.position[1] > 200:
                self.imgGrp.scrn.blit(heroHoleImg,(self.position[0],300),(0,300-self.position[1],100,self.position[1]-190))
            if self.isDamaged:
                tmpimg = self.imgGrp.imgs[self.imgNum].copy()
                self.imgGrp.imgs[self.imgNum].fill((0,100,100),special_flags=BLEND_SUB)
                super().render()
                self.imgGrp.imgs[self.imgNum] = tmpimg
            else:
                super().render()
            if self.state == "dashing" and self.stateNum < 10:
                if self.directionIsRight:
                    self.imgGrp.scrn.blit(heroDashImg_R,(self.position[0]-120,self.position[1]))
                else:
                    self.imgGrp.scrn.blit(heroDashImg_L,(self.position[0]+70,self.position[1]))

class ResultSceneSwitcher():
    def __init__(self,scn):
        global scsho
        scn.isEnd = True
        scn.nextScnNum = 1
        pg.mixer.music.stop()
        pg.mixer.music.load(os.path.join("musics_and_sounds",'避けきったらしい(intro).ogg'))
        pg.mixer.music.set_endevent(USEREVENT)
        scsho = screen.screen.copy()

class ResultObj(GameObject):

    # これはテスト用のクラスでした。

    def __init__(self,scn):
        super().__init__(resultImgGrp,scn,0,(-10,-10))
    
    def process(self,inpt):
        if inpt.type == KEYDOWN and inpt.key == K_t:
            self.scn.isEnd = True

class ClearObj(GameObject):
    def __init__(self,scn):
        super().__init__(resultStrImgGrp,scn,9,[100,600])
        self.renderTogether = False
        self.cmt = None
        self.musicWaitingCount = 0
    
    def process(self,inpt):
        if self.renderTogether and \
        ((inpt.type == KEYDOWN and inpt.key == K_t) or (inpt.type == JOYBUTTONDOWN and inpt.button in (6,7))):
        # 最初に戻るやつ
            self.scn.isEnd = True
            pg.mixer.music.load(os.path.join("musics_and_sounds","走って跳んで掘って避けて.ogg"))
            pg.mixer.music.play(-1)
        if inpt.type == USEREVENT:
            pg.mixer.music.load(os.path.join("musics_and_sounds",'避けきったらしい.ogg'))
            pg.mixer.music.play(-1)
    
    def update(self,):
        self.musicWaitingCount += 1
        if self.musicWaitingCount==60:
            pg.mixer.music.play()
        if self.position[1] > 60:
            self.position[1] -= 3
            if self.position[1] <= 60:
                self.cmt.isActive = True

    def render(self,):
        super().render()
        if self.renderTogether:
            self.imgGrp.scrn.blit(self.imgGrp.imgs[1],(70,240))
            self.imgGrp.scrn.blit(self.imgGrp.imgs[2],(400,440))
            self.imgGrp.scrn.blit(scsho,(200,378),(0,420,220,60))

class Comet(GameObject):
    def __init__(self,scn):
        super().__init__(cometImgGrp,scn,5,[850,-440])
        self.isActive = False
        self.clrobj = None
    
    def update(self,):
        if self.isActive:
            self.position[0] -= 9
            self.position[1] += 12

            if self.position[1] > 800:
                self.clrobj.renderTogether = True
                self.isActive = False
    
    def render(self,):
        if self.isActive:
            super().render()

class HPGauge(GameObject):

    X = 0
    Y = 420
    LIFE_FONT = pg.font.SysFont(None, 50)
    LIFE_IMG = LIFE_FONT.render("YOUR LIFE", False, (0,252,0))

    def __init__(self,hero,imgGrp,scn):
        self.hero = hero
        self.imgGrp = imgGrp
        self.scn = scn
        self.scn.lyrs[9].append(self)
        self.flickerCnt = 0
        self.imgNum = 0
    
    def update(self,):
        if self.hero.life < 50:
            self.imgNum = 2
        if self.hero.life < 20:
            if self.flickerCnt < 30:
                self.imgNum = 4
            else:
                self.imgNum = 6
        self.flickerCnt += 1
        if self.flickerCnt > 59:
            self.flickerCnt = 0
    
    def render(self,):
        self.imgGrp.scrn.blit(self.imgGrp.imgs[self.imgNum],(HPGauge.X,HPGauge.Y))
        pg.draw.rect(self.imgGrp.scrn, (252,252,0), Rect(HPGauge.X+10,HPGauge.Y+10,self.hero.life*2,40))
        self.imgGrp.scrn.blit(self.imgGrp.imgs[self.imgNum+1],(HPGauge.X,HPGauge.Y))

class Enemy(GameObject):
    def __init__(self,imgGrp,scn,lyrNum,position,area,hero):
        super().__init__(imgGrp,scn,lyrNum,position)
        self.area = area
        self.hero = hero
        self.scn.enms.append(self)
    
    def damage(self,):
        self.hero.life -= 1
        self.hero.isDamaged = True

class Stuttle(Enemy):
    def __init__(self,scn,position,hero,walksLeft):
        super().__init__(stuttleImgGrp,scn,7,position,(45,15),hero)
        self.walksLeft = walksLeft
        self.hero.footings.append(self)
        self.movingCount = 0
        self.isActive = True
    
    def changeImgNum(self,Num):
        if self.walksLeft:
            self.imgNum = Num
        else:
            self.imgNum = Num + 6
    
    def update(self,):
        if self.isActive:
            if self.walksLeft:
                self.position[0] -= 5
            else:
                self.position[0] += 5
            
            if not (-300 < self.position[0] < 800):
                self.isActive = False
                return None
            
            self.movingCount += 1
            if self.movingCount == 60:
                self.movingCount = 0
            for n in range(6):
                if self.movingCount == 10*n:
                    self.changeImgNum(n)
    
    def collide(self,):
        if self.isActive:
            if self.position[0]-20 < self.hero.position[0]+50 < self.position[0]+90 and\
               self.hero.position[1] < self.position[1]+20 < self.hero.position[1]+100:
               self.damage()
    
    def render(self,):
        if self.isActive:
            super().render()

class NormalEnemy(Enemy):

    SPEED = 3

    def __init__(self,imgGrp,scn,position,area,hero,walksLeft):
        super().__init__(imgGrp,scn,7,position,area,hero)
        self.isActive = True
        self.walkCount = 0
        self.walksLeft = walksLeft
        if self.walksLeft:
            self.imgNum = 0
        else:
            self.imgNum = 4
    
    def update(self,):
        if self.isActive:
            if self.walksLeft:
                self.position[0] -= NormalEnemy.SPEED
            else:
                self.position[0] += NormalEnemy.SPEED

            self.walkCount += 1
            if self.walkCount == 40:
                self.walkCount = 0

                self.imgNum -= 3
            elif self.walkCount in (10,20,30):
                self.imgNum += 1

            if self.position[0] < -100 or self.position[0] > 800:
                self.isActive = False
    
    def collide(self,):
        if self.isActive:
            if 2*((self.position[0]+self.area[0]/2)-(self.hero.position[0]+50))**2 \
            + ((self.position[1]+self.area[1]/2)-(self.hero.position[1]+50))**2 < 3000:
                self.damage()
    
    def render(self,):
        if self.isActive:
            super().render()

class TallEnemy(NormalEnemy):

    def __init__(self,imgGrp,scn,position,area,hero,walksLeft):
        super().__init__(imgGrp,scn,position,area,hero,walksLeft)
        self.imgNums = []
        if not self.walksLeft:
            self.imgNum = 4
        for n in range(9):
            self.imgNums.append(random.randrange(8))

    def collide(self,):
        if self.isActive:
            if self.hero.position[0]+5  < self.position[0] and self.position[0] < self.hero.position[0]+45\
           and self.hero.position[1]-500 < self.position[1] and self.position[1] < self.hero.position[1]+100:
                self.damage()

    def update(self,):
        if self.isActive:

            self.walkCount += 1
            if self.walkCount == 40:
                self.walkCount = 0

                self.imgNum -= 3
            elif self.walkCount in (30,20,10):
                self.imgNum += 1
            
            if self.walksLeft:
                self.position[0] -= TallEnemy.SPEED
            else:
                self.position[0] += TallEnemy.SPEED

            if self.position[0] < -100 or self.position[0] > 800:
                self.isActive = False
    
    def render(self,):
        if self.isActive:
            for n in range(9):
                self.imgGrp.scrn.blit(self.imgGrp.imgs[self.imgNums[n]],(self.position[0],self.position[1]+50*n))
            self.imgGrp.scrn.blit(self.imgGrp.imgs[self.imgNum],(self.position[0],self.position[1]+450))

class Guin(Enemy):
    def __init__(self,scn,position,hero,walksLeft):
        self.imgGrp = guinImgGrp
        self.scn = scn
        self.scn.lyrs[7].append(self)
        self.position = position
        self.hero = hero
        self.count = 0
        self.isActive = True
        self.scn.enms.append(self)
        self.walksLeft = walksLeft
        if self.walksLeft:
            self.imgNum = 8
        else:
            self.imgNum = 0

    def update(self,):
        if self.isActive:
            if self.walksLeft:
                self.position[0] -= 4
            else:
                self.position[0] += 4

            self.count += 1

            for c in range(1,8):
                if self.count == 10*c:
                    self.imgNum += 1
                    break
            else:
                if self.count == 80:
                    self.count = 0
                    self.imgNum -= 7
            
            if self.position[0]>800 or self.position[0]<-250:
                self.isActive = False

    def collide(self,):
        if self.isActive:
            if self.hero.position[1]+100 > self.position[1]+20  and \
               self.hero.position[1]     < self.position[1]+50  and \
               \
               self.hero.position[0]+70  > self.position[0]+25  and \
               self.hero.position[0]+30  < self.position[0]+155 :
               self.damage()

class Arim(Enemy):
    def __init__(self,imgGrp,scn,position,hero,walksLeft):
        super().__init__(imgGrp,scn,7,position,[100,100],hero)
        self.isActive = True
        self.walkCount = 0
        self.fireRotationCount = 0
        self.firePositions = [[0,0],[0,0],[0,0]]
        self.fireSizes = [1,0,2] # 0:小、1:中、2:大
        self.walksLeft = walksLeft
        if not self.walksLeft:
            self.imgNum = 5
    
    def update(self,):
        if self.isActive:
            if self.walksLeft:
                self.position[0] -= 2
            else:
                self.position[0] += 2

            if self.position[0] < -200 or self.position[0] > 800:
                self.isActive = False

            self.walkCount += 1
            if self.walkCount == 26:
                self.walkCount = 0
                if self.imgNum == 0 or self.imgNum == 5:
                    self.imgNum += random.randrange(2)
                elif self.imgNum == 4 or self.imgNum == 9:
                    self.imgNum -= random.randrange(2)
                else:
                    self.imgNum += random.randrange(3) - 1
            
            self.fireRotationCount += 1

            # 遠近法
            if self.fireRotationCount == 15*2:
                self.fireSizes[0] = 2
                self.fireSizes[2] = 1
            elif self.fireRotationCount == 30*2:
                self.fireSizes[0] = 1
                self.fireSizes[1] = 0
            elif self.fireRotationCount == 45*2:
                self.fireSizes[1] = 1
                self.fireSizes[2] = 2
            elif self.fireRotationCount == 60*2:
                self.fireSizes[0] = 0
                self.fireSizes[2] = 1
            elif self.fireRotationCount == 75*2:
                self.fireSizes[0] = 1
                self.fireSizes[1] = 2
            elif self.fireRotationCount == 90*2:
                self.fireSizes[1] = 1
                self.fireSizes[2] = 0
                self.fireRotationCount = 0

            # 火の玉の座標決定
            angles = [math.radians(self.fireRotationCount*2),math.radians(self.fireRotationCount*2+120),math.radians(self.fireRotationCount*2+240)]
            for i in range(3):
                if self.imgNum == 0 or self.imgNum == 9:
                    self.firePositions[i][0] = self.position[0]+41 + 150*math.cos(angles[i]) # 50
                    self.firePositions[i][1] = self.position[1]+29 + 150*math.cos(angles[i]) # 50
                elif self.imgNum == 1 or self.imgNum == 8:
                    self.firePositions[i][0] = self.position[0]+28 + 198*math.cos(angles[i]) # 66
                    self.firePositions[i][1] = self.position[1]+18 + 69*math.cos(angles[i]) # 23
                elif self.imgNum == 2 or self.imgNum == 7:
                    self.firePositions[i][0] = self.position[0]+15 + 210*math.cos(angles[i]) # 70
                    self.firePositions[i][1] = self.position[1]+15
                elif self.imgNum == 3 or self.imgNum == 6:
                    self.firePositions[i][0] = self.position[0]+ 2 + 198*math.cos(angles[i]) # 66
                    self.firePositions[i][1] = self.position[1]+18 - 69*math.cos(angles[i]) # 23
                elif self.imgNum == 4 or self.imgNum == 5:
                    self.firePositions[i][0] = self.position[0]-11 + 150*math.cos(angles[i]) # 50
                    self.firePositions[i][1] = self.position[1]+29 - 150*math.cos(angles[i]) # 50
                else:
                    print("なんかarimおかしくね？")
        
    def collide(self,):
        if self.isActive:
            if self.imgNum == 0 or self.imgNum == 9:
                e1,e2,h1,h2 = (self.position[0]+80,self.position[1]+25), (self.position[0]+30,self.position[1]+75),\
                              (self.hero.position[0]+35,self.hero.position[1]+5), (self.hero.position[0]+65,self.hero.position[1]+95)
                if (e1[0]-h1[0])*(e2[0]-h2[0]) < 0 and (e1[1]-h1[1])*(e2[1]-h2[1]) < 0:
                    if ((e1[0]-h1[0])-(e1[1]-h1[1])) * ((e2[0]-h2[0])-(e2[1]-h2[1])) < 0:
                        self.damage()

            if self.imgNum == 1 or self.imgNum == 8:
                e1,e2,h1,h2 = (self.position[0]+60,self.position[1]+20), (self.position[0]+45,self.position[1]+80),\
                              (self.hero.position[0]+35,self.hero.position[1]+5), (self.hero.position[0]+65,self.hero.position[1]+95)
                if (e1[0]-h1[0])*(e2[0]-h2[0]) < 0 and (e1[1]-h1[1])*(e2[1]-h2[1]) < 0:
                    if (2*(e1[0]-h1[0])-(e1[1]-h1[1])) * (2*(e2[0]-h2[0])-(e2[1]-h2[1])) < 0:
                        self.damage()

            if self.imgNum == 2 or self.imgNum == 7:
                e1,e2,h1,h2 = (self.position[0]+50,self.position[1]+10), (self.position[0]+50,self.position[1]+90),\
                              (self.hero.position[0]+35,self.hero.position[1]+5), (self.hero.position[0]+65,self.hero.position[1]+95)
                if (e1[0]-h1[0])*(e2[0]-h2[0]) < 0 and (e1[1]-h1[1])*(e2[1]-h2[1]) < 0:
                    self.damage()
            
            if self.imgNum == 3 or self.imgNum == 6:
                e1,e2,h1,h2 = (self.position[0]+40,self.position[1]+20), (self.position[0]+55,self.position[1]+80),\
                              (self.hero.position[0]+65,self.hero.position[1]+5), (self.hero.position[0]+35,self.hero.position[1]+95)
                if (e1[0]-h1[0])*(e2[0]-h2[0]) < 0 and (e1[1]-h2[1])*(e2[1]-h1[1]) < 0:
                    if (2*(e1[0]-h1[0])+(e1[1]-h1[1])) * (2*(e2[0]-h2[0])+(e2[1]-h2[1])) < 0:
                        self.damage()

            if self.imgNum == 3 or self.imgNum == 6:
                e1,e2,h1,h2 = (self.position[0]+20,self.position[1]+25), (self.position[0]+70,self.position[1]+75),\
                              (self.hero.position[0]+65,self.hero.position[1]+5), (self.hero.position[0]+35,self.hero.position[1]+95)
                if (e1[0]-h1[0])*(e2[0]-h2[0]) < 0 and (e1[1]-h2[1])*(e2[1]-h1[1]) < 0:
                    if (2*(e1[0]-h1[0])+(e1[1]-h1[1])) * (2*(e2[0]-h2[0])+(e2[1]-h2[1])) < 0:
                        self.damage()
            
            for i in range(3):
                if self.fireSizes[i] == 1:
                    if 2*((self.firePositions[i][0]+35)-(self.hero.position[0]+50))**2 \
                       + ((self.firePositions[i][1]+35)-(self.hero.position[1]+50))**2 < 1500:
                       self.damage()

    def render(self,):
        if self.isActive:
            for i in range(3):
                if self.fireSizes[i] == 0 or self.fireSizes[i] == 1:
                    self.imgGrp.scrn.blit(self.imgGrp.imgs[self.fireSizes[i]+10],(self.firePositions[i][0],self.firePositions[i][1]))
            self.imgGrp.scrn.blit(self.imgGrp.imgs[self.imgNum],(self.position[0],self.position[1]))
            for i in range(3):
                if self.fireSizes[i] == 2:
                    self.imgGrp.scrn.blit(self.imgGrp.imgs[self.fireSizes[i]+10],(self.firePositions[i][0],self.firePositions[i][1]))

class GameRestarter():
    def __init__(self,scn):
        self.scn = scn
        scn.lyrs[0].append(self)
    
    def process(self,inpt):
        if (inpt.type == KEYDOWN and inpt.key == K_s) or (inpt.type == JOYBUTTONDOWN and inpt.button == 0):
            self.scn.isEnd = True
            pg.mixer.music.stop()
            pg.mixer.music.load(os.path.join("musics_and_sounds",'走って跳んで掘って避けて.ogg'))
            pg.mixer.music.play(-1)
    
    def update(self,):
        pass
    
    def render(self,):
        pass

class TitleUI(GameObject):


    def __init__(self,scn):
        super().__init__(titleImgGrp,scn,9,[-10,-10])

    def process(self,inpt):
        if inpt.type == KEYDOWN:
            if inpt.key == K_s or inpt.key == K_RETURN:
                sams.oksound.play()
                if self.imgNum == 0:
                    self.scn.isEnd = True
                else:
                    screen.game_is_running = False
                    time.sleep(1)

            elif inpt.key == K_DOWN:
                self.imgNum = 1
                sams.typesound.play()
            elif inpt.key == K_UP:
                self.imgNum = 0
                sams.typesound.play()

        elif inpt.type == JOYBUTTONDOWN:
            if inpt.button == 0:
                sams.oksound.play()
                if self.imgNum == 0:
                    self.scn.isEnd = True
                else:
                    screen.game_is_running = False
                    time.sleep(1)
        
        elif inpt.type == JOYAXISMOTION:
            if js.up():
                self.imgNum = 0
                sams.typesound.play()
            elif js.down():
                self.imgNum = 1
                sams.typesound.play()

class Boss():
    def __init__(self,scn,hero):
        self.scn = scn
        self.hero = hero

        self.imgGrp = bossImgGrp # 画像(複数枚かも)をまとめるオブジェクト
        self.lyrNum = 5
        scn.lyrs[5].append(self)
        self.scn.enms.append(self)
        self.imgNum = 0
        self.position = [800,0]
        self.state = "entering"
        self.count = 0

    def process(self,inpt):
        pass
    
    def update(self,):
        if self.state == "tested":
            if self.count <= 0:
                self.imgNum = 1
                self.position[0] -= 8
            if self.position[0] < -200:
                self.position[0] = 1000
            
            if 350 <= self.position[0] <= 357:
                if self.count <= 0:
                    self.count = 50
                    self.imgNum = 0
                else:
                    self.count -= 1
        elif self.state == "entering":
            self.position[0] -= 2
            if self.position[0] < 400:
                self.state = "waiting1"
        elif self.state == "waiting1":
            self.count += 1
            if self.count in (40,120):
                self.imgNum = 2
            elif self.count in (80,160):
                self.imgNum = 0 
            elif self.count == 200:
                self.count = 0
                self.state = "ready1"
                self.imgNum = 3
        elif self.state == "ready1":
            if self.position[0] < 500:
                self.position[0] += 10
            else:
                self.count += 1
                self.imgNum = 0
                if self.count > 50:
                    self.imgNum = 1
                    self.state = "rushing1"
                    self.count = 0
        elif self.state == "rushing1":
            self.position[0] = 490 - 10 * self.count
            self.position[1] = -0.14 * ((27 - self.count)**2) + 110
            self.count += 1
            if self.position[0] < -55:
                self.imgNum = 3
                self.state = "rushing2"
        elif self.state == "rushing2":
            self.position[0] = 490 - 10 * self.count
            self.position[1] = -0.14 * ((27 - self.count)**2) + 110
            self.count -= 1
            if self.count == 0:
                self.count = 0
                self.imgNum = 0
                self.state = "ready2"
        elif self.state == "ready2":
            self.count += 1
            if self.count > 100:
                self.position[0] += 2
                if self.position[0] > 640:
                    self.count = 0
                    self.position = [100,-200]
                    self.imgNum = 4
                    self.state = "readytobeam1"
        elif self.state == "readytobeam1":
            if self.position[1] < -80:
                self.position[1] += 2
            else:
                self.count += 1
                if self.count == 30:
                    self.imgNum = 5
                elif self.count > 50:
                    self.count = 0
                    self.imgNum = 6
                    self.state = "beaming1"
                    sams.beamsound.play()
        elif self.state == "beaming1":
            self.count += 1
            if self.count > 30:
                self.count = 0
                self.imgNum = 4
                self.state = "tracing1"
        elif self.state == "tracing1":
            self.count += 1
            if self.count < 100:
                if self.position[0]+60 < self.hero.position[0]:
                    self.position[0] += 7
                elif self.position[0]+40 > self.hero.position[0]:
                    self.position[0] -= 7
            else:
                self.state = "readytobeam2"
                self.count = 0
                self.imgNum = 5
        elif self.state == "readytobeam2":
            self.count += 1
            if self.count > 20:
                self.count = 0
                self.imgNum = 6
                self.state = "beaming2"
                sams.beamsound.play()
        elif self.state == "beaming2":
            self.count += 1
            if self.count > 30:
                self.count = 0
                self.imgNum = 4
                self.state = "tracing2"
        elif self.state == "tracing2":
            self.count += 1
            if self.count < 70:
                if self.position[0]+60 < self.hero.position[0]:
                    self.position[0] += 10
                elif self.position[0]+40 > self.hero.position[0]:
                    self.position[0] -= 10
            else:
                self.state = "readytobeam3"
                self.count = 0
                self.imgNum = 5
        elif self.state == "readytobeam3":
            self.count += 1
            if self.count > 20:
                self.count = 0
                self.imgNum = 6
                self.state = "beaming3"
                sams.beamsound.play(-1)
        elif self.state == "beaming3":
            self.count += 1
            if self.count > 20:
                if self.position[0]+60 < self.hero.position[0]:
                        self.position[0] += 6
                elif self.position[0]+40 > self.hero.position[0]:
                    self.position[0] -= 6
            if self.count > 200:
                self.count = 0
                self.imgNum = 4
                self.state = "ready3"
                sams.beamsound.stop()
        elif self.state == "ready3":
            self.count += 1
            if self.count > 50:
                self.position[1] -= 5
                if self.position[1] < -200:
                    self.position = [700,0]
                    self.count = 0
                    self.imgNum = 7
                    self.state = "readytodirect1"
        elif self.state == "readytodirect1":
            if self.position[0] > 500:
                self.position[0] -= 3
            else:
                self.count += 1
                if self.count > 50:
                    self.count = 0
                    self.imgNum = 8
                    self.state = "directing1"
                    for n in range(9):
                        stuttle = Stuttle(self.scn,[640+40*abs(n-4),270-30*n],self.hero,True)
        elif self.state == "directing1":
            self.count += 1
            if self.count > 120:
                self.imgNum = 7
                self.position[0] += 8
                if self.position[0] > 650:
                    self.position = [-260,0]
                    self.count = 0
                    self.imgNum = 9
                    self.state = "readytodirect2"
        elif self.state == "readytodirect2":
            if self.position[0] < -60:
                self.position[0] += 5
            else:
                self.count += 1
                if self.count > 50:
                    self.count = 0
                    self.imgNum = 10
                    self.state = "directing2"
                    for n in range(9):
                        stuttle = Stuttle(self.scn,[-100-40*abs(n-4),270-30*n],self.hero,False)
        elif self.state == "directing2":
            self.count += 1
            if self.count > 100:
                self.imgNum = 9
                self.position[0] -= 10
                if self.position[0] < -210:
                    self.position = [220,-200]
                    self.count = 0
                    self.imgNum = 4
                    self.state = "readytosomething"
        elif self.state == "readytosomething":
            if self.position[1] < -80:
                self.position[1] += 8
            else:
                self.count += 1
                if self.count == 20:
                    self.imgNum = 5
                elif self.count > 30:
                    self.count = 0
                    self.imgNum = 6
                    self.state = "something"
                    sams.beamsound.play(-1)
                    for n in range(9):
                        stuttle = Stuttle(self.scn,[-100-40*abs(n-4),270-30*n],self.hero,False)
                    for n in range(9):
                        stuttle = Stuttle(self.scn,[640+40*abs(n-4),270-30*n],self.hero,True)
        elif self.state == "something":
            self.count += 1
            if self.count == 200:
                self.imgNum = 4
                sams.beamsound.stop()
                self.state = "tired"
        elif self.state == "tired":
            self.count += 1
            if 400 > self.count > 300:
                if self.count % 10 < 5:
                    self.imgNum = 11
                else:
                    self.imgNum = 12
            elif 500 > self.count > 400:
                self.imgNum = 4
            elif self.count > 500:
                self.position[1] += 2
                if self.position[1] > 600:
                    self.state = "left"

    def collide(self,):
        d1 = ((self.position[0]+100)-(self.hero.position[0]+50))**2 + ((self.position[1]+100)-(self.hero.position[1]+5))**2
        d2 = ((self.position[0]+100)-(self.hero.position[0]+50))**2 + ((self.position[1]+100)-(self.hero.position[1]+95))**2
        if d1 < 8100 or d2 < 8100:
            self.hero.life -= 1
            self.hero.isDamaged = True
        elif self.state in ("beaming1","beaming2","beaming3","something"):
            if 5 < self.hero.position[0]-self.position[0] < 95:
                self.hero.life -= 1
                self.hero.isDamaged = True

    def render(self,):
        self.imgGrp.scrn.blit(self.imgGrp.imgs[self.imgNum],(self.position[0],self.position[1]))

class EnemySpawner():
    def __init__(self,scn,hero):
        self.count = 0
        self.scn = scn
        self.scn.lyrs[0].append(self)
        self.haveLaunchEnemy_s = False
        self.hero = hero

        self.enemy_and_time = [
                               # n数体
                               [100,"n",800,250,True],[200,"n",800,250,True],[40,"n",800,250,True],[40,"n",800,250,True],
                               # nが浮く
                               [200,"n",800,100,True],[0,"g",800,350,True],
                               [200,"n",800,160,True],[200,"n",800,180,True],[0,"g",800,350,True],
                               [60,"n",800,80,True],[10,"n",800,30,True],
                               # aを出す
                               [200,"a",800,200,True],[0,"g",800,320,True],[100,"g",800,380,True],[100,"g",330,440,True],
                               [100,"a",800,100,True],[0,"g",800,320,True],[0,"g",800,400,True],[100,"g",800,400,True],
                               # nが後ろから出る(誘導しておくこと)
                               [200,"n",800,200,True],[0,"g",800,350,True],[100,"n",800,200,True],
                               [150,"n",-100,250,False],[50,"g",-200,300,False],[50,"g",-200,340,False],
                               # tが出る
                               [0,"t",800,-200,True],[100,"n",-100,200,False],[100,"t",800,-200,True],
                               [100,"n",-100,200,False],[0,"t",800,-200,True],[0,"g",-200,350,False],
                               [200,"n",-100,50,False],[20,"n",-100,100,False],[0,"g",800,320,True],[20,"n",-100,150,False],[20,"n",-100,200,False],
                               [20,"t",-100,-200,False],
                               # tだらけ
                               [200,"t",800,-200,True],[20,"t",800,-200,True],[20,"t",800,-200,True],[20,"t",800,-200,True],[20,"t",800,-200,True],
                               [20,"t",800,-200,True],[20,"t",800,-200,True],[20,"t",800,-200,True],
                               [20,"t",800,-200,True],[20,"t",800,-200,True],[20,"t",800,-200,True],
                               # tとgが出る
                               [200,"g",800,310,True],[30,"g",-200,350,False],[40,"t",-100,-200,False],
                               [10,"g",800,380,True],[60,"g",-200,370,False],[10,"g",800,305,True],
                               # sが出る
                               [100,"s",800,200,True],[0,"g",-200,350,False],[0,"g",800,370,True],
                               [150,"n",800,180,True],[100,"s",800,250,True],[0,"g",800,320,True],[20,"s",800,250,True],[20,"s",800,250,True],
                               # めっちゃ乗って安心
                               [0,"g",-200,350,False],[100,"s",-100,200,False],[0,"g",-200,350,False],[20,"s",-100,200,False],[20,"s",-100,200,False],[20,"s",-100,200,False],
                               [30,"s",-100,150,False],[20,"s",-100,150,False],
                               [30,"a",800,200,True],
                               [0,"s",-100,100,False],[0,"g",800,320,True],[20,"s",-100,100,False],[30,"s",-100,50,False],[20,"s",-100,50,False],
                               [30,"s",-100,0,False],[20,"s",-100,0,False],[20,"s",-100,0,False],[20,"s",-100,0,False],
                               [20,"s",-100,0,False],[0,"g",800,320,True],[20,"s",-100,0,False],[0,"g",-200,350,False],[20,"s",-100,0,False],[20,"s",-100,0,False],
                               [30,"s",-100,50,False],[20,"s",-100,50,False],[30,"s",-100,100,False],[20,"s",-100,100,False],
                               [30,"s",-100,150,False],[20,"s",-100,150,False],[30,"s",-100,200,False],[0,"g",800,320,True],[20,"s",-100,200,False],
                               # sでステージを作る
                               [100,"n",800,250,True],[20,"n",800,250,True],[20,"n",800,250,True],
                               [20,200],[0,"n",800,250,True],
                               [20,200],[0,"g",800,370,True],[0,"n",800,250,True],[0,"g",-200,350,False],
                               [20,150],[0,200],[0,"n",800,250,True],
                               [20,150],[0,200],[0,"n",800,250,True],
                               [20,100],[0,150],[0,"g",800,370,True],[0,200],[0,"n",800,250,True],
                               [20,100],[0,150],[0,200],[0,"n",800,250,True],
                               [20,50], [0,100],[0,150],[0,200],[0,"n",800,250,True],
                               [20,50], [0,100],[0,"g",800,320,True],[0,150],[0,200],[0,"n",800,250,True],[0,"g",-200,350,False],
                               [20,0],  [0,50], [0,100],[0,150],[0,200],[0,"n",800,250,True],
                               [20,0],  [0,50], [0,100],[0,150],[0,200],[0,"n",800,250,True],
                               [20,200],[0,150],[0,100],[0,"g",800,320,True],[0,"n",800,250,True],
                               [20,200],[0,"n",800,250,True],
                               [20,200],[0,"n",800,250,True],
                               [20,200],[0,"n",800,250,True],
                               [20,200],[0,"g",800,320,True],[0,"n",800,250,True],
                               [20,"n",800,250,True],[10,200],
                               [10,"n",800,250,True],[20,200],[0,"g",-200,350,False],
                               [0,"n",800,250,True],[20,"n",800,250,True],[20,"n",800,250,True],[10,200],
                               [10,"n",800,250,True],[20,"n",800,250,True],[20,"n",800,250,True],[0,100],
                               [20,"n",800,250,True],[20,"n",800,250,True],[10,150],
                               [10,"n",800,250,True],[0,"g",800,320,True],[20,"n",800,250,True],[20,"n",800,250,True],[0,200],
                               [20,"n",800,250,True],[20,"n",800,250,True],[10,150],
                               [10,"n",800,250,True],[0,"g",800,370,True],[10,150],[10,"n",800,250,True],[10,150],
                               [10,"n",800,250,True],[0,"g",800,320,True],
                               [20,"n",800,250,True],[0,"g",-200,350,False],
                               [20,"n",800,250,True],[0,"n",800,200,True],[0,"g",-200,350,False],
                               [20,"n",800,250,True],[0,"n",800,200,True],[0,"n",800,150,True],
                               [20,"n",800,250,True],[0,"n",800,200,True],[0,"n",800,150,True],[0,"n",800,100,True],[0,"g",-200,350,False],
                               [20,"n",800,250,True],[0,"g",800,320,True],[0,"n",800,200,True],[0,"n",800,150,True],[0,"n",800,100,True],[0,"n",800,50,True],
                               # ボス
                               [500,"b"],
                               [40,"g",800,320,True],[40,"g",-200,400,False],[40,"g",800,320,True],[40,"g",-200,400,False],
                               [40,"g",800,320,True],[40,"g",-200,400,False],[40,"g",800,320,True],[40,"g",-200,400,False],
                               [40,"g",800,320,True],[40,"g",-200,400,False],[40,"g",800,320,True],[40,"g",-200,400,False],
                               [40,"g",800,320,True],[40,"g",-200,400,False],[40,"g",800,320,True],[40,"g",-200,400,False],
                               [40,"g",800,320,True],[40,"g",-200,400,False],[40,"g",800,320,True],[40,"g",-200,400,False],
                               [40,"g",800,320,True],[40,"g",-200,400,False],[40,"g",800,320,True],[40,"g",-200,400,False],
                               [40,"g",800,320,True],[40,"g",-200,400,False],[40,"g",800,320,True],[40,"g",-200,400,False],
                               [40,"g",800,320,True],[40,"g",-200,400,False],[40,"g",800,320,True],[40,"g",-200,400,False],
                               [40,"g",800,320,True],[40,"g",-200,400,False],[40,"g",800,320,True],[40,"g",-200,400,False],
                               [40,"g",800,320,True],[40,"g",-200,400,False],[40,"g",800,320,True],[40,"g",-200,400,False],
                               [40,"g",800,320,True],[40,"g",-200,400,False],[40,"g",800,320,True],[40,"g",-200,400,False],
                               [40,"g",800,320,True],[40,"g",-200,400,False],[40,"g",800,320,True],[40,"g",-200,400,False],
                               [40,"g",800,320,True],[40,"g",-200,400,False],[40,"g",800,320,True],[40,"g",-200,400,False],
                               [40,"g",800,320,True],[40,"g",-200,400,False],[40,"g",800,320,True],[40,"g",-200,400,False],
                               [40,"g",800,320,True],[40,"g",-200,400,False],[40,"g",800,320,True],[40,"g",-200,400,False],
                               [340,"r"]] # 2800F後に終わる

        for n in range(1,len(self.enemy_and_time)):
            self.enemy_and_time[n][0] += self.enemy_and_time[n-1][0]

    def process(self,inpt):
        pass
    
    def update(self,):
        self.count += 1
        for comp in self.enemy_and_time:
            if comp[0] == self.count:
                if comp[1] == "n":
                    naitram = NormalEnemy(enmImgGrp,self.scn,[comp[2],comp[3]],(50,50),self.hero,comp[4])
                elif comp[1] == "a":
                    arim = Arim(arimImgGrp,self.scn,[comp[2],comp[3]],self.hero,comp[4])
                elif comp[1] == "t":
                    tallnaitram = TallEnemy(enmImgGrp,self.scn,[comp[2],comp[3]],(50,500),self.hero,comp[4])
                elif comp[1] == "g":
                    guin = Guin(self.scn,[comp[2],comp[3]],self.hero,comp[4])
                elif comp[1] == "s":
                    stuttle = Stuttle(self.scn,[comp[2],comp[3]],self.hero,comp[4])
                elif comp[1] == "b":
                    boss = Boss(self.scn,self.hero)
                elif comp[1] == "r":
                    rss = ResultSceneSwitcher(self.scn)
                else:
                    stuttle = Stuttle(self.scn,[800,comp[1]],self.hero,True)
                self.haveLaunchEnemy_s = True
            elif self.haveLaunchEnemy_s:
                self.haveLaunchEnemy_s = False
                break
    
    def render(self,):
        pass

class BossTstObj(GameObject):

    # 使わないで
    def __init__(self,imgGrp,scn,lyrNum,position):
        super().__init__(imgGrp,scn,lyrNum,position)
        self.count = 0

    def update(self,):
        if self.count <= 0:
            self.imgNum = 1
            self.position[0] -= 8
        if self.position[0] < -200:
            self.position[0] = 1000
        
        if 350 <= self.position[0] <= 357:
            if self.count <= 0:
                self.count = 50
                self.imgNum = 0
            else:
                self.count -= 1
