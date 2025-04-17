from kivy.metrics import dp
from kivy.uix.button import Button


class ControlButton(Button):
    color_light_gray = [0.7, 0.7, 0.7, 1]
    color_dark_gray = [0.55, 0.55, 0.55, 1]
    color_black = [0, 0, 0, 1]

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        # button decorations
        self.__setup_decorations()

    def __setup_decorations(self) -> None:
        # base
        self.background_down = ''
        self.background_normal = ""
        self.background_disabled_normal = ""
        # size
        self.size_hint_y = None
        self.height = dp(40)
        # text
        self.font_size = dp(20)
        self.halign = 'center'
        self.valign = 'middle'
        # colors setup
        self.color = self.color_black
        self.background_color = self.color_light_gray
        self.disabled_color = self.color_dark_gray
