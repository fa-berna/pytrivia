import keyboard
from pytrivia.utils import cls

selected = 1


class NavigationMenu:

    def __init__(self):
        self._selected = 1
        self._options = ["Do something 1", "Do something 2", "Do something 3", "Do something 4"]

    def _show_menu(self):
        print("Choose an option:")
        for i in range(len(self._options)):
            print(f"{'>' if selected == i else ' '} {i}.{self._options[i]} {'<' if selected == i else ' '}")

    def _up(self):
        if self._selected == 1:
            return
        self._selected -= 1
        cls()
        self._show_menu()

    def _down(self):
        if self._selected == 4:
            return
        self._selected += 1
        cls()
        self._show_menu()


def run_menu():
    menu = NavigationMenu()
    keyboard.add_hotkey('up', menu._up)
    keyboard.add_hotkey('down', menu._down)
    keyboard.wait()

# def show_menu():
#     global selected
#     # print("\n" * 30)
#     print("Choose an option:")
#     for i in range(1, 5):
#         print("{1} {0}. Do something {0} {2}".format(i, ">" if selected == i else " ", "<" if selected == i else " "))
#
#
# def up():
#     global selected
#     if selected == 1:
#         return
#     selected -= 1
#     cls()
#     show_menu()
#
#
# def down():
#     global selected
#     if selected == 4:
#         return
#     selected += 1
#     cls()
#     show_menu()


# show_menu()
# keyboard.add_hotkey('up', up)
# keyboard.add_hotkey('down', down)
# keyboard.wait()

run_menu()