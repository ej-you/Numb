from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

from kivy.logger import Logger

from random import randint, shuffle

from internal.base.digit import Digit
from internal.base.digit_button import DigitButton
from internal.services.digit_list_with_manager import DigitListWithManager


class Game:
    # colors according to focus
    colors = {
        "normal": [1, 0, 1, 1],
        "active": [1, 0, 0, 1],
    }
    columns = 10
    rows = 4

    def __init__(self):
        self.__score = 0
        self.__game_over = False

        # list with pressed digit buttons instances
        self.__pressed_digit_buttons: list[DigitButton] = []

        # amount of ability to add unchecked digits to the end of the list
        self.__add_ability = 3
        self.__digit_list = self.__generate_digit_list()
        self.__digit_manager = DigitListWithManager(self.columns)

    # create new random digit list
    def __generate_digit_list(self) -> list[Digit]:
        # if list len is odd
        list_len = self.rows * self.columns
        if list_len % 2 != 0:
            raise ValueError("The product of rows and columns must be an even number")
        # fill digit list
        digit_list = []
        for i in range(0, list_len, 2):
            random_value = randint(1, 9)
            digit_list.append(Digit(random_value))
            digit_list.append(Digit(random_value))
        shuffle(digit_list)
        return digit_list

    # decrement ability and return new value
    def __use_ability(self, instance) -> int:
        if self.__add_ability == 0:
            return 0
        # add unchecked copies of digits to the end of the digit list
        self.__digit_list.extend([elem.copy() for elem in self.__digit_list if not elem.is_checked()])

        self.__add_ability -= 1
        return self.__add_ability

    def __process_digit_combination(self, digit_button1: DigitButton, digit_button2: DigitButton):
        x1, y1 = self.__digit_manager.get_x_y_for_digit(self.__digit_list, digit_button1.digit)
        x2, y2 = self.__digit_manager.get_x_y_for_digit(self.__digit_list, digit_button2.digit)

        points = self.__digit_manager.check_digit_buttons(self.__digit_list, x1, y1, x2, y2)
        # if combination is invalid then skip all the next actions
        if not points:
            return

        self.__score += points
        Logger.info(f"points {points} | score {self.__score}")
        digit_button1.disable()
        digit_button2.disable()

    def digit_btn_click(self, instance, status) -> None:
        # срабатывает при нажатии и отпускании кнопки
        # пропускаем обработку при нажатии
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
                Logger.warn(f"Кнопка {instance.digit} уже не в списке нажатых")

        Logger.debug(f"Нажатые кнопки: {[elem.digit for elem in self.__pressed_digit_buttons]}")
        if len(self.__pressed_digit_buttons) == 2:
            # remove focus from two selected buttons
            for elem in self.__pressed_digit_buttons:
                elem.on_press_action(elem)
            # start digit combination process
            self.__process_digit_combination(*self.__pressed_digit_buttons)
            # clear pressed digit buttons list
            self.__pressed_digit_buttons = []

    def __prepare_digit_list_to_display(self) -> GridLayout:
        btn_grid = GridLayout(
            cols=self.columns,
        )
        for elem in self.__digit_list:
            btn = DigitButton(
                elem,
                text=str(elem.get_value()),
            )
            btn.bind(state=lambda instance, value: self.digit_btn_click(instance, value))
            btn_grid.add_widget(btn)
        return btn_grid

    def display(self) -> BoxLayout:
        main_layout = BoxLayout(orientation='vertical')
        main_layout.add_widget(self._header())
        main_layout.add_widget(self.__prepare_digit_list_to_display())
        return main_layout

    def _header(self) -> BoxLayout:
        header = BoxLayout(orientation='horizontal')
        score = Label(text=str(self.__score))
        header.add_widget(score)

        add_ability_btn = Button(text="+")
        add_ability_btn.bind(on_press=self.__use_ability)
        header.add_widget(add_ability_btn)

        return header
