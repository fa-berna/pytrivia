from typing import Callable, Type
from abc import ABC, abstractmethod

from pytrivia.utils import print_title,\
    blank_separator,\
    alphabetic_range,\
    create_folder_if_missing
from pytrivia.base import query_random_question,\
    query_3_questions


class MenuOption:

    def __init__(self, name: str, action: Callable):
        self._action = action
        self._name = name

    @property
    def action(self):
        return self._action

    @property
    def name(self):
        return self._name


class Menu:

    def __init__(self):
        self._options_dict = {}

    def add_menu_option(self, option: MenuOption):
        """
        Allows to add one option to the menu

        :param option: MenuOption object
        :return:
        """
        if not isinstance(option, MenuOption):
            raise ValueError("Option is not an object of type MenuOption")
        self._options_dict[len(self._options_dict)+1] = option

    def show(self):
        """
        Prints the menu

        :return:
        """
        print_title("MENU")
        blank_separator()
        dict_options = self._options_dict
        for option_idx in dict_options:
            print(f"{option_idx}. {dict_options[option_idx].name}")
        blank_separator()
        input_idx = self._get_user_input()
        return self._map_option_to_callable(input_idx)

    def _get_user_input(self):
        inpt = input("Choose: ")
        if inpt.isdigit() and int(inpt) in self._options_dict:
            return int(inpt)
        else:
            print("Invalid input!")
            return self._get_user_input()

    def _map_option_to_callable(self, idx):
        return self._options_dict[idx].action()

