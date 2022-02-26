from words import get_guesses, get_answers
import random

################################ Helper methods ################################
def run():
    answers = get_answers()
    guesses = answers + get_guesses()
    soln = random.choice(answers)

    set_glob(soln, guesses, answers)
    print("Solution: {}".format(soln))
    print(algo(answers, 5))

def set_glob(in_sol, in_guesses, in_answers):
    global soln
    global guesses
    global answers
    soln = in_sol
    guesses = in_guesses
    answers = in_answers
################################################################################

################################# Game methods #################################
# Output is 5x1 tuple of in-place rating of characters.
# 0 == not in answer
# 1 == in answer, wrong position
# 2 == in answer, right position
def wordle(guess, ans = None):
    global soln
    if not ans:
        ans = soln
    out = [0 for i in range(5)]
    for c in range(5):
        if guess[c] == ans[c]:
            out[c] = 2
            ans = ans[:c] + '#' + ans[c + 1:]
    for c in range(5):
        if guess[c] in ans and out[c] == 0:
            out[c] = 1
            x = ans.find(guess[c])
            ans = ans[:x] + '#' + ans[x + 1:]
    return tuple(out)
################################################################################

################################# Algo methods #################################
# Core algorithm behind the game
def best_guess(possible_answers, my_guesses):
    # Find the guess that will leave us with the smallest possible answer pool.
    best_case = 1e6
    for g in my_guesses:
        scenario = {}
        for a in possible_answers:
            eval = wordle(g, a)
            if eval not in scenario:
                scenario[eval] = [a]
            else:
                scenario[eval].append(a)
        # the worst possible case for current guess (we want to minimize this).
        worst_case = max([len(val) for val in scenario.values()])
        if worst_case < best_case:
            best_case = worst_case
            my_guess = g
            best_scenario = scenario

    return best_scenario, my_guess

# Algorithmically narrow down the possibilities at each guess, until there is only 1 possible answer.
# I made it recursive for fun, even though I know it's inefficient tail recursion :p
def algo(possible_answers, guesses_left):
    global guesses
    # Base case.
    if guesses_left == 0 or len(possible_answers) == 1:
        print("Guess #{}: {}".format(6 - guesses_left, possible_answers[0]))
        return 6 - guesses_left
    # Initial guess.
    elif guesses_left == 5:
        my_guesses = ["salet"]
    # Guess pool.
    else:
        my_guesses = guesses

    best_scenario, my_guess = best_guess(possible_answers, my_guesses)
    possible_answers = best_scenario[wordle(my_guess)]

    print("Guess #{}: {}".format(6 - guesses_left, my_guess))

    return algo(possible_answers, guesses_left - 1)
################################################################################

# run()
