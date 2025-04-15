from random import randint, shuffle

from kivy.properties import NumericProperty, ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.logger import Logger
from kivy.metrics import dp
from kivy.uix.scrollview import ScrollView

from internal.base.digit_button import DigitButton
from internal.services.digit_list_with_manager import DigitListManager


class Game(BoxLayout):
    color_white = [1, 1, 1, 1]
    # color_light_gray = [0.7, 0.7, 0.7, 1]
    color_black = [0, 0, 0, 1]

    columns = 10
    rows = 4

    score = NumericProperty(0)
    digit_list = ListProperty([])
    # amount of ability to add unchecked digits to the end of the list
    add_ability = NumericProperty(3)

    score_label = Label(text=f"score: 0", color=color_black)
    btn_grid = GridLayout(
        cols=columns,
        spacing=dp(1),
        size_hint_y=None, # AAAAAAAAAAAAAAAAAA
    )
    add_ability_btn = Button(text=f"+ 3", color=color_black)

    def __init__(self):
        super().__init__()
        # list with pressed digit buttons instances
        self.__pressed_digit_buttons: list[DigitButton] = []

        self.digit_list = self.__generate_digit_list()
        self.__digit_manager = DigitListManager(self.columns)

        Logger.info(f"type self.digit_list {type(self.digit_list)}")
        Logger.info(f"self.digit_list {self.digit_list}")
        # 3. Автоподстройка высоты содержимого
        self.btn_grid.bind(minimum_height=self.btn_grid.setter('height'))

        # self.add_widget(self.display())
        self.bind(score=self._update_display)
        self.bind(digit_list=self.update_digit_list)
        self.bind(add_ability=self.update_add_ability)

        self.add_ability_btn.bind(on_press=self._use_ability)

        self.__prepare_digit_list_to_display()
        self.display()

    def _update_display(self, instance, value):
        self.score_label.text = f"score: {self.score}"

    # new game button handler
    def on_new_game(self, instance):
        self.score = 0
        self.digit_list = self.__generate_digit_list()
        self.add_ability = 3
        self.__pressed_digit_buttons: list[DigitButton] = []
        self.add_ability_btn.disabled = False

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
                digit_btn.bind(state=lambda instance, value: self.digit_btn_click(instance, value))
        for _ in range(3):
            shuffle(digit_list)
        return digit_list

    # decrement ability and return new value
    def _use_ability(self, instance: Button):
        Logger.debug(f"instance {instance}")
        if self.add_ability == 0:
            # instance.disabled = True
            return
        # add unchecked copies of digits to the end of the digit list
        unchecked = [elem.copy() for elem in self.digit_list if not elem.is_checked()]
        for elem in unchecked:
            elem.bind(state=lambda instance, value: self.digit_btn_click(instance, value))
        self.digit_list.extend(unchecked)
        self.add_ability -= 1
        if self.add_ability == 0:
            instance.disabled = True

    def __process_digit_combination(self, digit_button1: DigitButton, digit_button2: DigitButton):
        x1, y1 = self.__digit_manager.get_x_y_for_digit(self.digit_list, digit_button1)
        x2, y2 = self.__digit_manager.get_x_y_for_digit(self.digit_list, digit_button2)

        points = self.__digit_manager.check_digit_buttons(self.digit_list, x1, y1, x2, y2)
        # if combination is invalid then skip all the next actions
        if not points:
            return

        Logger.info(f"points {points} | score {self.score}")
        points_line = self.__digit_manager.remove_checked_lines(self.digit_list)
        Logger.info(f"points_line {points_line} | score {self.score}")
        self.score += points + points_line

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
                Logger.warn(f"Кнопка {instance} уже не в списке нажатых")

        Logger.debug(f"Нажатые кнопки: {[elem for elem in self.__pressed_digit_buttons]}")
        if len(self.__pressed_digit_buttons) == 2:
            # remove focus from two selected buttons
            for elem in self.__pressed_digit_buttons:
                elem.on_press_action(elem)
            # start digit combination process
            self.__process_digit_combination(*self.__pressed_digit_buttons)
            # clear pressed digit buttons list
            self.__pressed_digit_buttons = []

    def __prepare_digit_list_to_display(self):
        Logger.debug(f"prepare | score: {self.score}")
        # if player checked all digits and no one digit buttons row left
        if len(self.digit_list) == 0:
            self.digit_list = self.__generate_digit_list()
            self.add_ability = 3

        self.btn_grid.clear_widgets()
        for elem in self.digit_list:
            self.btn_grid.add_widget(elem)

    def update_digit_list(self, instance, value):
        self.__prepare_digit_list_to_display()

    def update_add_ability(self, instance, value):
        # Logger.debug(f"instance: {instance} | value {value}")
        self.add_ability_btn.text = f"+ {self.add_ability}"

    def __prepare_header(self) -> BoxLayout:
        # container
        header = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(50),
            padding=(dp(0), dp(0), dp(0), dp(10)),
        )

        # new game button
        new_game_btn = Button(text="new game", color=self.color_black)
        new_game_btn.bind(on_press=self.on_new_game)

        # score
        # score_container = BoxLayout(
        #     orientation='vertical',
        # )
        # score_container.add_widget(
        #     Label(text="score", color=self.color_black)
        # )
        # score_container.add_widget(
        #     # Label(text=str(self.score), color=self.color_black)
        #     self.score_label
        # )

        # add unchecked digits button
        # add_unchecked_btn = self.add_ability_btn  # Button(text=f"+ {self.add_ability}", color=self.color_black)
        # add_unchecked_btn.bind(on_press=self._use_ability)

        # fill header
        header.add_widget(new_game_btn)
        header.add_widget(self.score_label)
        # header.add_widget(add_unchecked_btn)
        header.add_widget(self.add_ability_btn)
        return header

    def display(self) -> None: # BoxLayout:
        main_layout = BoxLayout(
            orientation='vertical',
            padding=dp(10),
            # background_color=[0.7, 0.7, 0.7, 1],
        )

        # Создаем ScrollView
        scroll = ScrollView(
            size_hint=(1, 1),  # Занимает всё доступное пространство
            # bar_width=dp(10),  # Толщина полосы прокрутки
            bar_width=0,  # Толщина полосы прокрутки
            # scroll_type=['bars', 'content']  # Тип прокрутки
        )
        scroll.do_scroll_x = False

        # scroll.add_widget(self.__prepare_digit_list_to_display())
        scroll.add_widget(self.btn_grid)

        main_layout.add_widget(self.__prepare_header())
        # main_layout.add_widget(self.__prepare_digit_list_to_display())
        # main_layout.add_widget(self.btn_grid)

        main_layout.add_widget(scroll)

        self.add_widget(main_layout)
        # return main_layout
