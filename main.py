from kivy.app import App
from kivy.config import Config
from kivy.core.window import Window
from kivy.logger import Logger, LOG_LEVELS
from kivy.metrics import dp

from internal.game import Game


Logger.setLevel(LOG_LEVELS["debug"])

Config.set("graphics", "resizable", 0)
Config.set("graphics", "height", dp(2340))
Config.set("graphics", "width", dp(1080))

Window.clearcolor = (0.8, 0.8, 0.8, 1)


class NumbApp(App):
    def build(self):
        game = Game()
        return game

if __name__ == "__main__":
    NumbApp().run()
