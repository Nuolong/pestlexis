#!/usr/bin/env python3

import json
import random
import time
from utils import debug

# default numbers - quite useless
TWO = 86400
THREE = 604800
FOUR = 1209600
FIVE = 1814400

# settings in seconds
def load_setting():
    debug("In load_setting")
    global TWO, THREE, FOUR, FIVE

    with open("../data/user/settings.json", "r") as settings:
        settings_dict = json.load(settings)

    TWO = settings_dict['2']
    THREE = settings_dict['3']
    FOUR = settings_dict['4']
    FIVE = settings_dict['5']
    return [TWO, THREE, FOUR, FIVE]

# load settings on startup
load_setting()

# finds a word in progress ready to be trained
def choose_word():
    with open("../data/user/progress.json", "r") as prog:
        prog_json = json.load(prog)

    if prog_json['1']:
        word, _ = prog_json['1'][0]
        return word, '1'

    # yes, I could avoid code duplication here but that's a later-job
    if prog_json['2']:
        word, logged = prog_json['2'][0]
        print(time.time() - logged)
        print(TWO)
        if time.time() - logged >= TWO:
            return word, '2'

    if prog_json['3']:
        word, logged = prog_json['3'][0]
        if time.time() - logged >= THREE:
            return word, '3'

    if prog_json['4']:
        word, logged = prog_json['4'][0]
        if time.time() - logged >= FOUR:
            return word, '4'

    if prog_json['5']:
        word, logged = prog_json['5'][0]
        if time.time() - logged >= FIVE:
            return word, '5'

    # no words ready to be trained\
    return None, None

# returns a (word, meaning, roman*) ready to be trained
def get_word():
    word, lvl = choose_word()

    # if no words need to be trained currently
    if word is None:
        return None, None, None, None

    with open("../data/user/dict.json", "r") as words:
        words_json = json.load(words)

    meaning = words_json[word]['definitions']
    try:
        roman = words_json[word]['romanization']
    except KeyError:
        roman = None

    return word, meaning, roman, lvl

# checks if input is correct
def validate(word, *args):
    tx_def = args[0]
    if len(args) == 2:
        et_roman = args[1]

    def_inp = [x.strip() for x in tx_def.get("1.0", "end").split(",")]
    try:
        roman_inp = et_roman.get()
    except NameError:
        roman_inp = None

    with open("../data/user/dict.json", "r") as words:
        words_json = json.load(words)

    # check valid definitions
    for defi in def_inp:
        if defi.lower() not in map(str.lower, words_json[word]['definitions']):
            tx_def.config(fg='green')
            tx_def.delete("1.0", "end")
            tx_def.insert("end", ", ".join(words_json[word]['definitions']))
            if roman_inp is not None:
                et_roman.config(fg='green')
                et_roman.delete(0, "end")
                et_roman.insert(0, words_json[word]['romanization'])
            return False
        continue

    # check valid romanization
    if roman_inp is not None:
        if roman_inp.lower().strip() != words_json[word]['romanization'].lower().strip():
            tx_def.config(fg='green')
            tx_def.delete("1.0", "end")
            tx_def.insert("end", ", ".join(words_json[word]['definitions']))
            et_roman.config(fg='green')
            et_roman.delete(0, "end")
            et_roman.insert(0, words_json[word]['romanization'])
            return False

    return True

# move word to next level in progress
def correct(word, lvl):
    with open("../data/user/progress.json", "r") as prog:
        prog_json = json.load(prog)

    # the word _will_ be in the front of the queue
    word_test = prog_json[lvl].pop(0)

    # maybe don't even need to pass word parameter - test later
    if lvl == '5':
        prog_json[lvl].append((word_test[0], int(time.time())))
    else:
        lvl = int(lvl)
        lvl += 1
        lvl = str(lvl)
        prog_json[lvl].append((word_test[0], int(time.time())))

    with open("../data/user/progress.json", "w") as prog_out:
        json.dump(prog_json, prog_out, ensure_ascii = False)

    return 'Correct!'

# move word back to level 1
def incorrect(word, lvl):
    with open("../data/user/progress.json", "r") as prog:
        prog_json = json.load(prog)

    word_test = prog_json[lvl].pop(0)
    prog_json['1'].append((word_test[0], int(time.time())))

    with open("../data/user/progress.json", "w") as prog_out:
        json.dump(prog_json, prog_out, ensure_ascii = False)

    return 'Incorrect.'
