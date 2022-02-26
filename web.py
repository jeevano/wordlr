import selenium
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from words import get_guesses, get_answers
from main import best_guess

def enter_guess(guess, turn):
    global page
    page.send_keys(guess)
    page.send_keys(Keys.ENTER)
    time.sleep(2)
    return read_result(turn)

def read_result(turn):
    global driver
    script = "return document.querySelector('game-app').shadowRoot.querySelectorAll('game-row')[{}].shadowRoot.querySelector('div.row')".format(turn)
    row = driver.execute_script(script)
    tiles = row.find_elements(By.TAG_NAME, "game-tile")
    out = []
    for tile in tiles:
        # evaluation is correct || absent || present
        eval = tile.get_attribute("evaluation")
        if eval == "correct":
            out.append(2)
        elif eval == "present":
            out.append(1)
        else:
            out.append(0)
    return tuple(out)

def play(possible_answers, guesses_left):
    global guesses
    if guesses_left == 0 or len(possible_answers) == 1:
        enter_guess(possible_answers[0], 5)
        return 6 - guesses_left
    elif guesses_left == 5:
        my_guesses = ["soare"]
    else:
        my_guesses = guesses

    best_scenario, my_guess = best_guess(possible_answers, my_guesses)
    possible_answers = best_scenario[enter_guess(my_guess, 5 - guesses_left)]

    return play(possible_answers, guesses_left - 1)

answers = get_answers()
guesses = answers + get_guesses()

driver = webdriver.Safari()
driver.get("https://www.nytimes.com/games/wordle/index.html")
time.sleep(1)
page = driver.find_element(By.TAG_NAME, "html")
page.click()
time.sleep(1)

play(answers, 5)

time.sleep(10)
driver.quit()
