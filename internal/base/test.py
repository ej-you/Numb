from digit_list_with_manager import DigitListWithManager


if __name__ == '__main__':
    repo = DigitListWithManager(4, 4)
    print(repo)
    print("left add_ability:", repo.use_ability())
    print(repo)
    print()
    print("x:1 y:2 |", repo.get_digit_by_x_y(1, 2))
    # print("x:3 y:4 |", repo.get_digit_by_x_y(3, 4))

    try:
        while True:
            print()
            x1, y1, x2, y2 = [int(elem) for elem in input("Enter x1, y1, x2, y2: ").strip().split(" ")]
            print("Score (check):", repo.check_digit_buttons(x1, y1, x2, y2))
            print("Score (lines):", repo.remove_checked_lines())
            print(repo)
    except KeyboardInterrupt:
        print("Goodbye")
