from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout

from internal.objects.header import Header
from internal.objects.main_field import MainField


class Game(BoxLayout):
    # main field settings
    __columns = 10
    __rows = 4

    # default values
    __default_score = 0
    __default_add_ability = 3

    def __init__(self, columns: int = 10, rows: int = 4, default_add_ability: int = 3) -> None:
        super().__init__()
        # game container
        self.orientation = 'vertical'
        self.padding = dp(10)

        # base attributes
        self.__columns = columns
        self.__rows = rows
        self.__default_score = 0
        self.__default_add_ability = default_add_ability

        self.__header = Header(self.__default_score, self.__default_add_ability)
        # buttons is triggered by press down and pull up (so skip press down processing)
        self.__header.btn_new_game.bind(state=lambda instance, status: self._on_new_game(status) if status != "down" else None)
        self.__header.btn_add_ability.bind(state=lambda instance, status: self._use_ability(status) if status != "down" else None)

        self.__main_field = MainField(self.__columns, self.__rows)
        # do if digit list is empty
        self.__main_field.bind(digit_list_len=lambda instance, value: self._empty_digit_list() if not value else None)
        # for update total score every move
        self.__main_field.bind(move_score_update_flag=lambda instance, value: self._increase_score())

        # fill game
        self.add_widget(self.__header)
        self.add_widget(self.__main_field)

    # new game button handler
    def _on_new_game(self, status) -> None:
        # reset score and add_ability values
        self.__header.score = self.__default_score
        self.__header.add_ability = self.__default_add_ability
        self.__header.enable_add_ability()
        # generate new digit list
        self.__main_field.new_digit_list()

    # decrement ability and return new value
    def _use_ability(self, status) -> None:
        if self.__header.add_ability == 0:
            return
        self.__main_field.extend_with_unchecked()
        self.__header.add_ability -= 1

        if self.__header.add_ability == 0:
            self.__header.disable_add_ability()

    # reset add_ability button state if digit list is empty
    def _empty_digit_list(self) -> None:
        self.__header.add_ability = self.__default_add_ability
        self.__header.enable_add_ability()

    # increase total score by new move score
    def _increase_score(self) -> None:
        self.__header.score += self.__main_field.move_score
