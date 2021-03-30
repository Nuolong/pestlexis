#!/usr/bin/env python3

# imports
import tkinter as tk
import train
import utils

# constants
background_clr = "#000000"

class Window:
    def __init__(self):
        # window settings
        self.root = tk.Tk()
        self.root.title('Pestlexis')
        self.root.config(background = background_clr)
        self.root.geometry("500x500")

    # wait for events
    def start(self):
        self.root.mainloop()

    def need_data_page(self):
        print("In need_data_page()")
        # TODO: show welcome, need data.json
        lb_title = tk.Label(
            text="Pestlexis",
            bg="black",
            fg="white",
            width=100,
            height=1,
            font=("Times New Roman", 45),
            anchor="center",
            pady=100
        )
        lb_need_data = tk.Label(
            text="Please add a data.json\n to the data directory. ",
            bg="black",
            fg="#ffcccc",
            width=100,
            height=1,
            font=("Consolas", 15),
            anchor="center",
            pady=40
        )

        bt_refresh = tk.Button(
            text="Refresh",
            width=10,
            height=2,
            bg="black",
            font=("Consolas", 15),
            fg="white",
            anchor="center",
            highlightthickness=0,
            command=utils.refresh
        )

        lb_title.pack()
        lb_need_data.pack()
        bt_refresh.pack()

    def new_user_page(self):
        print("In new_user_page()")
        # TODO: show welcome page, define json fields from data.json and create progress.json

    def default_page(self):
        print("In default_page()")
        # TODO: do program
