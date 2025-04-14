from math import ceil

from internal.base.digit import Digit


# digit buttons list class
class DigitList:
    def __init__(self, columns: int) -> None:
        self._columns = columns

    def get_digit_by_x_y(self, digit_list: list[Digit], x_position: int, y_position: int) -> Digit:
        return digit_list[y_position * self._columns + x_position]

    # check digit
    def check_digit_by_x_y(self, digit_list: list[Digit], x_position: int, y_position: int) -> None:
        digit_list[y_position * self._columns + x_position].check()

    # reformat digit list to matrix
    def to_matrix(self, digit_list: list[Digit]) -> list[list[Digit|None]]:
        digit_matrix = [[None for _ in range(self._columns)] for _ in range(self._get_current_rows(digit_list))]
        for i in range(len(digit_list)):
            x, y = self._get_x_y_position(i)
            digit_matrix[y][x] = digit_list[i]
        return digit_matrix

    # get current rows amount
    def _get_current_rows(self, digit_list: list[Digit]) -> int:
        return ceil(len(digit_list) / self._columns)

    # get digit x and y position using digit list position
    def _get_x_y_position(self, list_position: int) -> (int, int):
        return list_position % self._columns, list_position // self._columns

    # get digit index in digits list
    @staticmethod
    def _get_digit_index(digit_list: list[Digit], digit: Digit) -> int:
        return digit_list.index(digit)

    # get digit x and y position in digits list
    def get_x_y_for_digit(self, digit_list: list[Digit], digit: Digit) -> (int, int):
        return self._get_x_y_position(self._get_digit_index(digit_list, digit))

    def __repr__(self):
        # digit_matrix = self.to_matrix()
        # digit_list = "\n\t".join([" ".join([str(digit_matrix[i][j]) for j in range(len(digit_matrix[i]))]) for i in range(len(digit_matrix))])
        # return f"Digit repo\n\tMay add: {self._add_ability} times\n\tDigits:\n\t{digit_list}"
        return f"Digit repo: columns - {self._columns}"
