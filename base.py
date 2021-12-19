"""Contains base classes"""

import random
import requests
import logging

from enum import Enum
from time import sleep


class Answer:

    def __init__(self, text: str, tf: bool):
        self._text = text
        self._tf = tf

    @property
    def text(self):
        return self._text

    @property
    def is_correct(self):
        return self._tf


class Question:

    def __init__(self, text: str, category: str, answers: list):
        self._text = text
        self._category = category
        self._answers = random.sample(answers, k=len(answers))
        # self._random_ordering_indices = random.sample(range(len(answers)), k=len(answers))

    @property
    def text(self):
        return self._text

    @property
    def category(self):
        return self._category

    @property
    def answers(self):
        return self._answers

    @property
    def correctness(self):
        return [ans.is_correct for ans in self._answers]

    @property
    def correct_answer(self):
        correct_answers = [ans for ans in self._answers if ans.is_correct is True]
        assert len(correct_answers) == 1
        return correct_answers[0]

    @property
    def wrong_answers(self):
        wrong_answers = [ans for ans in self._answers if ans.is_correct is False]
        assert len(wrong_answers) == len(self._answers) - 1
        return wrong_answers

    def validate_answer(self, answer_idx):
        correctness_seq = [ans.is_correct for ans in self._answers]
        return correctness_seq[answer_idx]


class Category(Enum):
    FoodAndDrink = ('Food and Drink', 'food_and_drink')
    Geography = ('Geography', 'geography')
    GeneralKnowledge = ('General Knowledge', 'general_knowledge')
    History = ('History', 'history')
    ArtAndLiterature = ('Art and Literature', 'literature')
    Movies = ('Movies', 'movies')
    Music = ('Music', 'music')
    Science = ('Science', 'science')
    SocietyAndCulture = ('Society and Culture', 'society_and_culture')
    SportAndLeisure = ('Sport and Leisure', 'sport_and_leisure')
    Unknown = ('-', '-')  # To catch unknown categories. Not to be used in queries

    @property
    def formatted_str(self):
        return self.value[0]

    @property
    def query_str(self):
        return self.value[1]

    @classmethod
    def list_formatted_str(cls):
        return [c.formatted_str for c in cls if c != Category.Unknown]  # exlude catch-all category

    @classmethod
    def list_query_str(cls):
        return [c.query_str for c in cls if c != Category.Unknown]  # exlude catch-all category

    @classmethod
    def map_from_query_str(cls, query_str):
        query_str_to_names_dict = {c.query_str: c.name for c in cls}
        if query_str in query_str_to_names_dict:
            return Category[query_str_to_names_dict[query_str]]
        return Category.Unknown

    @classmethod
    def map_from_formatted_str(cls, formatted_str):
        formatted_str_to_names_dict = {c.formatted_str: c.name for c in cls}
        if formatted_str in formatted_str_to_names_dict:
            return Category[formatted_str_to_names_dict[formatted_str]]
        return Category.Unknown


class QueryBuilder:
    QUESTION_TYPE = 'Multiple Choice'
    DEFAULT_LIMIT = 1

    def __init__(self):
        self._categories = []
        self._limit = self.DEFAULT_LIMIT

    def categories(self, values: list):
        if not isinstance(values, list):
            values = [values]
        for val in values:
            if val not in self._categories:
                logging.debug(f"Adding category '{val}' to query parameters")
                self._categories.append(val)
        return self

    def limit(self, value: int):
        self._limit = value
        logging.debug(f"Adding limit of {value} to query parameters")
        return self

    def _build_query_url(self):
        base_url = 'https://api.trivia.willfry.co.uk/questions'
        query_params = []
        if self._categories:
            cat_params = f"categories={','.join([cat.query_str for cat in self._categories])}"
            query_params.append(cat_params)
        limit_param = f"limit={self._limit}"
        query_params.append(limit_param)
        query_url = base_url if not query_params else base_url + f"?{'&'.join(query_params)}"
        logging.debug(f"Querying '{query_url}'")
        return query_url

    @staticmethod
    def _launch_single_query(query_url: str):
        response = requests.get(query_url)
        if not response or response.status_code != 200:
            return None
        response_data = response.json()
        return response_data

    def _validate(self, response_data: list):
        return [quest for quest in response_data if quest['type'] == self.QUESTION_TYPE]

    def _query(self, *args, **kwargs):
        response_data = self._launch_single_query(*args, **kwargs)
        success = False if response_data is None else True
        runs = 0
        while success is False and runs < 5:  # if API is unresponsive
            logging.debug(f"No response from the API. Waiting 3 seconds")
            sleep(3)
            response_data = self._launch_single_query(*args, **kwargs)
            runs += 1
            success = False if response_data is None else True
        if response_data is None:
            raise ConnectionError("Haven't been able to connect to the API")
        return response_data

    def _query_and_validate(self, *args, **kwargs):
        pass

    @staticmethod
    def _convert_raw_response(response_data):
        questions = []
        for raw_question in response_data:
            wrong_answers = [Answer(answer_text, False) for answer_text in raw_question['incorrectAnswers']]
            correct_answer = Answer(raw_question['correctAnswer'], True)
            answers = wrong_answers + [correct_answer]
            question_text = raw_question['question']
            question_category_str = raw_question['category']
            question_category = Category.map_from_formatted_str(question_category_str)
            questions.append(Question(question_text, question_category, answers))
        return questions

    def get_questions(self):
        query_url = self._build_query_url()
        raw_data = self._launch_single_query(query_url)
        validated_raw_data = self._validate(raw_data)
        questions = self._convert_raw_response(validated_raw_data)
        return questions


def query_trivia_api():
    """Entry-level method"""
    return QueryBuilder()


def query_random_question():
    return query_trivia_api().limit(1).get_questions()[0]


def query_question_in_category(category: Category):
    return query_trivia_api().categories([category]).limit(1).get_questions()


def query_3_questions():
    pass
