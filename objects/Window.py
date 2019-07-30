import pygame as pg
import numpy as np

black = np.array([  0,   0,   0])
white = np.array([255, 255, 255])
red   = np.array([255,   0,   0])
green = np.array([  0, 255,   0])
blue  = np.array([  0,   0, 255])

class Window():
    def __init__(self, size, background=black):
        self.height, self.width = size
        self.background = white/2
        self.window = pg.display.set_mode(size)
        self.window.fill(background)
        self.sensetivity_dict = {"MOUSE":[], "KEY":[], "NONE":[]}
        self.element_dict = {}

    def handle_events(self, key_event, mouse_event):
        if np.sum(mouse_event):
            for name_tag in self.sensetivity_dict["MOUSE"]:
                pos = pg.mouse.get_pos()
                self.element_dict[name_tag].handle_event(mouse_event=mouse_event, pos=pos)

        if np.sum(key_event):
            for name_tag in self.sensetivity_dict["KEY"]:
                self.element_dict[name_tag].handle_event(key_event=key_event)

    def update(self):
        for name_tag in self.element_dict:
            self.element_dict[name_tag].update()
        pg.display.flip()

    def add_element(self, element, name_tag):
        element.set_window(self.window)
        self.element_dict[name_tag] = element
        if not isinstance(element.sensetivity, list):
            element.sensetivity = [element.sensetivity]
        for sens in element.sensetivity:
            self.sensetivity_dict[sens].append(name_tag)
    
    def remove_element(self, name_tag):
        del self.element_dict[element_tag]