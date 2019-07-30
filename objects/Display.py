from .Element import Element
import pygame as pg
import numpy as np
import copy as cp

img_path = "images/"

#Color
black =   np.array([  0,   0,   0])
white =   np.array([255, 255, 255])
magenta = np.array([  0, 255, 255])
red =     np.array([255,   0,   0])
green =   np.array([  0, 255,   0])
blue =    np.array([  0,   0, 255])

#Fonts
font_size = 20
cs_font = pg.font.SysFont('Comic Sans MS', font_size)
arial_font = pg.font.SysFont('Arial', font_size)

class Display(Element):
    def __init__(self, pos, radius, num_x=10, num_y=10, spacing=2, boarder=5, sensetivity="MOUSE", value_label=None, pwm_button=None, select_button=None):
        Element.__init__(self, pos, sensetivity)
        self.pos_x, self.pos_y = self.pos
        self.radius = radius
        self.height = num_y*radius*2 + (num_y+3)*spacing
        self.width = num_x*radius*2 + (num_x+3)*spacing
        self.num_x = num_x
        self.num_y = num_y
        self.img_clean = pg.image.load(img_path + 'magnet_clean.png')
        self.img_clean = pg.transform.scale(self.img_clean, (self.radius*2,self.radius*2))
        self.img_occupied = pg.image.load(img_path + 'splash_clean.png')
        self.img_occupied = pg.transform.scale(self.img_occupied, (self.radius*2,self.radius*2))
        self.img = self.img_clean
        self.spacing = spacing
        self.boarder = boarder
        self.frame_rect = pg.Rect(self.pos_x, self.pos_y, 
                                  self.width, self.height)
     
        self.frame = np.zeros((num_x, num_y))
        self.frame_prev_state = np.ones((num_x, num_y))
        self.background = white / (3)
        self.frame_color = np.array([94,61,0])
        self.intensity = 255
        self.first = True
        self.value_label = value_label
        self.pwm_button = pwm_button
        self.select_button = select_button


    def draw(self):
        if self.first:
            pg.draw.rect(self.window, self.frame_color, self.frame_rect, self.boarder)
            pg.draw.rect(self.window, self.background, self.frame_rect)
            self.first = False

        idx_x_list, idx_y_list = np.where((self.frame == self.frame_prev_state) == False)
        for idx_x in idx_x_list:
            for idx_y in idx_y_list:    
                color = white - magenta * self.frame[idx_x, idx_y]  
                pos_x = self.pos_x + self.spacing*2  + idx_x * (self.radius*2 + self.spacing)
                pos_y = self.pos_y + self.spacing*2  + idx_y * (self.radius*2 + self.spacing)
                if self.frame[idx_x, idx_y] > 0:
                    self.window.blit(self.img_occupied, (pos_x, pos_y))
                    self.myfont = arial_font.render("{0:.0f}".format(self.frame[idx_x, idx_y]), False, white)
                    pos_x_text, pos_y_text = np.array([pos_x, pos_y]) + self.radius - np.array(self.myfont.get_size())/2
                    self.window.blit(self.myfont, (pos_x_text, pos_y_text))
                else:
                    self.window.blit(self.img_clean, (pos_x, pos_y))
        self.frame_prev_state = cp.deepcopy(self.frame)

    def handle_event(self, **kwargs):
        mouse_event = kwargs["mouse_event"]
        if mouse_event[0] and self.frame_rect.collidepoint(kwargs["pos"]):
            pos_x, pos_y = kwargs["pos"]
            idx_x = (pos_x - self.pos_x - self.spacing) // (self.radius*2 + self.spacing) 
            idx_y = (pos_y - self.pos_y - self.spacing) // (self.radius*2 + self.spacing)
            if self.value_label != None:
                self.intensity = int(self.value_label)
            if self.pwm_button != None:
                if self.frame[idx_x, idx_y] > 0:
                    self.frame[idx_x, idx_y] = self.intensity
            #if self.
            self.frame[idx_x, idx_y] = self.intensity
            self.changed = True
            
    def clear_frame(self):
        self.frame = self.frame*0
        self.changed = True

    def load_frame(self, frame):
        self.frame = cp.deepcopy(frame)
        self.frame_prev_state = np.zeros((self.num_x, self.num_y))
        self.changed = True

    def get_frame(self):
        return cp.deepcopy(self.frame)

class DummyDisplay(Display):
    def __init__(self, pos, radius, num_x=10, num_y=10, spacing=2, boarder=5, sensetivity="MOUSE", marked=False):
        Display.__init__(self, pos, radius, num_x, num_y, spacing, boarder, sensetivity)
        self.marked = marked
        self.changed = True

    def draw(self):
        pg.draw.rect(self.window, self.frame_color, self.frame_rect, self.boarder)
        pg.draw.rect(self.window, self.background, self.frame_rect)
        idx_x_list, idx_y_list = np.where((self.frame == self.frame_prev_state) == False)
        for idx_x in idx_x_list:
            for idx_y in idx_y_list:    
                if self.frame[idx_x, idx_y] > 0:
                    color = white - magenta * self.frame[idx_x, idx_y]  
                    pos_x = self.pos_x + self.spacing*2  + idx_x * (self.radius*2 + self.spacing)
                    pos_y = self.pos_y + self.spacing*2  + idx_y * (self.radius*2 + self.spacing)
                    self.window.blit(self.img_occupied, (pos_x, pos_y))
        self.frame_prev_state = cp.deepcopy(self.frame)

    def handle_event(self, **kwargs):
        mouse_event = kwargs["mouse_event"]
        if mouse_event[0] and self.frame_rect.collidepoint(kwargs["pos"]):
            self.marked = True
            self.changed = True

if __name__=="__main__":
    dd = DummyDisplay((1,1), 20)
    print(dd.img_clean)