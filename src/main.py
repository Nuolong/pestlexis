#!/usr/bin/env python3

import os, json
from window import Window

def main():

    wd = Window()

    # check if there is a progress.json
    #data = [x for x in os.listdir("../data/user/") if len(x) >= 5 and  x[-5:] == ".json"]
    #if not data:

    if not os.path.exists("../data/user/progress.json"):
        wd.homepage(False)
        wd.start()
        exit(1)

    wd.homepage(True)
    wd.start()


if __name__ == '__main__':
    main()
