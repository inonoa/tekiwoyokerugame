import pygame as pg
import os

pg.mixer.pre_init(44100, 16, 2, 512)
pg.init()

jumpsound = pg.mixer.Sound(os.path.join("musics_and_sounds","se_maoudamashii_se_sound17.wav"))
typesound = pg.mixer.Sound(os.path.join("musics_and_sounds","se_maoudamashii_se_pc03.wav"))
oksound = pg.mixer.Sound(os.path.join("musics_and_sounds","se_maoudamashii_system48.wav"))
dashsound = pg.mixer.Sound(os.path.join("musics_and_sounds","se_maoudamashii_retro11.wav"))
beamsound = pg.mixer.Sound(os.path.join("musics_and_sounds","se_maoudamashii_retro01_small.wav"))

pg.mixer.music.load(os.path.join("musics_and_sounds","走って跳んで掘って避けて.ogg"))
pg.mixer.music.set_volume(0.7)