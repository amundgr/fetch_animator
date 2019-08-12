import pygame as pg
import numpy as np
import copy as cp
import sys

#Needs to be called before import homemade modules
pg.init()

from objects.Display import Display, DummyDisplay
from objects.Window import Window
from objects.Button import Button, TextField
from objects.Element import Element

img_path = "images/"

width, height = (1600, 900)
num_x = 19
num_y = 10
animation = []
mini_displays = []
frame_numbers = []
current_frame = 0
current_display = 0
num_frames = 1
num_mini_displays = 7
num_active_mini_displays = 1

window = Window((width, height))
#pg.event.set_blocked(pg.MOUSEMOTION)
img = pg.image.load(img_path + 'logo.png')
window.window.fill((0,0,0))
window.window.blit(img,(width/2-300,height/2-300))
pg.display.flip()

def print_vitals():
    print("---------------------------------")
    print("Current Frame:", current_frame)
    print("Current Display:", current_display)
    print("Number of frames:", num_frames)
    print("Actual number of frames:", len(animation))
    print("Number of dispalys:", len(mini_displays))
    print("Number of active mini displays:", num_active_mini_displays)
    print("Frames displayed:", get_frame_slice())
    print("---------------------------------")
    print("Elements in window:", window.element_dict.keys())
    print("---------------------------------")
    for a in animation:
        print(a.transpose())
        print()
    print()

prev_click = 0
def prevent_double_click(timeout=5):
    global prev_click
    time_since_prev_click = pg.time.get_ticks() - prev_click
    if time_since_prev_click < timeout:
        return False
    else:
        return True

def get_frame_slice():
    global current_frame, num_mini_displays, animation, current_display
    if current_frame <= num_mini_displays / 2:
        current_display = current_frame
        return range(num_mini_displays)
    elif current_frame > len(animation) - num_mini_displays / 2 - 1:
        current_display = (num_mini_displays - 1) - (len(animation) - 1 - current_frame)
        if current_display >= num_mini_displays:
            current_display = num_mini_displays - 1
        return range(len(animation)-num_mini_displays, len(animation))
    else:
        current_display = round(num_mini_displays/2)-1
        return range(current_frame - num_mini_displays // 2, current_frame + num_mini_displays // 2 + 1)

def update_mini_display():
    for md, fn, idx in zip(mini_displays, frame_numbers, get_frame_slice()):
        md.load_frame(animation[idx])
        fn.change_text("{}".format(idx+1))
        fn.infill_color = [200, 200, 200]
    frame_numbers[current_display].infill_color = [100,100,100]
    for i, a in enumerate(animation):
        if np.sum(a) > 0:
            print(i)

#-----------------------------------------------------------------------------------------#
#-----------------------------------------BUTTONS-----------------------------------------#
#-----------------------------------------------------------------------------------------#

def func_cls_button():
    main_display.clear_frame()
    return
cls_button = Button((1270,600), 0, func_cls_button , text="CLS", fit_text=True)
window.add_element(cls_button, "cls_button")

def func_cpy_button():
    main_display.load_frame(animation[current_frame])
    return
cpy_button = Button((1370,600), 0, func_cpy_button , text="CPY", fit_text=True)
window.add_element(cpy_button, "cpy_button")

def func_del_button():
    global animation, current_frame, num_mini_displays, num_x, num_y, num_active_mini_displays, window, num_active_mini_displays, num_frames
    if num_frames == 1:
        animation[0] = np.zeros((num_x, num_y))
    
    elif num_frames <= num_mini_displays:
        animation.pop(current_display)
        animation.append(np.zeros((num_x, num_y)))
        window.disable_element("N{}".format(num_active_mini_displays))
        num_active_mini_displays -= 1
        #animation[current_frame] = np.zeros((num_x, num_y))

    else:
        animation.pop(current_frame)

    if current_frame == num_frames - 1 and not current_frame == 0:
        current_frame -= 1

    if num_frames > 1:
        num_frames -= 1

    update_mini_display()
    window.update()
    return
del_button = Button((1470,600), 0, func_del_button , text="DEL", fit_text=True)
window.add_element(del_button, "del_button")


def func_move_mark_right_button():
    global current_frame
    if current_frame > 0:
        current_frame -= 1
        update_mini_display()
    return
move_mark_right_button = Button((1300,300), 0, func_move_mark_right_button , text="  <- ", fit_text=True)
window.add_element(move_mark_right_button, "move_mark_right_button")

def func_add_frame_button():
    global num_x, num_y, current_frame, num_active_mini_displays, num_frames
    if prevent_double_click:
        if num_active_mini_displays < num_mini_displays:
            num_active_mini_displays += 1
            inc = num_active_mini_displays - 1
            window.enable_element("N{}".format(inc+1))
        else:
            animation.insert(current_frame+1, np.zeros((num_x, num_y)))

        current_frame += 1
        num_frames += 1
        update_mini_display()
    return
add_left_button = Button((1380,300), 0, func_add_frame_button , text="  +  ", fit_text=True)
window.add_element(add_left_button, "add_left_button")

def func_move_mark_left_button():
    global current_frame, animation, num_active_mini_displays, num_frames
    if current_frame < num_frames-1:
        current_frame += 1
        update_mini_display()
    return
move_mark_left_button = Button((1460,300), 0, func_move_mark_left_button , text=" ->  ", fit_text=True)
window.add_element(move_mark_left_button, "move_mark_Left_button")


def func_apply_frame_button():
    animation[current_frame] = main_display.get_frame()
    mini_displays[current_display].load_frame(animation[current_frame])
    return
apply_frame_button = Button((1340,350), 0, func_apply_frame_button , text="ADD", fit_text=True)
window.add_element(apply_frame_button, "apply_frame_button")


def func_play_button(time=200):
    global main_display, animation, current_frame, window, num_frames
    main_display.clear_frame()
    window.update()
    tmp_current_frame = current_frame
    print(tmp_current_frame)
    for i in range(num_frames):
        current_frame = i
        main_display.load_frame(animation[i])
        update_mini_display()
        window.update()
        pg.time.wait(time)
    main_display.clear_frame()
    print(tmp_current_frame)
    current_frame = tmp_current_frame
    main_display.load_frame(animation[current_frame])
    window.update()
    return
play_button = Button((1250,50), 0, func_play_button , text="PLAY", fit_text=True)
window.add_element(play_button, "play_button")

def func_load_button():
    return
load_button = Button((1360,50), 0, func_load_button , text="LOAD", fit_text=True)
window.add_element(load_button, "load_button")

def func_save_button(outfile="out"):
    global num_frames, num_x, num_y, animation
    pwm_frames = []
    with open("{}.bin".format(outfile), "wb") as fp:
        for i in range(num_frames):
            frame = cp.deepcopy(animation[i])
            frame = frame.transpose()
            print(frame.shape)
            frame = np.flip(frame, 0)
            binary_factors = 2**np.linspace(0,num_y, num_y+1)[0:-1]
    
            binary_frame_matrix = (frame > 0)
            binary_frame_array = np.sum(binary_frame_matrix * binary_factors.reshape(-1,1), 0)
            binary_frame_array_uint32 = np.uint32(binary_frame_array.astype(int))
    
            frame[frame == 0] = 20
            pwm_frame_uint8 = np.uint8(frame)
            
            fp.write(bytes(binary_frame_array_uint32))
            pwm_frames.append(pwm_frame_uint8)
    
        for pwm_frame in pwm_frames:
            fp.write(bytes(pwm_frame))

    with open("{}.txt".format(outfile), "w") as fp:
        fp.write("{},{},{},0,0,1,0,-1,0,-1,0".format(num_x, num_y, num_frames))
    return

save_button = Button((1480,50), 0, func_save_button , text="SAVE", fit_text=True)
window.add_element(save_button, "save_button")

#-----------------------------------------------------------------------------------------#
#---------------------------------------TEXT FIELDS---------------------------------------#
#-----------------------------------------------------------------------------------------#

def func_pwm_text_field():
    return
pwm_text_field = TextField((1440,350), 0, func_pwm_text_field , text="19", fit_text=True)
window.add_element(pwm_text_field, "pwm_text_field")

#-----------------------------------------------------------------------------------------#
#-----------------------------------------FRAMES------------------------------------------#
#-----------------------------------------------------------------------------------------#

for i in range(7):
    mini_displays.append(DummyDisplay((55+i*170,700), 3, num_x=19, num_y=10, boarder=2))
    window.add_element(mini_displays[-1], "D{}".format(i))
    animation.append(mini_displays[-1].get_frame())
    frame_numbers.append(TextField((105+i*170,800), (60,40), text="{}".format(i+1), fit_text=False, sensetivity=[]))
    window.add_element(frame_numbers[i], "N{}".format(i+1))
    if i > 0:
        window.disable_element("N{}".format(i+1))

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
try:
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

finally:
    func_save_button(outfile="backup")
    #print_vitals()