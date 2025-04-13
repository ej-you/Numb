from kivy.uix.button import Button

from internal.base.digit import Digit


class DigitDisplay(Digit):
    # colors according to focus
    colors = {
        False: [1, 1, 1, 1],
        True: [1, 0, 0, 1],
    }

    def __init__(self, value: int) -> None:
        super().__init__(value)
        self._focus = False
        self._button = None


    def display(self):
        self._button = Button(
            text=str(self._value),
        )
        self._button.background_color = self.colors[self._focus]
        self._button.bind(state=self.toggle_color)
        return self._button

    def toggle_color(self, instance):
        self._focus = not self._focus
        self._button.background_color = self.colors[self._focus]
