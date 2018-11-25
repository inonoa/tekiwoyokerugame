import pygame as pg

js_plugged = False

try:
    j = pg.joystick.Joystick(0) # create a joystick instance
    j.init() # init instance
    print('Joystickの名称: ' + j.get_name())
    print('ボタン数 : ' + str(j.get_numbuttons()))
    js_plugged = True
except pg.error:
    print('Joystickが見つかりませんでした。')

def right():
    if js_plugged:
        return j.get_axis(0) > 0.5

def left():
    if js_plugged:
        return j.get_axis(0) < -0.5

def up():
    if js_plugged:
        return j.get_axis(1) < -0.5

def down():
    if js_plugged:
        return j.get_axis(1) > 0.5