import pygame as pg
from load import *
import screen

class ImageGroup():
    def __init__(self,imgs,scrn):
        self.imgs = imgs # 画像のリスト
        self.length = len(imgs)
        self.scrn = scrn

phantomIMG = ImageGroup([heroPhImg_L,heroPhImg_R],screen.screen)
gmovImgGrp = ImageGroup([gameoverImg],screen.screen)
# resultImgGrp = ImageGroup([resultImg],screen.screen)
hpImgs = [hpImg1a,hpImg1b,hpImg2a,hpImg2b,hpImg3a,hpImg3b,hpImg4a,hpImg4b]
bgImgGrp = ImageGroup([bgImg],screen.screen)
heroImgGrp = ImageGroup([heroImg_L_standing,heroImg_L_running1,heroImg_L_running2,\
                         heroImg_L_running3,heroImg_L_running4,heroImg_L_jumpingA,\
                         heroImg_L_jumpingB,heroImg_L_jumpingC,heroImg_L_dashing1,\
                         heroImg_L_dashing2,heroImg_L_digging1,heroImg_L_digging2,\
                         heroImg_L_digging3],\
                         screen.screen)
for im in heroImgGrp.imgs[:]:
    heroImgGrp.imgs.append(pg.transform.flip(im,True,False))

HPImgGrp = ImageGroup(hpImgs,screen.screen)
enmImgGrp = ImageGroup([enemyImg1,enemyImg2,enemyImg3,enemyImg4],screen.screen)
for im in enmImgGrp.imgs[:]:
    enmImgGrp.imgs.append(pg.transform.flip(im,True,False))
arimImgGrp = ImageGroup([arimImg0,arimImg1,arimImg2,arimImg3,arimImg4,arimImg5,\
                                           arimImg6,arimImg7,arimImg8,arimImg9,\
                                           arimFireImgS,arimFireImgM,arimFireImgL],\
                                           screen.screen)
guinImgGrp = ImageGroup([guinImg1,guinImg2,guinImg3,guinImg4,guinImg5,guinImg6,guinImg7,guinImg8],screen.screen)
for im in guinImgGrp.imgs[:]:
    guinImgGrp.imgs.append(pg.transform.flip(im,True,False))
titleBGImgGrp = ImageGroup([titleBGImg],screen.screen)
titleImgGrp = ImageGroup([titleImg1,titleImg2],screen.screen)
bossImgGrp = ImageGroup([bossImg_l_1,bossImg_l_2,
                         bossImg_r_1,bossImg_r_2,
                         bossImg_b_1,bossImg_b_2,bossImg_b_3,
                         bossImg_s_1,bossImg_s_2,bossImg_s_3,bossImg_s_4,
                         bossImg_d_1,bossImg_d_2],screen.screen)

resultBGImgGrp = ImageGroup([resultbgImg],screen.screen)
cometImgGrp = ImageGroup([cometImg],screen.screen)
resultStrImgGrp = ImageGroup([clearImg,congratsImg,totitleImg],screen.screen)

bossTstImgGrp = ImageGroup([bosstestImg,bosstestImg2],screen.screen)

stuttleImgGrp = ImageGroup([stlImg1,stlImg2,stlImg3,stlImg4,stlImg5,stlImg6],screen.screen)
for im in stuttleImgGrp.imgs[:]:
    stuttleImgGrp.imgs.append(pg.transform.flip(im,True,False))