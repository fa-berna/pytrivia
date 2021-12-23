from typing import Callable, Type
from abc import ABC, abstractmethod

from utils import print_title, blank_separator, alphabetic_range
from pytrivia.base import query_random_question, query_3_questions


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


class Round(ABC):
    """
    Abstract class for Round objects
    """

    def __init__(self, number, initial_score):
        self._number = number
        self._initial_score = initial_score
        self._question = self._set_question()
        self._final_score = None

    @property
    def number(self):
        return self._number

    @property
    def initial_score(self):
        return self._initial_score

    @property
    def final_score(self):
        return self._final_score

    @abstractmethod
    def _set_question(self):
        pass

    @abstractmethod
    def play(self):
        pass


class RegularRound(Round):

    POS_POINTS = 1  # points added for a good answer
    NEG_POINTS = 1  # points deducted for a bad answer

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _set_question(self):
        return query_random_question()

    def play(self):
        # get question and answers
        question = self._question
        answers = question.get_randomly_ordered_answers(n_max=4)
        category = question.category
        initial_score = self.initial_score
        round_n = self.number
        # structure answers in a dictionary
        dict_answers = {k: v for k, v in zip(alphabetic_range(len(answers)), answers)}
        # structure visual output
        print_title(f"ROUND {round_n}")
        blank_separator()
        print(f"Current score: {initial_score}")
        blank_separator()
        print(f"(Category: {category.formatted_str})")
        blank_separator()
        print(f"{question.text}")
        blank_separator()
        for key, ans in dict_answers.items():
            print(f"{key}) {ans.text}")
        blank_separator()
        input_key = input("Answer: ").lower()
        # check the input
        tf = dict_answers[input_key].is_correct
        if tf:
            print(f"GOOD! +{self.POS_POINTS} points")
            self._final_score = initial_score + self.POS_POINTS
        else:
            print(f"WRONG! -{self.NEG_POINTS} points")
            right_answer = question.correct_answer
            right_key = [k for k in dict_answers.keys() if dict_answers[k] == right_answer][0]
            print(f"The correct answer was: {right_key}) {right_answer.text}")
            self._final_score = initial_score - self.NEG_POINTS
        blank_separator()


class BonusRound(Round):

    POS_POINTS = 2  # points added for a good answer
    NEG_POINTS = 0  # points deducted for a bad answer

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _set_question(self):
        questions = query_3_questions()
        print_title("BONUS ROUND")
        blank_separator()
        print("In a BONUS ROUND you can choose the question that you want to answer")
        blank_separator()
        for i in range(3):
            print(f"{i+1}) {questions[i].text}")
        blank_separator()
        input_idx = int(input("Choose the question that you want to answer: "))
        blank_separator()
        return questions[input_idx-1]

    def play(self):
        # get question and answers
        question = self._question
        answers = question.get_randomly_ordered_answers(n_max=4)
        category = question.category
        initial_score = self.initial_score
        # structure answers in a dictionary
        dict_answers = {k: v for k, v in zip(alphabetic_range(len(answers)), answers)}
        # structure visual output
        print_title(f"BONUS ROUND")
        blank_separator()
        print(f"Current score: {initial_score}")
        blank_separator()
        print(f"(Category: {category.formatted_str})")
        blank_separator()
        print(f"{question.text}")
        blank_separator()
        for key, ans in dict_answers.items():
            print(f"{key}) {ans.text}")
        blank_separator()
        input_key = input("Answer: ").lower()
        # check the input
        tf = dict_answers[input_key].is_correct
        if tf:
            print(f"GOOD! +{self.POS_POINTS} points")
            self._final_score = initial_score + self.POS_POINTS
        else:
            print(f"WRONG! Don't worry, there was no point deduction")
            right_answer = question.correct_answer
            right_key = [k for k in dict_answers.keys() if dict_answers[k] == right_answer][0]
            print(f"The correct answer was: {right_key}) {right_answer.text}")
            self._final_score = initial_score - self.NEG_POINTS
        blank_separator()


class CategorySelectionRound(RegularRound):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _set_question(self):
        questions = query_3_questions()
        n_round = self.number
        print_title("BONUS ROUND")
        blank_separator()
        print("In a BONUS ROUND you can choose the question that you want to answer")
        blank_separator()
        for i in range(3):
            print(f"{i+1}) {questions[i].text}")
        blank_separator()
        input_idx = int(input("Choose the question that you want to answer: "))
        blank_separator()
        return questions[input_idx-1]


# class Settings:
#
#     def __init__(self, n_max_answers):
#         self.n_max = n_max_answers


class Game:
    """
    Game is comprised of a series of rounds and stops when points reach 0 or below.
    """
    START_SCORE = 1
    START_ROUND = 0
    START_STREAK = 0
    BONUS_ROUND_STREAK_THRES = 3

    def __init__(self):  # settings: Settings
        # self._settings = settings
        self._rounds = []

    @property
    def high_score(self):
        return max([rnd.final_score for rnd in self._rounds] + [rnd.initial_score for rnd in self._rounds])

    @property
    def n_rounds(self):
        return len(self._rounds)

    @property
    def current_round_number(self):
        if len(self._rounds) > 0:
            return self._rounds[-1].number
        else:
            return self.START_ROUND

    @property
    def current_score(self):
        if len(self._rounds) > 0:
            return self._rounds[-1].final_score
        else:
            return self.START_SCORE

    def _configure_next_round(self, round_class: Type[Round]):
        n_round = self.current_round_number + 1
        score = self.current_score
        next_round = round_class(n_round, score)
        self._rounds.append(next_round)

    def _play_next_round(self):
        next_round = self._rounds[-1]
        next_round.play()

    def _show_game_over(self):
        print_title("GAME OVER")
        blank_separator()
        print("Summary:")
        print(f"- High score: {self.high_score}")
        print(f"- Number of rounds: {self.n_rounds}")
        blank_separator()

    def _show_home_screen(self):
        # Generated by: https://www.fancytextpro.com/BigTextGenerator/
        message = """

                        Welcome to

            ____       ______     _       _      
           / __ \__  _/_  __/____(_)   __(_)___ _
          / /_/ / / / // / / ___/ / | / / / __ `/
         / ____/ /_/ // / / /  / /| |/ / / /_/ / 
        /_/    \__, //_/ /_/  /_/ |___/_/\__,_/  
              /____/         

                  Press Enter to continue                                           
            """
        _ = input(message)
        blank_separator()

    def play(self):
        # initialize parameters for looping
        score = self.START_SCORE
        round = self.START_ROUND
        streak = self.START_STREAK
        bonus_round = False
        # home screen
        self._show_home_screen()
        # loop during game
        while score > 0:
            if bonus_round:
                self._configure_next_round(BonusRound)
                self._play_next_round()
                new_score = self._rounds[-1].final_score
                bonus_round = False
                score = new_score
            else:
                self._configure_next_round(RegularRound)
                self._play_next_round()
                new_score = self._rounds[-1].final_score
                if new_score > score:
                    streak += 1
                    if streak >= self.BONUS_ROUND_STREAK_THRES:
                        bonus_round = True
                else:
                    streak = self.START_STREAK
                    bonus_round = False
                score = new_score
                round += 1
        # game over
        self._show_game_over()

