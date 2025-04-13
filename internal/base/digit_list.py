from math import ceil
from random import randint, shuffle

from internal.base.digit import Digit


# digit buttons list class
class DigitList:
    def __init__(self, rows: int, columns: int) -> None:
        self._columns = columns
        # amount of ability to add unchecked digits to the end of the list
        self._add_ability = 3

        # if list len is odd
        list_len = rows * columns
        if list_len % 2 != 0:
            raise ValueError("The product of rows and columns must be an even number")
        # fill digit list
        self._list = []
        for i in range(0, list_len, 2):
            random_value = randint(1, 9)
            self._list.append(Digit(random_value))
            self._list.append(Digit(random_value))
        shuffle(self._list)

    # decrement ability and return new value
    def use_ability(self) -> int:
        if self._add_ability == 0:
            return 0
        # add unchecked copies of digits to the end of the digit list
        self._list.extend([elem.copy() for elem in self._list if not elem.is_checked()])

        self._add_ability -= 1
        return self._add_ability

    def get_digit_by_x_y(self, x_position: int, y_position: int) -> Digit:
        return self._list[y_position * self._columns + x_position]

    # check digit
    def check_digit_by_x_y(self, x_position: int, y_position: int) -> None:
        self._list[y_position * self._columns + x_position].check()

    # reformat digit list to matrix
    def to_matrix(self) -> list[list[Digit|None]]:
        digit_matrix = [[None for _ in range(self._columns)] for _ in range(self._get_current_rows())]
        for i in range(len(self._list)):
            x, y = self._get_x_y_position(i)
            digit_matrix[y][x] = self._list[i]
        return digit_matrix

    # get current rows amount
    def _get_current_rows(self) -> int:
        return ceil(len(self._list) / self._columns)

    # get digit x and y position using digit list position
    def _get_x_y_position(self, list_position: int) -> (int, int):
        return list_position % self._columns, list_position // self._columns

    # get digit index in digits list
    def _get_digit_index(self, digit: Digit) -> int:
        return self._list.index(digit)

    def __repr__(self):
        digit_matrix = self.to_matrix()
        digit_list = "\n\t".join([" ".join([str(digit_matrix[i][j]) for j in range(len(digit_matrix[i]))]) for i in range(len(digit_matrix))])
        return f"Digit repo\n\tMay add: {self._add_ability} times\n\tDigits:\n\t{digit_list}"
