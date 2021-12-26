# PyTrivia

**Pytrivia** is a quiz game that tests your general knowledge through questions that range across 10 different 
categories. It is built based on Will Fry's free to use Trivia API (https://trivia.willfry.co.uk/). Its questions are 
procedurally generated and user generated. 


## How the game works

You start the game with a **score** of 1 and the game is over whenever your score reaches 0. You start with a **success 
streak count** of 0 and 1 point is added for each consecutive correct answer to a regular round question. 
Each time you answer incorrectly in a regular round, the streak count is reset to 0. 

In a **regular round**, you will be asked to choose amongst 4 possible answers by typing the letter corresponding to that 
answer. A correct answer will give you one point, a bad answer will take you one point away.

For every 4 regular rounds (i.e. in rounds 5, 10, 15, 20, ...), there will be one **category round** where you will 
have the opportunity to chose the category for that round's question. As in a regular round, a correct answer will 
give you one point, a bad answer will take you one point away.

If you reach a streak count of 3, you will be able to play a **bonus round**: you will be asked to chose which amongst
3 possible questions you want to answer and will receive 2 points for a correct answer. In such a round there will be 
no point deduction for a wrong answer. A bonus round is always followed and preceded by regular rounds.
If you answer correctly to the question in the regular round following a bonus round (independently of your answer in the
bonus round), you will have the chance to play another bonus round.

Your high scores will be cached in a temporary cache folder within a JSON file. If you delete the cache/ folder, you 
will reset your high score. 


## How to run the code

1. Clone the repository
2. Either:
    a) manually install all the libraries needed and listed in ``requirements.txt`` via the PIP (you can automate 
    this by running ``pip install -r requirements.txt``) 
    b) setup a virtual environment via `python3 -m venv venv/`, run the command to activate the virtual environment
     (in Windows: `venv\Scripts\activate.bat`) and then install the packages in the virtual environment via 
     ``pip install -r requirements.txt``
3. Run the game by running the ``run_game.py`` file (if you used a virutal environment in 2, make sure it is active 
for this step to work).


## Notes

- An internet connection is needed to connect to the Trivia API.
- Game was developed on Python 3.8.10


## Credits

- Will Fry's Trivia API (https://trivia.willfry.co.uk/)