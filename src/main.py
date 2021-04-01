#!/usr/bin/env python3

import os, json
from window import Window

def main():

    wd = Window()

    # check if vocabulary exists
    if not os.path.exists("../data/vocab.json"):
        wd.need_data_page()
        print("Please put vocab.json in data directory")
        wd.start()
        exit(1)

    # if new user
    if not os.path.exists("../data/progress.json"):
        wd.new_user_page()
        wd.start()



if __name__ == '__main__':
    main()
