#!/usr/bin/env python3

import sys, os
import json
import time
import train

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

def save_pests(focus, sound):
    try:
        with open("../data/user/settings.json", "r") as settings:
            settings_dict = json.load(settings)
    except FileNotFoundError:
        return "Settings file missing"

    settings_dict['focus'] = focus
    settings_dict['sound'] = sound

    with open("../data/user/settings.json", "w") as outfile:
        json.dump(settings_dict, outfile, ensure_ascii = False)

    return "Success"

# to set class attribute on every open of Window
def get_pests():
    with open("../data/user/settings.json", "r") as settings:
        settings_dict = json.load(settings)

    return settings_dict['focus'], settings_dict['sound']


def save_settings(lvl2, lvl3, lvl4, lvl5):
    # this function is very bad, but I don't feel like being smart about it yet
    seconds = [86400, 3600, 60]

    try:
        lvl2 = list(map(int, lvl2.strip().split(":")))
        lvl2_sec = 0
        lvl2_sec += seconds[0] * lvl2[0]
        lvl2_sec += seconds[1] * lvl2[1]
        lvl2_sec += seconds[2] * lvl2[2]
        lvl2_sec += lvl2[3]
    except ValueError:
        return "Level 2: Invalid Format"
    except IndexError:
        return "Level 2: Missing unit"

    try:
        lvl3 = list(map(int, lvl3.strip().split(":")))
        lvl3_sec = 0
        lvl3_sec += seconds[0] * lvl3[0]
        lvl3_sec += seconds[1] * lvl3[1]
        lvl3_sec += seconds[2] * lvl3[2]
        lvl3_sec += lvl3[3]
    except ValueError:
        return "Level 3: Invalid Format"
    except IndexError:
        return "Level 3: Missing unit"

    try:
        lvl4 = list(map(int, lvl4.strip().split(":")))
        lvl4_sec = 0
        lvl4_sec += seconds[0] * lvl4[0]
        lvl4_sec += seconds[1] * lvl4[1]
        lvl4_sec += seconds[2] * lvl4[2]
        lvl4_sec += lvl4[3]
    except ValueError:
        return "Level 4: Invalid Format"
    except IndexError:
        return "Level 4: Missing unit"

    try:
        lvl5 = list(map(int, lvl5.strip().split(":")))
        lvl5_sec = 0
        lvl5_sec += seconds[0] * lvl5[0]
        lvl5_sec += seconds[1] * lvl5[1]
        lvl5_sec += seconds[2] * lvl5[2]
        lvl5_sec += lvl5[3]
    except ValueError:
        return "Level 5: Invalid Format"
    except IndexError:
        return "Level 5: Missing unit"

    try:
        with open("../data/user/settings.json", "r") as settings:
            settings_dict = json.load(settings)
    except FileNotFoundError:
        return "Settings file missing"

    settings_dict["2"] = lvl2_sec
    settings_dict["3"] = lvl3_sec
    settings_dict["4"] = lvl4_sec
    settings_dict["5"] = lvl5_sec

    with open("../data/user/settings.json", "w") as outfile:
        json.dump(settings_dict, outfile, ensure_ascii = False)

    train.load_setting()
    return "Success"

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
        prog_decoded['1'].append((word, int(time.time())))

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
                    try:
                        progress_json['1'].append((word[word_key], int(time.time())))
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
