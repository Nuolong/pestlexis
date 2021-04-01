#!/usr/bin/env python3

# imports
import tkinter as tk
import train
import utils
from utils import debug
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
        self.lb_title = tk.Label(
            text="Pestlexis",
            bg="black", fg="white",
            width=100,
            font=("Times New Roman", 45),
            anchor="center"
        )

        # to use in roman_sel()
        self.et_roman = tk.Entry(
            bg="black", fg="white",
            width=12,
            font=("Consolas", 15),
            justify='center',
            disabledbackground="#636363"
        )


    # wait for events
    def start(self):
        self.root.mainloop()

    # show welcome, need data.json
    def need_data_page(self):
        debug("In need_data_page()")

        lb_need_data = tk.Label(
            text="Please add a vocab.json\n to the data directory. ",
            bg="black", fg="#ffcccc",
            width=100, height=1,
            font=("Consolas", 15),
            anchor="center",
            pady=40
        )

        bt_refresh = tk.Button(
            text="Refresh",
            width=10, height=2,
            bg="black", fg="white",
            font=("Consolas", 15),
            anchor="center",
            highlightthickness=0,
            command=utils.refresh
        )

        # display widgets
        lb_title.pack(pady=(50,150))
        lb_need_data.pack()
        bt_refresh.pack()

    def new_user_page(self):
        debug("In new_user_page()")

        lb_vocab = tk.Label(
            text="Vocabulary key:",
            bg="black", fg="white",
            width=100, height=1,
            font=("Consolas", 15),
            anchor="center"
        )

        et_vocab = tk.Entry(
            bg="black", fg="white",
            width=12,
            font=("Consolas", 15),
            justify='center'
        )
        et_vocab.insert(0, "vocab")

        lb_def = tk.Label(
            text="Definition key:",
            bg="black", fg="white",
            width=100, height=1,
            font=("Consolas", 15),
            anchor="center"
        )
        et_def = tk.Entry(
            bg="black", fg="white",
            width=12,
            font=("Consolas", 15),
            justify='center'
        )
        et_def.insert(0, "meaning")


        lb_roman = tk.Label(
            text="Romanization key:",
            bg="black",
            fg="white",
            width=100,
            height=1,
            font=("Consolas", 15),
            anchor="center"
        )
        # y/n selection
        rd_roman_no = tk.Radiobutton(
            bg="black", fg="white",
            selectcolor="black",
            activebackground="black",
            activeforeground="white",
            font=("Consolas", 10),
            highlightthickness=0,
            value=0,
            command=partial(self.roman_sel, 0),
            text="No",
        )
        rd_roman_yes = tk.Radiobutton(
            bg="black", fg="white",
            selectcolor="black",
            activebackground="black",
            activeforeground="white",
            font=("Consolas", 10),
            highlightthickness=0,
            value=1,
            command=partial(self.roman_sel, 1),
            text="Yes",
        )
        self.et_roman.insert(0, "roman")

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

        # title
        self.lb_title.pack(pady=(50,5))

        # vocab
        lb_vocab.pack(pady=(10,0))
        et_vocab.pack(pady=(5,0))

        # definition
        lb_def.pack(pady=(15,0))
        et_def.pack(pady=(5,0))

        # romanization
        lb_roman.pack(pady=(15,0))
        rd_roman_no.pack(side="left")
        rd_roman_yes.pack(side="left")
        self.et_roman.pack()

        # start
        bt_start.pack(pady=(15,0))


    # TODO - now handle all entry values
    def get_vals(self, ent):
        utils.placeholder(ent.get())

    # No: 0; Yes: 1
    def roman_sel(self, selection):
        if not selection:
            self.et_roman.config(state='disabled', anchor="center")
        else:
            self.et_roman.config(state='normal')

    def default_page(self):
        debug("In default_page()")
        # TODO: do program
