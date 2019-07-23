import pygame as pg

#Needs to be called before import homemade modules
pg.init()

from objects.Display import Display
from objects.Window import Window
from objects.Button import Button, TextField
import numpy as np
import sys

img_path = "images/"

width, height = (1420, 1050)
window = Window((width, height))
pg.event.set_blocked(pg.MOUSEMOTION)
img = pg.image.load(img_path + 'logo.png')

window.window.blit(img,(width/2-300,height/2-300))
pg.display.flip()

# Main interactive display
d = Display((50,50), 30, num_x=19, num_y=10)
window.add_element(d, "Display")

"""
for i in range(6):
    frames.append(Display((80+i*180,860), 3, num_x=19, num_y=10, boarder=2, simple=True))
    window.add_element(frames[-1], "D{}".format(i))
frames[0].toggle_mark()

# Buttons
def b1_func():
    global current_frame
    frames[current_frame].load_frame(d.get_frame())
b1 = Button((50,810), 0, b1_func , text="Add frame", fit_text=True)
window.add_element(b1, "add frame button")

def b2_func():
    global current_frame
    d.clear_frame()
b2 = Button((300,810), 0, b2_func, text="Clear frame", fit_text=True)
window.add_element(b2, "clear frame button")

def b3_func():
    global current_frame
    current_frame = current_frame + 1
b3 = Button((650, 805), (50,50), b3_func, text=" + ", fit_text=False)
window.add_element(b3, "next frame button")

def b4_func():
    global current_frame
    if current_frame > 0: 
        current_frame = current_frame - 1
b4 = Button((710, 805), (50,50), b4_func, text="  - ", fit_text=False)
window.add_element(b4, "prev frame button")

def write_frames_to_file(filename):
    with open(filename, "w") as fp:
        for frame in frames:
            #fp.write(frame)
            pass

b5 = Button((810, 805), 0, write_frames_to_file("test.fetch"), text="Save", fit_text=True)
window.add_element(b5, "Save animation")
"""
#-----------------------------------------------------------------------------------------#
#-----------------------------------------BUTTONS-----------------------------------------#
#-----------------------------------------------------------------------------------------#

def func_cls_button():
    return
cls_button = Button((50,900), 0, func_cls_button , text="CLS", fit_text=True)
window.add_element(cls_button, "cls_button")

def func_cpy_button():
    return
cpy_button = Button((50,950), 0, func_cpy_button , text="CPY", fit_text=True)
window.add_element(cpy_button, "cpy_button")

def func_del_button():
    return
del_button = Button((50,1000), 0, func_del_button , text="DEL", fit_text=True)
window.add_element(del_button, "del_button")

def func_move_frame_right_button():
    return
move_frame_right_button = Button((440,900), 0, func_move_frame_right_button , text="<--", fit_text=True)
window.add_element(move_frame_right_button, "move_frame_right_button")

def func_move_mark_right_button():
    return
move_mark_right_button = Button((500,900), 0, func_move_mark_right_button , text=" <-", fit_text=True)
window.add_element(move_mark_right_button, "move_mark_right_button")

def func_add_frame_button():
    return
add_left_button = Button((560,900), 0, func_add_frame_button , text=" + ", fit_text=True)
window.add_element(add_left_button, "add_left_button")

def func_move_mark_left_button():
    return
move_mark_left_button = Button((620,900), 0, func_move_mark_left_button , text="-> ", fit_text=True)
window.add_element(move_mark_left_button, "move_mark_Left_button")

def func_move_frame_left_button():
    return
move_frame_left_button = Button((680,900), 0, func_move_frame_left_button , text="-->", fit_text=True)
window.add_element(move_frame_left_button, "move_frame_Left_button")

def func_set_pixel_value_button():
    return
set_pixel_value_button = Button((450,950), 0, func_set_pixel_value_button , text="VAL", fit_text=True)
window.add_element(set_pixel_value_button, "set_pixel_value_button")

def func_apply_frame_button():
    return
apply_frame_button = Button((540,950), 0, func_apply_frame_button , text="ADD", fit_text=True)
window.add_element(apply_frame_button, "apply_frame_button")

def func_mark_pixel_button():
    return
mark_pixel_button = Button((640,950), 0, func_mark_pixel_button , text="SEL", fit_text=True)
window.add_element(mark_pixel_button, "mark_pixel_button")


def func_play_button():
    return
play_button = Button((1000,900), 0, func_play_button , text="PLAY", fit_text=True)
window.add_element(play_button, "play_button")

def func_load_button():
    return
load_button = Button((1000,950), 0, func_load_button , text="LOAD", fit_text=True)
window.add_element(load_button, "load_button")

def func_save_button():
    return
save_button = Button((1000,1000), 0, func_save_button , text="SAVE", fit_text=True)
window.add_element(save_button, "save_button")

#-----------------------------------------------------------------------------------------#
#---------------------------------------TEXT FIELDS---------------------------------------#
#-----------------------------------------------------------------------------------------#

def func_pwm_text_field():
    return
pwm_text_field = TextField((540,1000), 0, func_pwm_text_field , text="PWM", fit_text=True)
window.add_element(pwm_text_field, "pwm_text_field")

#-----------------------------------------------------------------------------------------#
#-----------------------------------------FRAMES------------------------------------------#
#-----------------------------------------------------------------------------------------#

frames = []
current_frame = 0
frames.append(Display((100,700), 3, num_x=19, num_y=10, boarder=2, simple=True))
window.add_element(frames[-1], "D{}".format(0))

#-----------------------------------------------------------------------------------------#
#---------------------------------------MAIN LOOP-----------------------------------------#
#-----------------------------------------------------------------------------------------#
window.window.fill(np.array([255,255,255])/2)
window.update()
while True:
    #Wait for input
    e = pg.event.wait()
    
    #Events
    pg.event.pump()
    key_events = pg.key.get_pressed()
    mouse_events = pg.mouse.get_pressed()

    #Push events to window
    window.handle_events(key_events, mouse_events)
    window.update()

    #Exit condition
    if e.type == pg.QUIT:
        pg.display.quit()
        pg.quit()
        sys.exit()