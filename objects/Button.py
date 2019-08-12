from .Element import Element
import pygame as pg
import numpy as np

pg.font.init()
white = np.array([255, 255, 255])
black = np.array([0,0,0])
myfont = pg.font.SysFont('Comic Sans MS', 50)
numbers = np.array([pg.K_0, pg.K_1, pg.K_2, pg.K_3, pg.K_4,
           pg.K_5, pg.K_6, pg.K_7, pg.K_8, pg.K_9])


class Button(Element):
    def __init__(self, pos, size, action, frame=4, sensetivity="MOUSE", text="", fit_text=False, toggle=False, pair_button=None, text_color=black):
        Element.__init__(self, pos, sensetivity)
        self.text_color = text_color
        self.textsurface = myfont.render(text, False, text_color) 
        self.pos = self.pos_x, self.pos_y = pos
        self.action = action
        self.frame = frame
        self.marked = False
        self.pair_button = pair_button
        if fit_text:
            self.width, self.height = self.textsurface.get_size()
            self.width += frame*3; self.height += frame*2
            self.size = (self.width, self.height)
        else:
            self.size = self.width, self.height = size
        self._create_rect()
        self.pressed = False
        self.infill_color = [200,200,200]
        self.frame_color = white
        self.toggle = toggle
        self.time_prev_click = 0

    def _create_rect(self):
        self.frame_rect = pg.Rect(self.pos_x, self.pos_y, self.width, self.height)
        self.infill_rect = pg.Rect(self.pos_x+self.frame, self.pos_y+self.frame,
                                   self.width-self.frame*2, self.height-self.frame*2)

    def draw(self):
        pg.draw.rect(self.window, white, self.frame_rect)
        pg.draw.rect(self.window, self.infill_color, self.infill_rect)
        self.window.blit(self.textsurface, (self.pos_x+self.frame*1.5, self.pos_y+self.frame*1.5))
        if self.pressed and not self.toggle:
            self.infill_color = [200,200,200]
            self.changed = True
            self.pressed = False       
        

    def handle_event(self, **kwargs):
        mouse_event = kwargs["mouse_event"]
        if mouse_event[0]:
            if self.frame_rect.collidepoint(pg.mouse.get_pos()):
                if not self.toggle:
                    self.action()
                    self.changed=True
                    self.infill_color = [100,100,100]
                    self.pressed = True
                if self.toggle:
                    self.action()
                    self.changed=True
                    if self.pressed:
                        self.infill_color = [200,200,200]
                        self.pressed = False
                    else:
                        self.infill_color = [100,100,100]
                        self.pressed = True
                        if self.pair_button != None and self.pair_button.pressed:
                            self.pair_button.infill_color = [200,200,200]
                            self.pair_button.pressed = False
                            self.pair_button.changed = True
        
    def set_pair_button(self, pair_button):
        self.pair_button = pair_button

class TextField(Button):

    def __init__(self, pos, size, action=None, frame=4, sensetivity=["MOUSE", "KEY"], text="", fit_text=False, static=False, text_color=black, disabled=False):
        Button.__init__(self, pos, size, action, frame, sensetivity, text, fit_text, text_color)
        self.value = text
        self.static = static
        self.handle_event()
        self.frame_color = white
        self.disabled = disabled

    def draw(self):
        if self.disabled:
            self.frame_color = white / 2
            self.infill_color = white / 2
            self.text_color = white / 2

        if self.pressed:
            self.infill_color = [100,100,100]
            self.changed = True
            self.pressed = False
        self.textsurface = myfont.render(str(self.value), False, self.text_color) 
        pg.draw.rect(self.window, self.frame_color, self.frame_rect)
        pg.draw.rect(self.window, self.infill_color, self.infill_rect)
        self.window.blit(self.textsurface, (self.pos_x+self.frame*1.5, self.pos_y+self.frame*1.5))

    def change_text(self, text):
        self.value = text
        self.changed = True

    def handle_event(self, **kwargs):
        try:
            self.value = int(self.value)
        except ValueError:
            self.value = 100
        if not self.static:
            try:
                mouse_event = kwargs["mouse_event"]
            except KeyError:
                mouse_event = [False]
            try:
                key_event = np.array(kwargs["key_event"])
            except KeyError:
                key_event = False
            if mouse_event[0]:
                self.changed = True
                if self.frame_rect.collidepoint(pg.mouse.get_pos()):
                    if not self.marked:
                        self.infill_color = [100,100,100]
                        self.marked = True
                    elif self.marked:
                        self.infill_color = [200,200,200]
                        self.marked = False
                else:
                    self.infill_color = [200,200,200]
                    self.marked = False
            elif self.marked and sum(key_event) == 1:
                try:
                    number = np.where(key_event[numbers]  == 1)[0][0]
                    if self.value <= 10:
                        self.value = self.value*10 + number
                        if self.value > 19:
                            self.value = 19
                        self.changed = True
                except IndexError:
                    if key_event[pg.K_BACKSPACE]:
                        self.value = 0
                        self.changed = True
                    pass 
        
    def disable(self):
        self.disabled = True
        self.draw()


    def enable(self):
        self.frame_color = white
        self.infill_color = [100,100,100]  
        self.text_color = black
        self.disabled = False
        self.draw()          

if __name__ == '__main__':
    from Window import Window
    import sys
    pg.init()
    window = Window((200, 200))
    pg.event.set_blocked(pg.MOUSEMOTION)


    tf = TextField((50,50), (100, 50))
    window.add_element(tf, "example textfield")

    b = Button((10,10), (40,40), lambda : print(tf.value))
    window.add_element(b, "example button")
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
