from random import randint, shuffle

from kivy.logger import Logger
from kivy.metrics import dp
from kivy.properties import NumericProperty, ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView

from internal.base.digit_button import DigitButton
from internal.services.digit_list_with_manager import DigitListManager


class Game(BoxLayout):
    color_white = [1, 1, 1, 1]
    color_black = [0, 0, 0, 1]

    columns = 10
    rows = 4

    default_score = 0
    default_add_ability = 3

    score = NumericProperty(default_score)
    digit_list = ListProperty([])
    # amount of ability to add unchecked digits to the end of the list
    add_ability = NumericProperty(default_add_ability)

    score_label = Label(text=f"score: 0", color=color_black)
    btn_grid = GridLayout(cols=columns, spacing=dp(1), size_hint_y=None)
    add_ability_btn = Button(text=f"+ 3", color=color_black)

    def __init__(self) -> None:
        super().__init__()
        # list with pressed digit buttons instances
        self.__pressed_digit_buttons: list[DigitButton] = []
        self.__digit_manager = DigitListManager(self.columns)
        self.digit_list = self.__generate_digit_list()

        self.orientation = 'vertical'
        self.padding = dp(10)

        self.bind(score=self._update_score)
        self.bind(digit_list=self._update_digit_list)
        self.bind(add_ability=self._update_add_ability)

        self.add_ability_btn.bind(on_press=self._use_ability)
        self.btn_grid.bind(minimum_height=self.btn_grid.setter('height'))

        self.__update_digit_list_display()
        self.__display()

    def _update_score(self, instance, value) -> None:
        self.score_label.text = f"score: {self.score}"

    def _update_digit_list(self, instance, value) -> None:
        self.__update_digit_list_display()

    def _update_add_ability(self, instance, value) -> None:
        self.add_ability_btn.text = f"+ {self.add_ability}"

    # new game button handler
    def _on_new_game(self, instance) -> None:
        self.score = self.default_score
        self.add_ability = self.default_add_ability
        self.add_ability_btn.disabled = False
        self.digit_list = self.__generate_digit_list()
        self.__pressed_digit_buttons: list[DigitButton] = []

    # decrement ability and return new value
    def _use_ability(self, instance: Button) -> None:
        if self.add_ability == 0:
            return

        # add unchecked copies of digits to the end of the digit list
        unchecked = [elem.copy() for elem in self.digit_list if not elem.is_checked()]
        for elem in unchecked:
            elem.bind(state=lambda instance, value: self._digit_btn_click(instance, value))
        self.digit_list.extend(unchecked)
        self.add_ability -= 1

        if self.add_ability == 0:
            instance.disabled = True

    def _digit_btn_click(self, instance, status) -> None:
        # triggered by press down and pull up (so skip press down processing)
        if status == "down":
            return

        # if button is pressed then append it to list
        if instance.focus:
            self.__pressed_digit_buttons.append(instance)
        # if button is unpressed then remove it from list
        else:
            try:
                self.__pressed_digit_buttons.remove(instance)
            except ValueError:
                Logger.warn(f"Game digit_btn_click: Button {instance} is not in __pressed_digit_buttons list")

        Logger.debug(f"Game digit_btn_click: Pressed buttons: {[elem for elem in self.__pressed_digit_buttons]}")
        if len(self.__pressed_digit_buttons) == 2:
            # remove focus from two selected buttons
            for elem in self.__pressed_digit_buttons:
                elem.on_press_action(elem)
            # start digit combination process
            self.__process_digit_combination(*self.__pressed_digit_buttons)
            # clear pressed digit buttons list
            self.__pressed_digit_buttons = []

    # create new random digit list
    def __generate_digit_list(self) -> list[DigitButton]:
        # if list len is odd
        list_len = self.rows * self.columns
        if list_len % 2 != 0:
            raise ValueError("The product of rows and columns must be an even number")
        # fill digit list
        digit_list = []
        for i in range(0, list_len, 2):
            random_value = randint(1, 9)
            for _ in range(2):
                digit_btn = DigitButton(random_value)
                digit_list.append(digit_btn)
                digit_btn.bind(state=lambda instance, value: self._digit_btn_click(instance, value))
        for _ in range(3):
            shuffle(digit_list)
        return digit_list

    def __process_digit_combination(self, digit_button1: DigitButton, digit_button2: DigitButton) -> None:
        x1, y1 = self.__digit_manager.get_x_y_for_digit(self.digit_list, digit_button1)
        x2, y2 = self.__digit_manager.get_x_y_for_digit(self.digit_list, digit_button2)

        points = self.__digit_manager.check_digit_buttons(self.digit_list, x1, y1, x2, y2)
        # if combination is invalid then skip all the next actions
        if not points:
            return
        points_line = self.__digit_manager.remove_checked_lines(self.digit_list)
        self.score += points + points_line

    def __update_digit_list_display(self) -> None:
        Logger.debug(f"prepare | score: {self.score}")
        # if player checked all digits and no one digit buttons row left
        if len(self.digit_list) == 0:
            self.digit_list = self.__generate_digit_list()
            self.add_ability = 3

        self.btn_grid.clear_widgets()
        for elem in self.digit_list:
            self.btn_grid.add_widget(elem)

    def __header(self) -> BoxLayout:
        # container
        header = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(50),
            padding=(dp(0), dp(0), dp(0), dp(10)),
        )
        # new game button
        new_game_btn = Button(text="new game", color=self.color_black)
        new_game_btn.bind(on_press=self._on_new_game)
        # fill header
        header.add_widget(new_game_btn)
        header.add_widget(self.score_label)
        header.add_widget(self.add_ability_btn)
        return header

    def __display(self) -> None:
        scroll = ScrollView(
            size_hint=(1, 1),
            bar_width=0,
            do_scroll_x=False,
        )
        scroll.add_widget(self.btn_grid)

        self.add_widget(self.__header())
        self.add_widget(scroll)
