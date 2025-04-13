from kivy.uix.button import Button

from internal.base.digit import Digit


class DigitDisplay(Digit):
    # colors according to focus
    colors = {
        False: [1, 0, 1, 1],
        True: [1, 0, 0, 1],
    }

    def __init__(self, value: int) -> None:
        super().__init__(value)
        self._focus = False
        self._button = None

    def display(self) -> Button:
        self._button = Button(
            text=str(self._value),
        )
        self._button.background_normal = ""
        self._button.background_color = self.colors[self._focus]
        # self._button.bind(on_press=self.toggle_focus)
        return self._button

    def toggle_focus(self, instance) -> None:
        self._focus = not self._focus
        instance.background_color = self.colors[self._focus]
        instance.text = "gdrthsrt"

    def toggle(self, btn: Button):
        btn.bind(on_press=self.toggle_focus)
