from kivy.metrics import dp
from kivy.properties import NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

from internal.base.control_button import ControlButton


class Header(BoxLayout):
    color_black = [0, 0, 0, 1]

    score = NumericProperty(0)
    # amount of ability to add unchecked digits to the end of the list
    add_ability = NumericProperty(0)

    def __init__(self, default_score: int, default_add_ability: int):
        super().__init__()
        # header container
        self.orientation = 'horizontal'
        self.size_hint_y=None
        self.height=dp(50)
        self.padding=(dp(0), dp(0), dp(0), dp(10))

        # widgets
        self.__btn_new_game = ControlButton(text="новая игра")
        self.__label_score = Label(text=f"счет: {default_score}", color=self.color_black, font_size=dp(20))
        self.__btn_add_ability = ControlButton(text=f"+ {default_add_ability}")
        # properties bindings
        self.bind(score=lambda instance, value: self._update_score())
        self.bind(add_ability=lambda instance, value: self._update_add_ability())
        self.score = default_score
        self.add_ability = default_add_ability

        # fill header
        self.add_widget(self.__btn_new_game)
        self.add_widget(self.__label_score)
        self.add_widget(self.__btn_add_ability)

    @property
    def btn_add_ability(self) -> ControlButton:
        return self.__btn_add_ability

    @property
    def btn_new_game(self) -> ControlButton:
        return self.__btn_new_game

    # make add ability button disabled
    def disable_add_ability(self) -> None:
        self.__btn_add_ability.disabled = True

    # make add ability button enabled
    def enable_add_ability(self) -> None:
        self.__btn_add_ability.disabled = False

    def _update_score(self) -> None:
        self.__label_score.text = f"счет: {self.score}"

    def _update_add_ability(self) -> None:
        self.__btn_add_ability.text = f"+ {self.add_ability}"
