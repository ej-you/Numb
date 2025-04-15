from kivy.logger import Logger
from kivy.metrics import dp
from kivy.uix.button import Button

from internal.base.digit import Digit


class DigitButton(Digit, Button):
    color_white = [1, 1, 1, 1]
    color_light_gray = [0.7, 0.7, 0.7, 1]
    color_black = [0, 0, 0, 1]
    # base colors
    colors = {
        "color": color_black,
        "background_color": color_white,
        "disabled_color": color_light_gray,
    }
    # colors according to focus
    focus_background_colors = {
        False: color_white,
        True: color_light_gray,
    }

    def __init__(self, value: int) -> None:
        Digit.__init__(self, value)
        Button.__init__(self)
        self.__focus = False

        # button functionality
        self.text = str(self._value)
        self.bind(on_press=self.on_press_action)
        # button decorations
        self.__setup_decorations()

    # custom on_press action using for bind on_press
    def on_press_action(self, instance) -> None:
        self.__focus = not self.__focus
        self.background_color = self.focus_background_colors[self.__focus]
        Logger.debug(f"DigitButton on_press: Button {self} | Focus after press: {self.__focus}")

    @property
    def focus(self) -> bool:
        return self.__focus

    # returns copy of current digit button with new uuid
    def copy(self) -> "DigitButton":
        copy = DigitButton(self._value)
        if self.is_checked():
            copy.check()
        return copy

    # set checked True and disable button
    def check(self) -> None:
        super().check()
        self.disabled = True

    def __setup_decorations(self) -> None:
        # base
        self.background_down = ''
        self.background_normal = ""
        self.background_disabled_normal = ""
        # size
        self.size_hint_y = None
        self.height = dp(40)
        # text
        self.font_size = dp(30)
        self.halign = 'center'
        self.valign = 'middle'
        # colors setup
        self.color = self.colors["color"]
        self.background_color = self.colors["background_color"]
        self.disabled_color = self.colors["disabled_color"]
