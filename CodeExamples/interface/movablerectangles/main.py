#!/usr/bin/env python3
# main.py
# author: Sébastien Combéfis
# version: March 17, 2016

# Configuration
from kivy.config import Config
Config.set('graphics', 'width',  600)
Config.set('graphics', 'height', 200)

# Application
from kivy.app import App
from kivy.graphics import Line
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout

class DraggableWidget(RelativeLayout):
    def __init__(self, **kwargs):
        self.__selected = None
        super(DraggableWidget, self).__init__(**kwargs)
    
    def on_touch_down(self, touch):
        if self.collide_point(touch.x, touch.y):
            self.select()
            return True
        return super(DraggableWidget, self).on_touch_down(touch)
    
    def on_touch_move(self, touch):
        (x, y) = self.parent.to_parent(touch.x, touch.y)
        if self.__selected and self.parent.collide_point(x - self.width / 2, y - self.height / 2):
            self.translate(touch.x - self.__ix, touch.y - self.__iy)
            return True
        return super(DraggableWidget, self).on_touch_move(touch)
    
    def on_touch_up(self, touch):
        if self.__selected:
            self.unselect()
            return True
        return super(DraggableWidget, self).on_touch_up(touch)
    
    def select(self):
        if not self.__selected:
            self.__ix = self.center_x
            self.__iy = self.center_y
            with self.canvas:
                self.__selected = Line(rectangle=(0, 0, self.width, self.height), dash_offset=2)
    
    def unselect(self):
        if self.__selected:
            self.canvas.remove(self.__selected)
            self.__selected = None
    
    def translate(self, x, y):
        self.center_x = self.__ix = self.__ix + x
        self.center_y = self.__iy = self.__iy + y

class DraggableRectangle(DraggableWidget):
    pass


class MovableRectanglesForm(BoxLayout):
    pass

class MovableRectanglesApp(App):
    pass

if __name__ == '__main__':
    MovableRectanglesApp().run()