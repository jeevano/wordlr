from main import wordle, algo, set_glob
from words import get_guesses, get_answers
from statistics import mean

answers = get_answers()
guesses = answers + get_guesses()

def game(soln):
    set_glob(soln, guesses, answers)
    return algo(answers, 5)

avg = mean([game(a) for a in answers[0:50]])
print(avg)
