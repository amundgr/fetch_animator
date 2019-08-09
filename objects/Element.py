import pygame as pg

class Element():
    def __init__(self, pos, sensetivity="NONE"):
        self.pos = pos
        self.changed = True
        self.sensetivity = sensetivity
        self.window = None

    def set_window(self, window):
        self.window = window

    def update(self):
        if self.changed:
            self.changed = False
            self.draw()

    def draw(self):
        pass

    def delete(self):
        pass

    