from internal.base.digit import Digit

from kivy.uix.button import Button
from kivy.event import EventDispatcher

from kivy.logger import Logger


class DigitButton(Button, EventDispatcher):
    # colors according to focus
    colors = {
        False: [1, 0, 1, 1],
        True: [0, 0.8, 0.8, 1],
    }

    def __init__(self, digit: Digit, **kwargs):
        super().__init__(**kwargs)
        self.__focus = False

        self.digit = digit
        self.background_normal = ""
        self.background_color = self.colors[self.__focus]
        self.bind(on_press=self.on_press_action)

    @property
    def focus(self):
        return self.__focus

    # custom on_press action using for bind on_press
    def on_press_action(self, instance):
        self.__focus = not self.__focus
        self.background_color = self.colors[self.__focus]
        Logger.debug(f"Кнопка {self.digit} | Фокус после нажатия: {self.__focus}")

    # disable button
    def disable(self):
        self.disabled = True

    # enable button
    def enable(self):
        self.disabled = False

