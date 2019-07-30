import pygame as pg
import numpy as np
import sys

#Needs to be called before import homemade modules
pg.init()

from objects.Display import Display, DummyDisplay
from objects.Window import Window
from objects.Button import Button, TextField
from objects.Element import Element

img_path = "images/"

width, height = (1420, 1050)
num_x = 19
num_y = 10
animation = []
mini_displays = []
frame_numbers = []
current_frame = 0
current_display = 0
num_mini_displays = 7

window = Window((width, height))
pg.event.set_blocked(pg.MOUSEMOTION)
img = pg.image.load(img_path + 'logo.png')

window.window.blit(img,(width/2-300,height/2-300))
pg.display.flip()


def get_frame_slice():
    global current_frame, num_mini_displays, animation, current_display
    if current_frame < num_mini_displays / 2:
        current_display = current_frame
        print("first", current_display)
        return range(num_mini_displays)
    elif current_frame > len(animation) - num_mini_displays / 2 - 1:
        current_display = (num_mini_displays - 1) - (len(animation) - 1 - current_frame)
        if current_display >= num_mini_displays:
            current_display = num_mini_displays - 1
        print("second", current_display)
        return range(len(animation)-num_mini_displays, len(animation))
    else:
        current_display = round(num_mini_displays/2)-1
        print("last", current_display)
        return range(current_frame - num_mini_displays // 2, current_frame + num_mini_displays // 2 + 1)

def update_mini_display():
    for md, fn, idx in zip(mini_displays, frame_numbers, get_frame_slice()):
        md.load_frame(animation[idx])
        fn.change_text("{}".format(idx+1))
        fn.infill_color = [200, 200, 200]
    frame_numbers[current_display].infill_color = [100,100,100]

#-----------------------------------------------------------------------------------------#
#-----------------------------------------BUTTONS-----------------------------------------#
#-----------------------------------------------------------------------------------------#

def func_cls_button():
    main_display.clear_frame()
    return
cls_button = Button((50,900), 0, func_cls_button , text="CLS", fit_text=True)
window.add_element(cls_button, "cls_button")

def func_cpy_button():
    main_display.load_frame(animation[current_frame])
    return
cpy_button = Button((50,950), 0, func_cpy_button , text="CPY", fit_text=True)
window.add_element(cpy_button, "cpy_button")

def func_del_button():
    global animation, current_frame, num_mini_displays, num_x, num_y
    if len(animation) == num_mini_displays:
        animation[current_frame] = np.zeros((num_x, num_y))
    else:
        del animation[current_frame]
    if current_frame > 0:
        current_frame -= 1
    update_mini_display()
    return
del_button = Button((50,1000), 0, func_del_button , text="DEL", fit_text=True)
window.add_element(del_button, "del_button")

def func_move_frame_right_button():
    return
move_frame_right_button = Button((440,900), 0, func_move_frame_right_button , text="<--", fit_text=True)
window.add_element(move_frame_right_button, "move_frame_right_button")

def func_move_mark_right_button():
    global current_frame
    if current_frame > 0:
        current_frame -= 1
        update_mini_display()
    return
move_mark_right_button = Button((500,900), 0, func_move_mark_right_button , text=" <-", fit_text=True)
window.add_element(move_mark_right_button, "move_mark_right_button")

def func_add_frame_button():
    global num_x, num_y, current_frame
    if current_frame < num_mini_displays:
        current_frame += 1
    else:
        current_frame += 1
        animation.insert(current_frame, np.zeros((num_x, num_y)))
    print(len(animation))

    update_mini_display()
    return
add_left_button = Button((560,900), 0, func_add_frame_button , text=" + ", fit_text=True)
window.add_element(add_left_button, "add_left_button")

def func_move_mark_left_button():
    global current_frame, animation
    if current_frame < len(animation)-1:
        current_frame += 1
        update_mini_display()
    return
move_mark_left_button = Button((620,900), 0, func_move_mark_left_button , text="-> ", fit_text=True)
window.add_element(move_mark_left_button, "move_mark_Left_button")

def func_move_frame_left_button():
    return
move_frame_left_button = Button((680,900), 0, func_move_frame_left_button , text="-->", fit_text=True)
window.add_element(move_frame_left_button, "move_frame_Left_button")
"""
def func_set_pixel_value_button():
    return
set_pixel_value_button = Button((450,950), 0, func_set_pixel_value_button , text="VAL", fit_text=True, toggle=True)
window.add_element(set_pixel_value_button, "set_pixel_value_button")
"""
def func_apply_frame_button():
    animation[current_frame] = main_display.get_frame()
    mini_displays[current_display].load_frame(animation[current_frame])
    return
apply_frame_button = Button((540,950), 0, func_apply_frame_button , text="ADD", fit_text=True)
window.add_element(apply_frame_button, "apply_frame_button")
"""
def func_mark_pixel_button():
    return
mark_pixel_button = Button((640,950), 0, func_mark_pixel_button , text="SEL", fit_text=True, toggle=True)
mark_pixel_button.set_pair_button(set_pixel_value_button)
set_pixel_value_button.set_pair_button(mark_pixel_button)
window.add_element(mark_pixel_button, "mark_pixel_button")
"""
def func_play_button(time=500):
    global main_display, animation, current_frame, window
    for i in range(len(animation)):
        current_frame = i
        main_display.load_frame(animation[i])
        update_mini_display()
        window.update()
        pg.time.wait(time)
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

for i in range(7):
    mini_displays.append(DummyDisplay((55+i*170,700), 3, num_x=19, num_y=10, boarder=2))
    frame_numbers.append(TextField((105+i*170,800), (60,40), text="{}".format(i+1), fit_text=False, sensetivity=[]))
    window.add_element(mini_displays[-1], "D{}".format(i))
    window.add_element(frame_numbers[-1], "N{}".format(i+1))
    animation.append(mini_displays[-1].get_frame())

#-----------------------------------------------------------------------------------------#
#--------------------------------------MAIN DISPLAY---------------------------------------#
#-----------------------------------------------------------------------------------------#

main_display = Display((50,50), 30, num_x=num_x, num_y=num_y, value_label=pwm_text_field)
window.add_element(main_display, "Display")

#-----------------------------------------------------------------------------------------#
#---------------------------------------MAIN LOOP-----------------------------------------#
#-----------------------------------------------------------------------------------------#

window.window.fill(np.array([255,255,255])/2)
update_mini_display()
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