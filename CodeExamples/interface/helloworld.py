#!/usr/bin/env python3
# helloworld.py
# author: Sébastien Combéfis
# version: March 16, 2016

from kivy.app import App
from kivy.uix.button import Button, Label
from kivy.uix.boxlayout import BoxLayout

class HelloApp(App):
    def build(self):
        box = BoxLayout(orientation='vertical')
        box.add_widget(Label(text='Hello World!'))
        quitbtn = Button(text='Quitter')
        quitbtn.bind(on_press=self._quit)
        box.add_widget(quitbtn)
        return box
    
    def _quit(self, instance):
        App.get_running_app().stop()

if __name__ == '__main__':
    HelloApp().run()