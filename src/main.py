#!/usr/bin/env python3

import os, json, window

def main():

    # check if vocabulary exists
    if not os.path.exists("../data/vocab.json"):
        print("Please put vocab.json in data directory")
        exit(1)

    # if new user
    if not os.path.exists("../data/progress.json"):
        window.new_user_page()
        print("Creating new progress json")
        dictt = {}
        with open("../data/vocab.json", "r") as data:
            dictt = json.load(data)
        with open("../data/progress.json", "w") as outfile:
            json.dump(dictt, outfile, ensure_ascii = False)




if __name__ == '__main__':
    main()
