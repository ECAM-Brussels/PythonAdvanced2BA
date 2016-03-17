#!/usr/bin/env python3
# metro.py
# author: Sébastien Combéfis
# version: March 17, 2016

import re
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
        try:
            url = 'http://m.stib.be/api/getwaitingtimes.php?line={}&halt={}'.format(self.line_input.text, self.station_input.text)
            with urllib.request.urlopen(url) as response:
                xml = response.read().decode()
                pattern = r"<waitingtime>.*?<minutes>([0-9]+)</minutes>.*?<destination>([A-Z ']+)</destination>.*?</waitingtime>"
                p = re.compile(pattern)
                schedule = ''
                for m in p.finditer(xml):
                    schedule += 'Vers {} : prochain dans {} minutes\n'.format(m.group(2), m.group(1))
                self.result_output.text = schedule
        except:
            self.result_output.text = 'Impossible de récupérer les horaires.'

class MetroApp(App):
    pass

if __name__ == '__main__':
    MetroApp().run()