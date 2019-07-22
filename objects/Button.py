from .Element import Element
import pygame as pg

pg.font.init()
white = [255, 255, 255]
black = [0,0,0]
myfont = pg.font.SysFont('Comic Sans MS', 50)

class Button(Element):
    def __init__(self, pos, size, action, frame=4, sensetivity="MOUSE", text="", fit_text=False):
        Element.__init__(self, pos, sensetivity)
        self.textsurface = myfont.render(text, False, (0, 0, 0)) 
        self.pos = self.pos_x, self.pos_y = pos
        self.action = action
        self.frame = frame
        self.marked = False
        if fit_text:
            self.width, self.height = self.textsurface.get_size()
            self.width += frame*3; self.height += frame*2
            self.size = (self.width, self.height)
            print(self.height)
        else:
            self.size = self.width, self.height = size
        self._create_rect()
        self.pressed = False
        self.infill_color = [200,200,200]

    def _create_rect(self):
        self.frame_rect = pg.Rect(self.pos_x, self.pos_y, self.width, self.height)
        self.infill_rect = pg.Rect(self.pos_x+self.frame, self.pos_y+self.frame,
                                   self.width-self.frame*2, self.height-self.frame*2)

    def draw(self):
        pg.draw.rect(self.window, white, self.frame_rect)
        pg.draw.rect(self.window, self.infill_color, self.infill_rect)
        self.window.blit(self.textsurface, (self.pos_x+self.frame*1.5, self.pos_y+self.frame*1.5))
        if self.pressed:
            self.infill_color = [200,200,200]
            self.changed = True
            self.pressed = False
        

    def handle_event(self, **kwargs):
        print(kwargs)
        mouse_event = kwargs["mouse_event"]
        if mouse_event[0]:
            if self.frame_rect.collidepoint(pg.mouse.get_pos()):
                self.action()
                self.changed=True
                self.infill_color = [100,100,100]
                self.pressed = True

        

if __name__ == '__main__':
    pg.init()
    window = pg.display.set_mode((200, 200))
    window.fill(white)

    b = Button(window, (10,10), (40,40), lambda : print("asd"))
    b.draw()
    pg.display.flip()
    pg.time.wait(1000)
