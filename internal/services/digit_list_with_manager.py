from internal.base.digit import Digit
from internal.services.digit_list import DigitList


# extends digit buttons list class with methods to check digit buttons
class DigitListManager(DigitList):
    def __init__(self, columns: int) -> None:
        super().__init__(columns)

    # remove digits row if all the digits on this row is checked
    def remove_checked_lines(self, digit_list: list[Digit]) -> int:
        # filter digits to remove
        list_to_remove = []
        checked_row = []
        for i in range(0, len(digit_list), self._columns):
            checked_row = [elem for elem in digit_list[i:i + self._columns] if elem.is_checked()]
            # if checked all digits in a fulfilled row
            if len(checked_row) == self._columns:
                list_to_remove.extend(checked_row)
        # if checked all digits in the last row (maybe not fulfilled)
        if len(checked_row) == len(digit_list) % self._columns:
            list_to_remove.extend(checked_row)

        # clean digits list
        for elem in list_to_remove:
            digit_list.remove(elem)
        return len(list_to_remove) // self._columns * 10

    # check digit button (and returns score) if possible otherwise leave it unchanged
    def check_digit_buttons(self,
                            digit_list: list[Digit],
                            first_x: int, first_y: int, second_x: int, second_y: int
                            ) -> int:
        # check values
        first_digit_value = self._get_digit_by_x_y(digit_list, first_x, first_y).get_value()
        second_digit_value = self._get_digit_by_x_y(digit_list, second_x, second_y).get_value()
        if first_digit_value != second_digit_value and first_digit_value + second_digit_value != 10:
            return 0

        # check position
        for check_func in [
            self.__is_neighbours,
            self.__is_one_row, self.__is_one_column, self.__is_diagonal,
            self.__is_line_end
        ]:
            must_check, score = check_func(digit_list, first_x, first_y, second_x, second_y)
            if must_check:
                # set check for digits
                self._check_digit_by_x_y(digit_list, first_x, first_y)
                self._check_digit_by_x_y(digit_list, second_x, second_y)
                return score
        return 0

    # one row, one column or one diagonal neighbours
    @staticmethod
    def __is_neighbours(digit_list: list[Digit],
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
    def __is_one_row(self,
                     digit_list: list[Digit],
                     first_x: int, first_y: int, second_x: int, second_y: int
                     ) -> (bool, int):
        # check digits placed on one row
        if first_y != second_y:
            return False, 0
        # check all digits between two given digits is checked
        for x in range(min(first_x, second_x) + 1, max(first_x, second_x)):
            if not self._get_digit_by_x_y(digit_list, x, first_y).is_checked():
                return False, 0
        return True, abs(first_x - second_x)

    # digits placed on one column
    def __is_one_column(self,
                        digit_list: list[Digit],
                        first_x: int, first_y: int, second_x: int, second_y: int
                        ) -> (bool, int):
        # check digits placed on one column
        if first_x != second_x:
            return False, 0
        # check all digits between two given digits is checked
        for y in range(min(first_y, second_y) + 1, max(first_y, second_y)):
            if not self._get_digit_by_x_y(digit_list, first_x, y).is_checked():
                return False, 0
        return True, abs(first_y - second_y)

    # digits placed on diagonal
    def __is_diagonal(self,
                      digit_list: list[Digit],
                      first_x: int, first_y: int, second_x: int, second_y: int
                      ) -> (bool, int):
        max_x = max(first_x, second_x)
        min_x = min(first_x, second_x)
        max_y = max(first_y, second_y)
        min_y = min(first_y, second_y)
        # check digits placed on diagonal
        if max_x - min_x != max_y - min_y:
            return False, 0

        # process ranges for x and y coords (that point to digits between selected digits)
        x_range = (list(range(first_x, second_x)) if first_x < second_x else list(range(first_x, second_x, -1)))[1:]
        y_range = (list(range(first_y, second_y)) if first_y < second_y else list(range(first_y, second_y, -1)))[1:]

        # check all digits between two selected digits is checked
        for i in range(len(x_range)):
            if not self._get_digit_by_x_y(digit_list, x_range[i], y_range[i]).is_checked():
                return False, 0
        return True, max_x - min_x

    # digits are neighbours in list representation (not matrix)
    def __is_line_end(self,
                      digit_list: list[Digit],
                      first_x: int, first_y: int, second_x: int, second_y: int
                      ) -> (bool, int):
        first_digit = self._get_digit_by_x_y(digit_list, first_x, first_y)
        second_digit = self._get_digit_by_x_y(digit_list, second_x, second_y)

        first_digit_idx = digit_list.index(first_digit)
        second_digit_idx = digit_list.index(second_digit)

        for i in range(min(first_digit_idx, second_digit_idx) + 1, max(first_digit_idx, second_digit_idx)):
            if not digit_list[i].is_checked():
                return False, 0
        return True, abs(first_digit_idx - second_digit_idx)
