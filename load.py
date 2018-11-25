import pygame as pg
import os

titleBGImg = pg.image.load(os.path.join("images","titlebg.png")).convert()
titleImg1 = pg.image.load(os.path.join("images","titletostart.png")).convert_alpha()
titleImg2 = pg.image.load(os.path.join("images","titlenottostart.png")).convert_alpha()

pauseImg = pg.image.load(os.path.join("images","pause.png")).convert_alpha()

gameoverImg = pg.image.load(os.path.join("images","gameover.png")).convert_alpha()

# resultImg = pg.image.load(os.path.join("images","result.png")).convert()

bgImg = pg.image.load(os.path.join("images","background.png")).convert()
# heroImg = pg.image.load(os.path.join("images","testman.png")).convert_alpha()
# heroDmgdImg = heroImg.copy()
# heroDmgdImg.fill((0,100,100),special_flags=BLEND_SUB)
heroPhImg_L = pg.image.load(os.path.join("images","hero-phantom.png")).convert_alpha()
heroPhImg_R = pg.transform.flip(heroPhImg_L,True,False)

heroImg_L_standing = pg.image.load(os.path.join("images","hero_l_standing.png")).convert_alpha()
heroImg_L_running1 = pg.image.load(os.path.join("images","hero_l_running1.png")).convert_alpha()
heroImg_L_running2 = pg.image.load(os.path.join("images","hero_l_running2.png")).convert_alpha()
heroImg_L_running3 = pg.image.load(os.path.join("images","hero_l_running3.png")).convert_alpha()
heroImg_L_running4 = pg.image.load(os.path.join("images","hero_l_running4.png")).convert_alpha()
heroImg_L_jumpingA = pg.image.load(os.path.join("images","hero_l_jumpingA.png")).convert_alpha()
heroImg_L_jumpingB = pg.image.load(os.path.join("images","hero_l_jumpingB.png")).convert_alpha()
heroImg_L_jumpingC = pg.image.load(os.path.join("images","hero_l_jumpingC.png")).convert_alpha()
heroImg_L_dashing1 = pg.image.load(os.path.join("images","hero_l_dashing1.png")).convert_alpha()
heroImg_L_dashing2 = pg.image.load(os.path.join("images","hero_l_dashing2.png")).convert_alpha()
heroImg_L_digging1 = pg.image.load(os.path.join("images","hero_l_digging1.png")).convert_alpha()
heroImg_L_digging2 = pg.image.load(os.path.join("images","hero_l_digging2.png")).convert_alpha()
heroImg_L_digging3 = pg.image.load(os.path.join("images","hero_l_digging3.png")).convert_alpha()

heroDashImg_L = pg.image.load(os.path.join("images","dasheffect.png")).convert_alpha()
heroDashImg_R = pg.transform.flip(heroDashImg_L,True,False)

heroHoleImg = pg.image.load(os.path.join("images","herohole.png")).convert_alpha()

enemyImg1 = pg.image.load(os.path.join("images","naitram1.png")).convert_alpha()
enemyImg2 = pg.image.load(os.path.join("images","naitram2.png")).convert_alpha()
enemyImg3 = pg.image.load(os.path.join("images","naitram3.png")).convert_alpha()
enemyImg4 = pg.image.load(os.path.join("images","naitram4.png")).convert_alpha()
enemyImg = pg.image.load(os.path.join("images","naitram.png")).convert_alpha()
hpImg1a = pg.image.load(os.path.join("images","hpgauge1a.png")).convert_alpha()
hpImg1b = pg.image.load(os.path.join("images","hpgauge1b.png")).convert_alpha()
hpImg2a = pg.image.load(os.path.join("images","hpgauge2a.png")).convert_alpha()
hpImg2b = pg.image.load(os.path.join("images","hpgauge2b.png")).convert_alpha()
hpImg3a = pg.image.load(os.path.join("images","hpgauge3a.png")).convert_alpha()
hpImg3b = pg.image.load(os.path.join("images","hpgauge3b.png")).convert_alpha()
hpImg4a = pg.image.load(os.path.join("images","hpgauge4a.png")).convert_alpha()
hpImg4b = pg.image.load(os.path.join("images","hpgauge4b.png")).convert_alpha()

arimImg0 = pg.image.load(os.path.join("images","arim-l-1.png")).convert_alpha()
arimImg1 = pg.image.load(os.path.join("images","arim-l-2.png")).convert_alpha()
arimImg2 = pg.image.load(os.path.join("images","arim-l-3.png")).convert_alpha()
arimImg3 = pg.image.load(os.path.join("images","arim-l-4.png")).convert_alpha()
arimImg4 = pg.image.load(os.path.join("images","arim-l-5.png")).convert_alpha()
arimImg5 = pg.image.load(os.path.join("images","arim-r-1.png")).convert_alpha()
arimImg6 = pg.image.load(os.path.join("images","arim-r-2.png")).convert_alpha()
arimImg7 = pg.image.load(os.path.join("images","arim-r-3.png")).convert_alpha()
arimImg8 = pg.image.load(os.path.join("images","arim-r-4.png")).convert_alpha()
arimImg9 = pg.image.load(os.path.join("images","arim-r-5.png")).convert_alpha()
arimFireImgS = pg.image.load(os.path.join("images","arimb-s.png")).convert_alpha()
arimFireImgM = pg.image.load(os.path.join("images","arimb-m.png")).convert_alpha()
arimFireImgL = pg.image.load(os.path.join("images","arimb-l.png")).convert_alpha()

guinImg1 = pg.image.load(os.path.join("images","guin1.png")).convert_alpha()
guinImg2 = pg.image.load(os.path.join("images","guin2.png")).convert_alpha()
guinImg3 = pg.image.load(os.path.join("images","guin3.png")).convert_alpha()
guinImg4 = pg.image.load(os.path.join("images","guin4.png")).convert_alpha()
guinImg5 = pg.image.load(os.path.join("images","guin5.png")).convert_alpha()
guinImg6 = pg.image.load(os.path.join("images","guin6.png")).convert_alpha()
guinImg7 = pg.image.load(os.path.join("images","guin7.png")).convert_alpha()
guinImg8 = pg.image.load(os.path.join("images","guin8.png")).convert_alpha()

resultbgImg = pg.image.load(os.path.join("images","resultbg.png")).convert()
clearImg = pg.image.load(os.path.join("images","clear.png")).convert_alpha()
congratsImg = pg.image.load(os.path.join("images","congratulations.png")).convert_alpha()
totitleImg = pg.image.load(os.path.join("images","resulttotitle.png")).convert_alpha()
cometImg = pg.image.load(os.path.join("images","comet.png")).convert_alpha()

bosstestImg = pg.image.load(os.path.join("images","boss_l_1.png")).convert_alpha()
bosstestImg2 = pg.image.load(os.path.join("images","boss_l_2.png")).convert_alpha()

bossImg_l_1 = bosstestImg
bossImg_l_2 = bosstestImg2
bossImg_r_1 = pg.image.load(os.path.join("images","boss_r_1.png")).convert_alpha()
bossImg_r_2 = pg.image.load(os.path.join("images","boss_r_2.png")).convert_alpha()
bossImg_b_1 = pg.image.load(os.path.join("images","boss_b_1.png")).convert_alpha()
bossImg_b_2 = pg.image.load(os.path.join("images","boss_b_2.png")).convert_alpha()
bossImg_b_3 = pg.image.load(os.path.join("images","boss_b_3.png")).convert_alpha()
bossImg_s_1 = pg.image.load(os.path.join("images","boss_s_1.png")).convert_alpha()
bossImg_s_2 = pg.image.load(os.path.join("images","boss_s_2.png")).convert_alpha()
bossImg_s_3 = pg.image.load(os.path.join("images","boss_s_3.png")).convert_alpha()
bossImg_s_4 = pg.image.load(os.path.join("images","boss_s_4.png")).convert_alpha()
bossImg_d_1 = pg.image.load(os.path.join("images","boss_d_1.png")).convert_alpha()
bossImg_d_2 = pg.image.load(os.path.join("images","boss_d_2.png")).convert_alpha()

stlImg1,stlImg2,stlImg3,stlImg4,stlImg5,stlImg6 = pg.image.load(os.path.join("images","shuttle1.png")).convert_alpha(),\
pg.image.load(os.path.join("images","shuttle2.png")).convert_alpha(),pg.image.load(os.path.join("images","shuttle3.png")).convert_alpha(),\
pg.image.load(os.path.join("images","shuttle4.png")).convert_alpha(),pg.image.load(os.path.join("images","shuttle5.png")).convert_alpha(),\
pg.image.load(os.path.join("images","shuttle6.png")).convert_alpha()