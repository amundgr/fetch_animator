import pygame as pg

#Needs to be called before import homemade modules
pg.init()

from objects.Display import Display
from objects.Window import Window
from objects.Button import Button
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
frames = []
current_frame = 0


for i in range(6):
    frames.append(Display((80+i*180,860), 3, num_x=19, num_y=10, boarder=2, sensetivity="NONE", simple=True))
    window.add_element(frames[-1], "D{}".format(i))

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