from kivy.app import App

from internal.services.game import Game


class NumbApp(App):
    def build(self):
        game = Game()
        return game.display()

if __name__ == "__main__":
    NumbApp().run()
