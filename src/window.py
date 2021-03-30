#!/usr/bin/env python3

# imports
import tkinter as tk
import train

# constants
background_clr = "#e6e6ff"

# window settings
window = tk.Tk()
window.title('Pestlexis')
window.config(background = background_clr)

def need_data_page():
    print("In need_data_page()")
    # TODO: show welcome, need data.json

def new_user_page():
    print("In new_user_page()")
    # TODO: show welcome page, define json fields from data.json and create progress.json

def default_page():
    print("In default_page()")
    # TODO: do program

# wait for events
window.mainloop()
