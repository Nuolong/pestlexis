#!/usr/bin/env python3

import sys, os
import json

# debug print
def debug(string):
    str_len = len(string)
    print((str_len//2-3) * "-" + "DEBUG" + (str_len//2-2) * "-")
    print(string)
    print(str_len * "-")
    print()

# restart app
def refresh():
    python = sys.executable
    os.execl(python, python, * sys.argv)

def add_vocab(keys):
    word = keys[0].strip()
    definitions = [x.strip() for x in keys[1].split(",")]
    if len(keys) == 3:
        roman = keys[2].strip()

    # add to dictionary
    if os.path.exists("../data/user/dict.json"):
        with open("../data/user/dict.json", "r") as word_list:
            word_decoded = json.load(word_list)

        try:
            word_decoded[word] = {'definitions': definitions, 'romanization': roman}
        except NameError:
            word_decoded[word] = {'definitions': definitions}

        with open("../data/user/dict.json", "w") as word_list:
            json.dump(word_decoded, word_list, ensure_ascii = False)
    else:
        try:
            new_dict = {word: {'definitions': definitions, 'romanization': roman}}
        except NameError:
            new_dict = {word: {'definitions': definitions}}

        with open("../data/user/dict.json", "w") as word_list:
            json.dump(new_dict, word_list, ensure_ascii = False)


    # add to progress boxes
    with open("../data/user/progress.json", "r") as progress:
        prog_decoded = json.load(progress)
        prog_decoded['1'].append(word)

    with open("../data/user/progress.json", "w") as prog_out:
        json.dump(prog_decoded, prog_out, ensure_ascii = False)

    return "Added " + word + " to deck"



# create progress.json
def create_progress(keys):

    debug("Creating progress.json")
    data_dict = []
    progress = []
    with open("../data/vocab.json", "r") as data:
        data_list = json.load(data)
        for word in data_list:
            word_dict = {}

            try:
                word_dict['vocab'] = word[keys[0]]
            except KeyError:
                debug("Vocab key nonexistent")
                return "Vocabulary key nonexistent"

            try:
                word_dict['meaning'] = word[keys[1]]
            except KeyError:
                debug("Meaning key nonexistent")
                return "Meaning key nonexistent"

            try:
                if len(keys) == 3:
                    word_dict['roman'] = word[keys[2]]
            except KeyError:
                debug("Romanization key nonexistent")
                return "Romanization key nonexistent"

            progress.append(word_dict)

    with open("../data/progress.json", "w") as outfile:
        json.dump(progress, outfile, ensure_ascii = False)

    debug("Created progress.json")
    return "Success"
