"""Contains useful functions"""
import os


def alphabetic_range(length: int):
    """Returns an alphabetical list of small caps letter with a certain length
    Adapted from: https://www.pythonpool.com/python-alphabet/"""
    if length > 26:
        return ValueError("Not enough letters in the alphabet!")
    return list(map(chr, range(97, (97+length))))


def cls():
    """Function allows to clear the console output
    From: https://stackoverflow.com/questions/517970/how-to-clear-the-interpreter-console"""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_hashtag_separation(length=55):
    print("#"*length)


def print_dashed_separation(length=55):
    print("-" * length)


def print_title(text):
    print_hashtag_separation(55)
    print(" "*int((55-len(text))/2)+text.upper())
    print_hashtag_separation(55)


def blank_separator():
    return print("\n")