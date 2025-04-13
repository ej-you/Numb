from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

from internal.display.digit_list_with_manager import DigitListWithManagerDisplay


class Game:
    rows = 3
    columns = 10

    def __init__(self):
        self._score = 0
        self._game_over = False
        self._digit_list = DigitListWithManagerDisplay(rows=self.rows, columns=self.columns)

    def display(self) -> BoxLayout:
        main_layout = BoxLayout(orientation='vertical')
        main_layout.add_widget(self._header())
        main_layout.add_widget(self._digit_list.display())
        return main_layout

    def _header(self) -> BoxLayout:
        header = BoxLayout(orientation='horizontal')
        score = Label(text=str(self._score))
        header.add_widget(score)

        add_ability_btn = Button(text="+")
        add_ability_btn.bind(on_press=self._digit_list.use_ability)
        header.add_widget(add_ability_btn)

        return header
