"""Contains useful functions"""
from base import Question

def alphabetic_range(length: int):
    """Adapted from: https://www.pythonpool.com/python-alphabet/"""
    if length > 26:
        return ValueError("Not enough letters in the alphabet!")
    return list(map(chr, range(97, (97+length))))


def dictionarise_answers(question: Question, n_max: int=None):
    answers = question.answers
    dict_answers = {k: v for k, v in zip(alphabetic_range(len(answers)), answers)}