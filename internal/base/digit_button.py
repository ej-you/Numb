from internal.base.digit import Digit

from kivy.uix.button import Button
from kivy.event import EventDispatcher

from kivy.logger import Logger


class DigitButton(Button, EventDispatcher):
    __events__ = ('on_state_change',)

    # colors according to focus
    colors = {
        False: [1, 0, 1, 1],
        True: [0, 0.8, 0.8, 1],
    }

    def __init__(self, digit: Digit, **kwargs):
        super().__init__(**kwargs)
        self.focus = False
        # self.register_event_type('on_state_change')

        self.digit = digit
        self.background_normal = ""
        self.background_color = self.colors[self.focus]
        self.bind(on_press=self.on_press_action)

    def on_state_change(self, *args):
        # Logger.debug(f"Состояние дефолтное: {self.focus}")
        pass

    def on_press_action(self, instance):
        Logger.debug(f"Состояние при нажатии: {self.focus}")
        self.focus = not self.focus
        self.background_color = self.colors[self.focus]
        self.dispatch('on_state_change', self, self.focus)
