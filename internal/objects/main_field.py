from random import randint, shuffle

from kivy.logger import Logger
from kivy.metrics import dp
from kivy.properties import NumericProperty, ListProperty, BooleanProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView

from internal.base.digit_button import DigitButton
from internal.services.digit_list_manager import DigitListManager


class MainField(ScrollView):
    _digit_list = ListProperty([])
    digit_list_len = NumericProperty(0)

    # score for one move (for total score calc)
    __move_score = 0
    # handle in Game class for getting move score with every move even if move score is not new (equals to previous move score)
    move_score_update_flag = BooleanProperty()

    def __init__(self, columns: int, rows: int) -> None:
        super().__init__()
        # main field container
        self.size_hint = (1, 1)
        self.bar_width = 0
        self.do_scroll_x = False

        # base attributes
        self.__columns = columns
        self.__rows = rows

        # list with pressed digit buttons instances
        self.__pressed_digit_buttons: list[DigitButton] = []
        self.__digit_manager = DigitListManager(self.__columns)

        # widgets
        self.grid_digit_list = GridLayout(cols=self.__columns, spacing=dp(1), size_hint_y=None)
        self.grid_digit_list.bind(minimum_height=self.grid_digit_list.setter('height'))
        # properties bindings
        self.bind(_digit_list=lambda instance, value: self.__update_digit_list_display())
        self.__generate_digit_list()
        self.digit_list_len = len(self._digit_list)

        # fill main field
        self.add_widget(self.grid_digit_list)

    # create new digit list for new game
    def new_digit_list(self) -> None:
        # reset pressed buttons list
        self.__pressed_digit_buttons: list[DigitButton] = []
        self.__generate_digit_list()

    # extend digit list with unchecked digits
    def extend_with_unchecked(self) -> None:
        # add unchecked copies of digits to the end of the digit list
        unchecked = [elem.copy() for elem in self._digit_list if not elem.is_checked()]
        for elem in unchecked:
            elem.bind(state=lambda instance, value: self._digit_btn_click(instance, value))
        self._digit_list.extend(unchecked)

    @property
    def move_score(self) -> int:
        return self.__move_score

    # update move_score with given value
    def __set_move_score(self, move_score: int) -> None:
        self.__move_score = move_score
        self.move_score_update_flag = not self.move_score_update_flag

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
    def __generate_digit_list(self) -> None:
        # if list len is odd
        list_len = self.__rows * self.__columns
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
        self._digit_list = digit_list

    def __process_digit_combination(self, digit_button1: DigitButton, digit_button2: DigitButton) -> None:
        x1, y1 = self.__digit_manager.get_x_y_for_digit(self._digit_list, digit_button1)
        x2, y2 = self.__digit_manager.get_x_y_for_digit(self._digit_list, digit_button2)

        points = self.__digit_manager.check_digit_buttons(self._digit_list, x1, y1, x2, y2)
        # if combination is invalid then skip all the next actions
        if not points:
            return
        points_line = self.__digit_manager.remove_checked_lines(self._digit_list)
        self.__set_move_score(points + points_line)

    def __update_digit_list_display(self) -> None:
        self.digit_list_len = len(self._digit_list)
        # if player checked all digits and no one digit buttons row left
        if not self.digit_list_len:
            self.__generate_digit_list()
        # update grid widget
        self.grid_digit_list.clear_widgets()
        for elem in self._digit_list:
            self.grid_digit_list.add_widget(elem)
