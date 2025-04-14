from internal.base.digit import Digit

from kivy.uix.button import Button
from kivy.event import EventDispatcher

from kivy.logger import Logger


class DigitButton(Button, EventDispatcher):
    # __events__ = ('state',)

    # colors according to focus
    colors = {
        False: [1, 0, 1, 1],
        True: [0, 0.8, 0.8, 1],
    }

    def __init__(self, digit: Digit, **kwargs):
        super().__init__(**kwargs)
        self.focus = False
        # self.register_event_type('on_focus_change')

        self.digit = digit
        self.background_normal = ""
        self.background_color = self.colors[self.focus]
        self.bind(on_press=self.on_press_action)

    # custom on_press action for internal changes using inside outer on_press action
    def on_press_internal(self) -> bool:
        self.focus = not self.focus
        self.background_color = self.colors[self.focus]
        # self.dispatch('on_focus_change', self, self.focus)
        Logger.debug(f"Фокус после нажатия: {self.focus}")
        return self.focus

    def on_press_action(self, instance):
        self.focus = not self.focus
        self.background_color = self.colors[self.focus]
        # self.dispatch('on_focus_change', self, self.focus)
        Logger.debug(f"Состояние после нажатия: {self.focus}")
