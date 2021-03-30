#!/usr/bin/env python3

# imports
import tkinter as tk
import train
import utils
from functools import partial

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

    # show welcome, need data.json
    def need_data_page(self):
        print("In need_data_page()")

        lb_title = tk.Label(
            text="Pestlexis",
            bg="black",
            fg="white",
            width=100,
            height=1,
            font=("Times New Roman", 45),
            anchor="center",
            pady=(100,100)
        )
        lb_need_data = tk.Label(
            text="Please add a vocab.json\n to the data directory. ",
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

        # display widgets
        lb_title.pack()
        lb_need_data.pack()
        bt_refresh.pack()

    def new_user_page(self):
        print("In new_user_page()")
        # TODO: show welcome page, define json fields from data.json and create progress.json
        lb_title = tk.Label(
            text="Pestlexis",
            bg="black",
            fg="white",
            width=100,
            font=("Times New Roman", 45),
            anchor="center"
        )

        lb_vocab = tk.Label(
            text="Vocabulary key: ",
            bg="black",
            fg="white",
            width=100,
            height=1,
            font=("Consolas", 15),
            anchor="center"
        )

        et_vocab = tk.Entry(
            textvariable="test",
            bg="black",
            fg="white",
            width=100,
            font=("Consolas", 15),
        )

        lb_def = tk.Label(
            text="Definition key: ",
            bg="black",
            fg="white",
            width=100,
            height=1,
            font=("Consolas", 15),
            anchor="center"
        )

        lb_roman = tk.Label(
            text="Romanization key: ",
            bg="black",
            fg="white",
            width=100,
            height=1,
            font=("Consolas", 15),
            anchor="center"
        )

        bt_start = tk.Button(
            text="Start",
            width=10,
            height=2,
            bg="black",
            font=("Consolas", 15),
            fg="white",
            anchor="center",
            highlightthickness=0,
            command=partial(self.get_vals, et_vocab)
        )

        lb_title.pack(pady=(100,30))
        lb_vocab.pack(pady=(15,0))
        et_vocab.pack(pady=(15,0))
        lb_def.pack(pady=(15,0))
        lb_roman.pack(pady=(15,0))
        bt_start.pack(pady=(15,0))

    # TODO - now handle all entry values
    def get_vals(self, ent):
        utils.placeholder(ent.get())

    def default_page(self):
        print("In default_page()")
        # TODO: do program
