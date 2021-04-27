#!/usr/bin/env python3

import os, json
from window import Window

def main():

    wd = Window()

    # check if there is a progress.json
    #data = [x for x in os.listdir("../data/user/") if len(x) >= 5 and  x[-5:] == ".json"]
    #if not data:

    wd.homepage()
    wd.start()


if __name__ == '__main__':
    main()
