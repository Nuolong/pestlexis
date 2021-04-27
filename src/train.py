#!/usr/bin/env python3

import json
import random

# TODO: currently dummy: make configurable
TWO = 86400
THREE = 86400*2
FOUR = 86400*3
FIVE = 86400*4

# finds a word in progress ready to be trained
def choose_word():
    with open("../data/user/progress.json", "r") as prog:
        prog_json = json.load(prog)

    if prog_json['1']:
        word, _ = prog_json['1']
        return word, '1'

    # yes, I could avoid code duplication here but that's a later-job
    if prog_json['2']:
        word, logged = prog_json['2'][0]
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

    # no words ready to be trained
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

# move word to next level in progress
def correct(word, lvl):
    with open("../data/user/progress.json", "r") as prog:
        prog_json = json.load(prog)

    # the word _will_ be in the front of the queue
    word_test = prog_json[lvl].pop(0)

    # maybe don't even need to pass word parameter - test later
    if lvl == '5':
        prog_json[lvl].append((word_test, int(time.time())))
    else:
        lvl += 1
        prog_json[lvl].append((word_test, int(time.time())))

    with open("../data/user/progress.json", "w") as prog_out:
        json.dump(prog_json, prog_out, ensure_ascii = False)

# move word back to level 1
def incorrect(word, lvl):
    with open("../data/user/progress.json", "r") as prog:
        prog_json = json.load(prog)

    word_test = prog_json[lvl].pop(0)
    prog_json['1'].append((word_test, int(time.time())))

    with open("../data/user/progress.json", "w") as prog_out:
        json.dump(prog_json, prog_out, ensure_ascii = False)
