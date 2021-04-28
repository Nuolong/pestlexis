#!/usr/bin/env python3

import sys, os
import json
import time

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


# add to dictionary
# returns tuple:
# (0 on failure, string message)
# (1 on success, string message)
def add_vocab(keys):
    # get values from keys
    word = keys[0].strip()
    if word == "":
        return 0, "Missing word"
    definitions = [x.strip() for x in keys[1].split(",")]
    if definitions[0] == "":
        return 0, "Missing definition"
    if len(keys) == 3:
        roman = keys[2].strip()
        if roman == "":
            return 0, "Missing romanization"

    # add to dictionary (dict.json)
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
        print(prog_decoded['1'])
        prog_decoded['1'].append((word, int(time.time())))
        print(prog_decoded['1'])

    with open("../data/user/progress.json", "w") as prog_out:
        json.dump(prog_decoded, prog_out, ensure_ascii = False)

    return 1, "Added " + word + " to deck"


# create progress.json
def import_dict(keys):
    word_key = keys[0].strip()
    if word_key == "":
        return 0, "Missing word key"
    meaning_key = keys[1].strip()
    if meaning_key == "":
        return 0, "Missing meaning key"
    if len(keys) == 3:
        roman_key = keys[2].strip()
        if roman_key == "":
            return 0, "Missing romanization key"

    debug("Creating dict.json")
    word_dict = {}

    try:
        with open("../data/input/vocab.json", "r") as data:
            data_list = json.load(data)

            with open("../data/user/progress.json", "r") as progress:
                progress_json = json.load(progress)

                for word in data_list:
                    progress_json['1'].append(word[word_key])

                    try:
                        word_dict[word[word_key]] = {}
                    except KeyError:
                        debug("Vocab key nonexistent")
                        return 0, "Vocabulary key nonexistent"

                    try:
                        word_dict[word[word_key]]['definitions'] = word[meaning_key]
                    except KeyError:
                        debug("Meaning key nonexistent")
                        return 0, "Meaning key nonexistent"

                    try:
                        if len(keys) == 3:
                            word_dict[word[word_key]]['romanization'] = word[roman_key]
                    except KeyError:
                        debug("Romanization key nonexistent")
                        return 0, "Romanization key nonexistent"

    except FileNotFoundError:
        return 0, "Put vocab.json in data/input/"

    with open("../data/user/dict.json", "w") as outfile:
        json.dump(word_dict, outfile, ensure_ascii = False)
    debug("Created dict.json")

    with open("../data/user/progress.json", "w") as outfile:
        json.dump(progress_json, outfile, ensure_ascii = False)
    debug("Created progress.json")

    return 1, "Success"
