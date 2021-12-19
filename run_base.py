from base import query_trivia_api, Category, query_random_question
import logging

handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)

questions = query_trivia_api().limit(5).get_questions()
print(questions)

question = query_random_question()
print(question)
