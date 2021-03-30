#!/usr/bin/env python3

import sys, os

def refresh():
    python = sys.executable
    os.execl(python, python, * sys.argv)

def placeholder(test):
    print(test)
