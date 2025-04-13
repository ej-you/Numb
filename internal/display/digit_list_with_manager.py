from kivy.uix.gridlayout import GridLayout
from random import randint, shuffle

from internal.base.digit_list_with_manager import DigitListWithManager
from internal.display.digit import DigitDisplay


# one digit button class
class DigitListWithManagerDisplay(DigitListWithManager):
    def __init__(self, rows: int, columns: int) -> None:
        super().__init__(rows, columns)
        # fill digit list
        self._list = []
        for i in range(0, rows * columns, 2):
            random_value = randint(1, 9)
            self._list.append(DigitDisplay(random_value))
            self._list.append(DigitDisplay(random_value))
        shuffle(self._list)

        self._grid = self._create_grid()


    # decrement ability and return new value
    def use_ability(self) -> int:
        result = super().use_ability()
        self._grid = self._create_grid()
        return result

    def _create_grid(self) -> GridLayout:
        grid = GridLayout(
            cols=self._columns,
        )
        for elem in self._list:
            btn = elem.display()
            elem.toggle(btn)
            grid.add_widget(btn)
            # grid.add_widget(elem.display())
        return grid

    def display(self) -> GridLayout:
        return self._grid
