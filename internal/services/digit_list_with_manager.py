from internal.services.digit_list import DigitList
from internal.base.digit import Digit


# extends digit buttons list class with methods to check digit buttons
class DigitListWithManager(DigitList):
    def __init__(self, columns: int) -> None:
        super().__init__(columns)

    # remove digits row if all the digits on this row is checked
    def remove_checked_lines(self, digit_list: list[Digit]) -> int:
        # filter digits to remove
        list_to_remove = []
        for i in range(0, len(digit_list), self._columns):
            checked_row = [elem for elem in digit_list[i:i + self._columns] if elem.is_checked()]
            if len(checked_row) == self._columns:
                list_to_remove.extend(checked_row)
        # clean digits list
        for elem in list_to_remove:
            digit_list.remove(elem)
        return len(list_to_remove) // self._columns * 10

    # check digit button (and returns score) if possible otherwise leave it unchanged
    def check_digit_buttons(self, digit_list: list[Digit], first_x: int, first_y: int, second_x: int, second_y: int) -> int:
        # check values
        first_digit_value = self.get_digit_by_x_y(digit_list, first_x, first_y).get_value()
        second_digit_value = self.get_digit_by_x_y(digit_list, second_x, second_y).get_value()
        if first_digit_value != second_digit_value and first_digit_value + second_digit_value != 10:
            return 0

        # check position
        for check_func in [
            self._is_neighbours,
            self._is_one_row, self._is_one_column, self._is_diagonal,
            self._is_line_end
        ]:
            must_check, score = check_func(digit_list, first_x, first_y, second_x, second_y)
            if must_check:
                # set check for digits
                self.check_digit_by_x_y(digit_list, first_x, first_y)
                self.check_digit_by_x_y(digit_list, second_x, second_y)
                return score
        return 0

    # one row, one column or one diagonal neighbours
    @staticmethod
    def _is_neighbours(
            digit_list: list[Digit],
            first_x: int, first_y: int, second_x: int, second_y: int
    ) -> (bool, int):
        if first_y == second_y and min(first_x, second_x) + 1 == max(first_x, second_x):
            return True, 1
        if first_x == second_x and min(first_y, second_y) + 1 == max(first_y, second_y):
            return True, 1
        if min(first_x, second_x) + 1 == max(first_x, second_x) and min(first_y, second_y) + 1 == max(first_y, second_y):
            return True, 1
        return False, 0

    # digits placed on one row
    def _is_one_row(self,
            digit_list: list[Digit],
            first_x: int, first_y: int, second_x: int, second_y: int
    ) -> (bool, int):
        # check digits placed on one row
        if first_y != second_y:
            return False, 0
        # check all digits between two given digits is checked
        for x in range(min(first_x, second_x) + 1, max(first_x, second_x)):
            if not self.get_digit_by_x_y(digit_list, x, first_y).is_checked():
                return False, 0
        return True, abs(first_x - second_x)

    # digits placed on one column
    def _is_one_column(self,
            digit_list: list[Digit],
            first_x: int, first_y: int, second_x: int, second_y: int
    ) -> (bool, int):
        # check digits placed on one column
        if first_x != second_x:
            return False, 0
        # check all digits between two given digits is checked
        for y in range(min(first_y, second_y) + 1, max(first_y, second_y)):
            if not self.get_digit_by_x_y(digit_list, first_x, y).is_checked():
                return False, 0
        return True, abs(first_y - second_y)

    # digits placed on diagonal
    def _is_diagonal(self,
            digit_list: list[Digit],
            first_x: int, first_y: int, second_x: int, second_y: int
    ) -> (bool, int):
        max_x = max(first_x, second_x)
        min_x = min(first_x, second_x)
        max_y = max(first_x, second_x)
        min_y = min(first_y, second_y)
        n = max_x - min_x
        # check digits placed on diagonal
        if max_y - min_y != n:
            return False, 0

        # check all digits between two given digits is checked
        for i in range(min_x + 1, max_x):
            if not self.get_digit_by_x_y(digit_list, i, i).is_checked():
                return False, 0
        return True, max_x - min_x

    # digits are neighbours in list representation (not matrix)
    def _is_line_end(self,
            digit_list: list[Digit],
            first_x: int, first_y: int, second_x: int, second_y: int
    ) -> (bool, int):
        first_digit = self.get_digit_by_x_y(digit_list, first_x, first_y)
        second_digit = self.get_digit_by_x_y(digit_list, second_x, second_y)

        first_digit_idx = digit_list.index(first_digit)
        second_digit_idx = digit_list.index(second_digit)

        for i in range(min(first_digit_idx, second_digit_idx) + 1, max(first_digit_idx, second_digit_idx)):
            if not digit_list[i].is_checked():
                return False, 0
        return True, abs(first_digit_idx - second_digit_idx)
