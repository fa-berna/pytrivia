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
from pytrivia.base import Category,\
    request_random_question,\
    request_3_questions,\
    request_question_in_category


class Round(ABC):
    """Abstract parent class for Round objects"""

    def __init__(self, number: int, initial_score: int, initial_success_streak: int):
        """Initializes an object of the Round class

        Parameters
        ----------
        number: int
            Round number
        initial_score: int
            Score at the start of the round
        initial_success_streak: int
            Success streak at the start of the round
        """
        self._number = number
        self._initial_score = initial_score
        self._initial_success_streak = initial_success_streak
        self._question = self._set_question()
        self._final_score = None
        self._final_success_streak = None

    @property
    def number(self):
        """

        Returns
        -------
        number: int
            Round number
        """
        return self._number

    @property
    def initial_score(self):
        """

        Returns
        -------
        initial_score: int
            Score at the start of the round
        """
        return self._initial_score

    @property
    def final_score(self):
        """

        Returns
        -------
        final_score: int
            Score at the end of the round (after the user input has been evaluated)
        """
        return self._final_score

    @property
    def initial_success_streak(self):
        """

        Returns
        -------
        initial_success_streak: int
            Success streak at the start of the round
        """
        return self._initial_success_streak

    @property
    def final_success_streak(self):
        """

        Returns
        -------
        final_success_streak:
            Success streak at the end of the round
        """
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
    """Class for regular rounds where the user faces a question with 4 possible answers and points are added (deducted)
    for correct (incorrect) answers"""

    POS_POINTS = 1  # points added for a good answer
    NEG_POINTS = 1  # points deducted for a bad answer

    def __init__(self, *args, **kwargs):
        """Instantiates an object of the class RegularRound

        Parameters
        ----------
        *args
            Variable length argument list.
        **kwargs
            Arbitrary keyword arguments.
        """
        super().__init__(*args, **kwargs)

    def _set_question(self):
        return request_random_question()

    def play(self):
        """Starts a round that requests a random question from the API and asks the user to input the index
        corresponding to the correct answer to a certain question.

        Returns
        -------

        """
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
    """Class for bonus rounds where the user is allowed to choose which question to answer amongst 3 possibles and then
    faces a question with 4 possible answers and points are added for correct answers."""

    POS_POINTS = 2  # points added for a good answer
    NEG_POINTS = 0  # points deducted for a bad answer

    def __init__(self, *args, **kwargs):
        """Instantiates an object of the class BonusRound

        Parameters
        ----------
        *args
            Variable length argument list.
        **kwargs
            Arbitrary keyword arguments.
        """
        super().__init__(*args, **kwargs)

    def _set_question(self):
        questions = request_3_questions()
        print_title("BONUS ROUND")
        blank_separator()
        print("In a BONUS ROUND you can choose the question that you want to answer")
        blank_separator()
        for i in range(3):
            print(f"{i + 1}) {questions[i].text}")
        blank_separator()
        input_idx = self._get_numeric_user_input("Choose the question that you want to answer: ", range(1, 4))
        blank_separator()
        return questions[input_idx - 1]

    def play(self):
        """Starts a round that requests 3 random questions from the API, asks the user to select which of the three
        questions to answer and then gives the user 4 possible answers to the chosen question.

        Returns
        -------

        """
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


class CategoryRound(Round):
    """Class for category rounds where the user is allowed to choose the category for the next question and then
    faces a question with 4 possible answers and points are added for correct answers."""

    POS_POINTS = 1  # points added for a good answer
    NEG_POINTS = 1  # points deducted for a bad answer

    def __init__(self, *args, **kwargs):
        """Instantiates an object of the class CategoryRound

        Parameters
        ----------
        *args
            Variable length argument list.
        **kwargs
            Arbitrary keyword arguments.
        """
        super().__init__(*args, **kwargs)

    def _set_question(self):
        print_title(f"ROUND {self.number}")
        blank_separator()
        print("You can choose the category for the next question")
        blank_separator()
        cat_dict = Category.list_formatted_str()
        for i in range(len(cat_dict)):
            print(f"{i+1}) {cat_dict[i]}")
        blank_separator()
        input_idx = self._get_numeric_user_input("Choose the category: ", range(1, len(cat_dict)+1))
        blank_separator()
        chosen_cat = Category.map_from_formatted_str(cat_dict[input_idx-1])
        question = request_question_in_category(chosen_cat)
        return question

    def play(self):
        """Starts a round that lists all the possible categories and asks the user to choose 1. Then, it procedes the
        same way as a normal round.

        Returns
        -------

        """
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


class Game:
    """Game is comprised of a series of rounds and stops when points reach 0 or below."""

    START_SCORE = 1
    START_ROUND = 0
    START_SUCCESS_STREAK = 0
    BONUS_ROUND_SUCCESS_STREAK_THRES = 3
    CACHE_FOLDER = 'cache/'

    def __init__(self):
        """Initializes an instance of Game"""
        self._rounds = []

    @property
    def high_score(self):
        """

        Returns
        -------
        int
            The highest score reached at any point during the game
        """
        return max([rnd.final_score for rnd in self._rounds] + [rnd.initial_score for rnd in self._rounds])

    @property
    def n_rounds(self):
        """

        Returns
        -------
        int
            The number of rounds played in the game
        """
        non_bonus_rounds = [rnd for rnd in self._rounds if not isinstance(rnd, BonusRound)]
        return len(non_bonus_rounds)

    @property
    def current_round_number(self):
        """

        Returns
        -------
        int
            The current round number
        """
        if len(self._rounds) > 0:
            non_bonus_rounds = [rnd for rnd in self._rounds if not isinstance(rnd, BonusRound)]
            return non_bonus_rounds[-1].number
        else:
            return self.START_ROUND

    @property
    def current_score(self):
        """

        Returns
        -------
        int
            The current score (end of previous round if round just started)
        """
        if len(self._rounds) > 0:
            return self._rounds[-1].final_score
        else:
            return self.START_SCORE

    @property
    def current_success_streak(self):
        """

        Returns
        -------
        int
            The current success streak (end of the previous round if round just started)
        """
        if len(self._rounds) > 0:
            return self._rounds[-1].final_success_streak
        else:
            return self.START_SUCCESS_STREAK

    @property
    def longest_success_streak(self):
        """

        Returns
        -------
        int
            The longest success streak at any point during the game
        """
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
        """Prints information about the score whenever the game ends."""
        print_title("GAME OVER")
        blank_separator()
        print("Game summary:")
        print(f"- High score: {self.high_score}")
        print(f"- Number of rounds: {self.n_rounds}")
        print(f"- Longest success streak: {self.longest_success_streak}")
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
            print(f"- Longest success streak: {cached_dict['success_streak']}")
        else:
            print("--No historical high score information--")
        blank_separator()

    def _show_home_screen(self):
        # Logo generated via: https://www.fancytextpro.com/BigTextGenerator/
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
        """Starts a while loop that launches one round after the other and ends whenever the score reaches 0 or below.

        Returns
        -------

        """
        # Initialize parameters for the game
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
            elif (round+1) % 5 == 0:  # condition should be entered when round == 4, 9, 14, 19, ...
                self._configure_next_round(CategoryRound)
                self._play_next_round()
                new_score = self._rounds[-1].final_score
                new_success_streak = self._rounds[-1].final_success_streak
                bonus_round = True if new_score > score and new_success_streak >= self.BONUS_ROUND_SUCCESS_STREAK_THRES else False
                score = new_score
                round += 1
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


def run_game_in_loop():
    """Function allows to play multiple games in a loop as long as the user does not decide to quit the application"""

    def _get_user_willingness_to_play():
        inpt = input("Press enter to start another game or enter 'q' to exit the application: ")
        if inpt == 'q':
            return False
        else:
            return True

    keep_playing = True

    while keep_playing:

        game = Game()
        game.play()

        keep_playing = _get_user_willingness_to_play()