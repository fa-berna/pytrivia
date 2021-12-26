from typing import Callable, Type
from abc import ABC, abstractmethod
from datetime import datetime

from pytrivia.utils import print_title,\
    blank_separator,\
    alphabetic_range,\
    create_folder_if_missing, \
    create_file_if_missing, \
    read_json_file_to_dict, \
    write_dict_to_json_file
from pytrivia.base import query_random_question,\
    query_3_questions


class Round(ABC):
    """
    Abstract class for Round objects
    """

    def __init__(self, number, initial_score, initial_success_streak):
        self._number = number
        self._initial_score = initial_score
        self._initial_success_streak = initial_success_streak
        self._question = self._set_question()
        self._final_score = None
        self._final_success_streak = None

    @property
    def number(self):
        return self._number

    @property
    def initial_score(self):
        return self._initial_score

    @property
    def final_score(self):
        return self._final_score

    @property
    def initial_success_streak(self):
        return self._initial_success_streak

    @property
    def final_success_streak(self):
        return self._final_success_streak

    @abstractmethod
    def _set_question(self):
        pass

    @abstractmethod
    def play(self):
        pass

    def _get_numeric_user_input(self, text, possible_answers):
        inpt = input(text)
        if inpt.isdigit() and int(inpt) in possible_answers:
            return int(inpt)
        else:
            print("Invalid input!")
            return self._get_numeric_user_input(text, possible_answers)

    def _get_string_user_input(self, text, possible_answers):
        inpt = input(text)
        if inpt in possible_answers:
            return inpt
        else:
            print("Invalid input!")
            return self._get_string_user_input(text, possible_answers)


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
        success_streak = self.initial_success_streak
        round_n = self.number
        # structure answers in a dictionary
        dict_answers = {k: v for k, v in zip(alphabetic_range(len(answers)), answers)}
        # structure visual output
        print_title(f"ROUND {round_n}")
        blank_separator()
        print(f"Current score: {initial_score}")
        blank_separator()
        print(f"Current success streak: {success_streak}")
        blank_separator()
        print(f"(Category: {category.formatted_str})")
        blank_separator()
        print(f"{question.text}")
        blank_separator()
        for key, ans in dict_answers.items():
            print(f"{key}) {ans.text}")
        blank_separator()
        input_key = self._get_string_user_input("Answer: ", dict_answers.keys())
        # check the input
        tf = dict_answers[input_key].is_correct
        if tf:
            print(f"GOOD! +{self.POS_POINTS} points")
            self._final_score = initial_score + self.POS_POINTS
            self._final_success_streak = success_streak + 1
        else:
            print(f"WRONG! -{self.NEG_POINTS} points")
            right_answer = question.correct_answer
            right_key = [k for k in dict_answers.keys() if dict_answers[k] == right_answer][0]
            print(f"The correct answer was: {right_key}) {right_answer.text}")
            self._final_score = initial_score - self.NEG_POINTS
            self._final_success_streak = 0
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
        input_idx = self._get_numeric_user_input("Choose the question that you want to answer: ", range(1, 4))
        blank_separator()
        return questions[input_idx-1]

    def play(self):
        # get question and answers
        question = self._question
        answers = question.get_randomly_ordered_answers(n_max=4)
        category = question.category
        initial_score = self.initial_score
        success_streak = self.initial_success_streak
        # structure answers in a dictionary
        dict_answers = {k: v for k, v in zip(alphabetic_range(len(answers)), answers)}
        # structure visual output
        print_title(f"BONUS ROUND")
        blank_separator()
        print(f"Current score: {initial_score}")
        blank_separator()
        print(f"Current success streak: {success_streak}")
        blank_separator()
        print(f"(Category: {category.formatted_str})")
        blank_separator()
        print(f"{question.text}")
        blank_separator()
        for key, ans in dict_answers.items():
            print(f"{key}) {ans.text}")
        blank_separator()
        input_key = self._get_string_user_input("Answer: ", dict_answers.keys())
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
        self._final_success_streak = success_streak  # bonus rounds do not count towards success streak count
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
    START_SUCCESS_STREAK = 0
    BONUS_ROUND_SUCCESS_STREAK_THRES = 3
    CACHE_FOLDER = 'cache/'

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

    @property
    def current_success_streak(self):
        if len(self._rounds) > 0:
            return self._rounds[-1].final_success_streak
        else:
            return self.START_SUCCESS_STREAK

    @property
    def longest_success_streak(self):
        return max([rnd.final_success_streak for rnd in self._rounds] +
                   [rnd.initial_success_streak for rnd in self._rounds])

    def _configure_next_round(self, round_class: Type[Round]):
        n_round = self.current_round_number + 1
        score = self.current_score
        success_streak = self.current_success_streak
        next_round = round_class(n_round, score, success_streak)
        self._rounds.append(next_round)

    def _play_next_round(self):
        next_round = self._rounds[-1]
        next_round.play()

    def _show_game_over(self):
        print_title("GAME OVER")
        blank_separator()
        print("Game summary:")
        print(f"- High score: {self.high_score}")
        print(f"- Number of rounds: {self.n_rounds}")
        print(f"- Longest success streak {self.longest_success_streak}")
        blank_separator()
        cached_dict = read_json_file_to_dict(self.CACHE_FOLDER + 'cache.json')
        if cached_dict is None:
            print("***Congratulations: you set a new high score!***")
            print("***Congratulations: you set a new record for the number of rounds played!***")
            print("***Congratulations: you set a new record for longest success streak!***")
        else:
            if self.high_score > cached_dict['score'] or cached_dict is None:
                print("***Congratulations: you set a new high score!***")
            if self.n_rounds > cached_dict['n_rounds'] or cached_dict is None:
                print("***Congratulations: you set a new record for the number of rounds played!***")
            if self.longest_success_streak > cached_dict['success_streak'] or cached_dict is None:
                print("***Congratulations: you set a new record for longest success streak!***")
        blank_separator()
        if cached_dict is not None:
            print("Historical high score summary:")
            print(f"- High score: {cached_dict['score']}")
            print(f"- Number of rounds: {cached_dict['n_rounds']}")
            print(f"- Longest success streak {cached_dict['success_streak']}")
        else:
            print("--No historical high score information--")

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

    def _save_score(self):
        cache_dict = read_json_file_to_dict(self.CACHE_FOLDER + 'cache.json')
        game_score = self.high_score
        game_n_rounds = self.n_rounds
        game_success_streak = self.longest_success_streak
        if not cache_dict:
            cache_dict = {'score': game_score,
                          'n_rounds': game_n_rounds,
                          'success_streak': game_success_streak}
        else:
            if game_score > cache_dict['score']:
                cache_dict['score'] = game_score  # overwrite
            if game_n_rounds > cache_dict['n_rounds']:
                cache_dict['n_rounds'] = game_n_rounds
            if game_success_streak > cache_dict['success_streak']:
                cache_dict['success_streak'] = game_success_streak
        write_dict_to_json_file(cache_dict, self.CACHE_FOLDER + 'cache.json')

    def play(self):
        # initialize parameters for looping
        score = self.START_SCORE
        round = self.START_ROUND
        bonus_round = False
        # home screen
        self._show_home_screen()
        # create cache folder if missing
        create_folder_if_missing(self.CACHE_FOLDER)
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
                new_success_streak = self._rounds[-1].final_success_streak
                bonus_round = True if new_score > score and new_success_streak >= self.BONUS_ROUND_SUCCESS_STREAK_THRES else False
                score = new_score
                round += 1
        # game over
        self._show_game_over()
        # save the score
        self._save_score()

