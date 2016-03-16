#!/usr/bin/env python3
# metro.py
# author: Sébastien Combéfis
# version: March 16, 2016

import urllib.request

# Configuration
from kivy.config import Config
Config.set('graphics', 'width',  800)
Config.set('graphics', 'height', 300)

# Application
from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout

class MetroForm(BoxLayout):
    line_input = ObjectProperty()
    station_input = ObjectProperty()
    result_output = ObjectProperty()
    
    def loadschedule(self):
        url = 'http://m.stib.be/api/getwaitingtimes.php?line={}&halt={}'.format(self.line_input.text, self.station_input.text)
        with urllib.request.urlopen(url) as response:
            self.result_output.text = response.read().decode()


class MetroApp(App):
    pass

if __name__ == '__main__':
    MetroApp().run()