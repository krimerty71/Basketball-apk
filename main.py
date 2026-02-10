from kivy.app import App
from kivy.uix.label import Label

class Game(App):
    def build(self):
        return Label(text='МЯЧИК\nСделано Антоха-кодер')

if __name__ == '__main__':
    Game().run()
