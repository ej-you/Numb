from kivy.app import App
from kivy.config import Config
from kivy.logger import Logger, LOG_LEVELS

from internal.game import Game

Logger.setLevel(LOG_LEVELS["debug"])

Config.set("graphics", "resizable", 0)
Config.set("graphics", "height", 780) # 2340
Config.set("graphics", "width", 360) # 1080

class NumbApp(App):
    def build(self):
        game = Game()
        return game.display()

if __name__ == "__main__":
    NumbApp().run()
