"""Contains useful functions"""
import os
import json


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


def create_folder_if_missing(path_to_folder):
    """Based on: https://www.geeksforgeeks.org/create-a-directory-in-python/"""
    if not os.path.exists(path_to_folder):
        os.makedirs(path_to_folder)


def create_file_if_missing(path_to_file):
    """Based on: https://stackoverflow.com/questions/35807605/create-a-file-if-it-doesnt-exist"""
    if not os.path.exists(path_to_file):
        with open(path_to_file, 'w'):
            pass


def read_json_file_to_dict(path_to_file):
    """Based on https://devenum.com/how-to-convert-text-file-to-a-dictionary-in-python/"""
    dict = {}
    if os.path.exists(path_to_file):
        with open(path_to_file, 'r') as f:
            dict = json.load(f)
            return dict
    return None


def write_dict_to_json_file(dict, path_to_file):
    create_file_if_missing(path_to_file)
    with open(path_to_file, 'w') as f:
        json.dump(dict, f)
