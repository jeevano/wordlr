def get_guesses():
    return get_words("valid_guesses")

def get_answers():
    return get_words("answer_bank")

def get_words(filename):
    list = []
    with open("./res/{0}.txt".format(filename)) as f:
        for line in f:
            list.append(line.strip())
    return list
