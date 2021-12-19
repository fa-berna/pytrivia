from base import Category, query_random_question
from utils import alphabetic_range

points = 1

cached_questions = {}

print("#######################################################")
print("                     SETUP")
print("#######################################################")

pos_pts = int(input("Choose number of points that you gain for each good answer: "))
neg_pts = int(input("Choose number of points that you lose for each good answer: "))

max_answers = input("Choose the max. number of possible answers (blank = no restriction): ")

print("\n")

while points > 0:
    question_success_flag = 0
    while question_success_flag == 0:
        question = query_random_question()
        if question.text not in cached_questions:
            question_success_flag = 1
            cached_questions[question.text] = question
    answers = question.answers
    print("#######################################################")
    print("\n")
    print(f"Current points: {points}")
    print("\n")
    print(f"(Category: {question.category.formatted_str})")
    print("\n")
    print(f"{question.text}")
    print("-------------------------------------------------------")
    dict_answers = {k: v for k, v in zip(alphabetic_range(len(answers)), answers)}
    for key, ans in dict_answers.items():
        print(f"{key}) {ans.text}")
    print("\n")
    input_key, input_count = None, 0
    while input_key not in dict_answers.keys():
        if input_count > 0:
            print("Invalid input!")
        input_key = input("Answer: ").lower()
        input_count += 1
    tf = dict_answers[input_key].is_correct
    if tf:
        points += pos_pts
        print("GOOD!")
    else:
        points -= neg_pts
        print("WRONG!")
        right_answer = question.correct_answer
        right_key = [k for k in dict_answers.keys() if dict_answers[k] == right_answer][0]
        print(f"The correct answer was: {right_key}) {right_answer.text}")
    _ = input("Press enter to continue")
    print("\n")

print("#######################################################")
print("                     GAME OVER")
print("#######################################################")
