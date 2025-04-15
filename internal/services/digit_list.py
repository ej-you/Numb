from math import ceil

from internal.base.digit import Digit


# digit buttons list class
class DigitList:
    def __init__(self, columns: int) -> None:
        self._columns = columns

    # reformat digit list to matrix
    def to_matrix(self, digit_list: list[Digit]) -> list[list[Digit|None]]:
        digit_matrix = [[None for _ in range(self._columns)] for _ in range(self._get_current_rows(digit_list))]
        for i in range(len(digit_list)):
            x, y = self._get_x_y_position(i)
            digit_matrix[y][x] = digit_list[i]
        return digit_matrix

    # get digit x and y position in digits list
    def get_x_y_for_digit(self, digit_list: list[Digit], digit: Digit) -> (int, int):
        return self._get_x_y_position(digit_list.index(digit))

    # get digit
    def _get_digit_by_x_y(self, digit_list: list[Digit], x_position: int, y_position: int) -> Digit:
        return digit_list[y_position * self._columns + x_position]

    # check digit
    def _check_digit_by_x_y(self, digit_list: list[Digit], x_position: int, y_position: int) -> None:
        digit_list[y_position * self._columns + x_position].check()

    # get current rows amount
    def _get_current_rows(self, digit_list: list[Digit]) -> int:
        return ceil(len(digit_list) / self._columns)

    # get digit x and y position using digit list position
    def _get_x_y_position(self, list_position: int) -> (int, int):
        return list_position % self._columns, list_position // self._columns

    def __repr__(self) -> str:
        return f"Digit list: columns - {self._columns}"
