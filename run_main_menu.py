from pytrivia.game import Menu, MenuOption
import sys

def myfun():
    print(2)


option1 = MenuOption("Option1", lambda: print(1))
option2 = MenuOption("Option2", myfun)
option3 = MenuOption("Quit", sys.exit)

menu = Menu()
menu.add_menu_option(option1)
menu.add_menu_option(option2)
menu.add_menu_option(option3)

menu.show()