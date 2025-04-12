from uuid import uuid4 as uuid

# one digit button class
class Digit:
    def __init__(self, value: int) -> None:
        self._uuid = uuid()
        self._value = value
        self._checked = False

    # returns copy of current digit with new uuid
    def copy(self) -> "Digit":
        copy = Digit(self._value)
        if self.is_checked():
            copy.check()
        return copy

    # set checked True
    def check(self) -> None:
        self._checked = True

    # return True if digit is checked
    def is_checked(self) -> bool:
        return self._checked

    # get digit
    def get_value(self) -> int:
        return self._value

    def __repr__(self) -> str:
        checked = "✅" if self._checked else "❌"
        return f"({self._value} {checked})"
