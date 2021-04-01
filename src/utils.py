#!/usr/bin/env python3

import sys, os

def refresh():
    python = sys.executable
    os.execl(python, python, * sys.argv)

def debug(string):
    print("-------DEBUG-------")
    print(string)
    print("-------------------\n\n")

def placeholder(test):
    print(test)
