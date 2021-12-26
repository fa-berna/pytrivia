"""Contains base classes"""

import random
import requests

from enum import Enum
from time import sleep


class Category(Enum):
    """Enumerates all the possible question categories"""

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
        """

        Returns
        -------
        str
            Category name formatted for printing
        """
        return self.value[0]

    @property
    def query_str(self):
        """

        Returns
        -------
        str
            Category name in the format needed for querying
        """
        return self.value[1]

    @classmethod
    def list_formatted_str(cls):
        """Returns a  list of all the category names formatted for printing (with the exception of the Unknown
        category).

        Returns
        -------
        list of str
            List of all the category names formatted for printing (with the exception of the Unknown category).
        """
        return [c.formatted_str for c in cls if c != Category.Unknown]  # exlude catch-all category

    @classmethod
    def list_query_str(cls):
        """Returns a list of all the category names formatted for querying (with the exception of the Unknown category).

        Returns
        -------
        list of str
            List of all the category names formatted for querying (with the exception of the Unknown category).
        """
        return [c.query_str for c in cls if c != Category.Unknown]  # exlude catch-all category

    @classmethod
    def map_from_query_str(cls, query_str):
        """Maps categories in query string form to the corresponding Category class (if it can be found). Otherwise,
        it's mapped to the Category.Unknown.

        Parameters
        ----------
        query_str: str
            Category name in query string format

        Returns
        -------
        Category
            Corresponding Category class
        """
        query_str_to_names_dict = {c.query_str: c.name for c in cls}
        if query_str in query_str_to_names_dict:
            return Category[query_str_to_names_dict[query_str]]
        return Category.Unknown

    @classmethod
    def map_from_formatted_str(cls, formatted_str):
        """Maps categories in query format for printing to the corresponding Category (if it's found). Otherwise, it's
        mapped to the Category.Unknown.

        Parameters
        ----------
        formatted_str: str
            Category name formatted for printing

        Returns
        -------
        Category
            Corresponding Category
        """
        formatted_str_to_names_dict = {c.formatted_str: c.name for c in cls}
        if formatted_str in formatted_str_to_names_dict:
            return Category[formatted_str_to_names_dict[formatted_str]]
        return Category.Unknown


class Answer:
    """Answer base class"""

    def __init__(self, text: str, tf: bool):
        """Initializes an Answer object

        Parameters
        ----------
        text: str
            Answer in string form
        tf: bool
            Boolean indicating whether the answer is the correct (True) or wrong (False) to its corresponding question
        """
        self._text = text
        self._tf = tf

    @property
    def text(self):
        """

        Returns
        -------
        text: str
            Answer in string form
        """
        return self._text

    @property
    def is_correct(self):
        """

        Returns
        -------
        tf: bool
            Boolean indicating whether the answer is the correct (True) or wrong (False) to its corresponding question
        """
        return self._tf


class Question:
    """Question base class"""

    def __init__(self, text: str, category: Category, answers: list):
        """Initializes a Question object

        Parameters
        ----------
        text: str
            Question in string form
        category: Category
            The category of the question
        answers: list of Answer
            All the possible answers to the question.
        """
        self._text = text
        self._category = category
        self._answers = answers
        self._random_ordering_indices = random.sample(range(len(answers)), k=len(answers))

    @property
    def text(self):
        """

        Returns
        -------
        text: str
            Question in string form
        """
        return self._text

    @property
    def category(self):
        """

        Returns
        -------
        category: Category
            The category of the question
        """
        return self._category

    @property
    def correct_answer(self):
        """

        Returns
        -------
        Answer
            The correct answer to the question
        """
        correct_answers = [ans for ans in self._answers if ans.is_correct is True]
        assert len(correct_answers) == 1
        return correct_answers[0]

    @property
    def wrong_answers(self):
        """

        Returns
        -------
        list of Answer
            A list of the wrong answers to the question
        """
        wrong_answers = [ans for ans in self._answers if ans.is_correct is False]
        assert len(wrong_answers) == len(self._answers) - 1
        return wrong_answers

    def get_randomly_ordered_answers(self, n_max=None):
        """Returns a list of randomly-ordered answers to the question (always includes the correct answer)

        Parameters
        ----------
        n_max: int
            A restriction on the number of possible answers to the question. If None: no restriction and all the answers
            returned by the API will be used

        Returns
        -------
        list of Answer
        """
        n_max = len(self._answers) if n_max is None else min(n_max, len(self._answers))
        answers_to_combine = random.sample(self.wrong_answers, k=n_max-1) + [self.correct_answer]
        assert sum([ans.is_correct for ans in answers_to_combine]) == 1
        return random.sample(answers_to_combine, k=n_max)


class RequestBuilder:
    """Class with a fluent syntax that can be used to send requests to the Trivia API."""

    QUESTION_TYPE = 'Multiple Choice'
    DEFAULT_LIMIT = 1

    def __init__(self):
        """Initializes a RequestBuilder object"""
        self._categories = []
        self._limit = self.DEFAULT_LIMIT

    def categories(self, values: list):
        """Allows to add a Category (or multiple categories) to the request parameters.

        Parameters
        ----------
        values: list of Category
            Categories to be included in the request

        Returns
        -------
        self
        """
        if not isinstance(values, list):
            values = [values]
        for val in values:
            if val not in self._categories:
                self._categories.append(val)
        return self

    def limit(self, value: int):
        """Allows to limit the number of questions to be returned through the limit request parameter.

        Parameters
        ----------
        value: int
            Number of questions to be included in the request.

        Returns
        -------
        self
        """
        self._limit = value
        return self

    def _build_request_url(self):
        base_url = 'https://api.trivia.willfry.co.uk/questions'
        request_params = []
        if self._categories:
            cat_params = f"categories={','.join([cat.query_str for cat in self._categories])}"
            request_params.append(cat_params)
        limit_param = f"limit={self._limit}"
        request_params.append(limit_param)
        query_url = base_url if not request_params else base_url + f"?{'&'.join(request_params)}"
        return query_url

    @staticmethod
    def _send_single_request(query_url: str):
        response = requests.get(query_url)
        if not response or response.status_code != 200:
            return None
        response_data = response.json()
        return response_data

    def _validate(self, response_data: list):
        return [quest for quest in response_data if quest['type'] == self.QUESTION_TYPE]

    def _send(self, *args, **kwargs):
        response_data = self._send_single_request(*args, **kwargs)
        success = False if response_data is None else True
        runs = 0
        while success is False and runs < 5:  # if API is unresponsive
            sleep(3)
            response_data = self._send_single_request(*args, **kwargs)
            runs += 1
            success = False if response_data is None else True
        if response_data is None:
            raise ConnectionError("Haven't been able to connect to the API")
        return response_data

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
        """Builds the request URL, sends the request, validates the results and converts the raw response to Question instances

        Returns
        -------
        list of Question instances
        """
        request_url = self._build_request_url()
        raw_data = self._send_single_request(request_url)
        validated_raw_data = self._validate(raw_data)
        questions = self._convert_raw_response(validated_raw_data)
        return questions


def request_from_trivia_api():
    """Entry-level method"""
    return RequestBuilder()


def request_random_question():
    return request_from_trivia_api().limit(1).get_questions()[0]


def request_question_in_category(category: Category):
    return request_from_trivia_api().categories([category]).limit(1).get_questions()


def request_3_questions():
    return request_from_trivia_api().limit(3).get_questions()