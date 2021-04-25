#!/usr/bin/env python3

# imports
import tkinter as tk
import train
import utils
from utils import debug
from functools import partial

# constants
background_clr = "#000000"
entry_width = 14
subtext_size = 15
subtext_font = "Consolas"
text_box_font = "Consolas"
title_font = "Times New Roman"
title_size = 45

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
            font=(title_font, title_size),
            anchor="center"
        )

        # to use in roman_sel()
        self.et_roman = tk.Entry(
            bg="black", fg="white",
            width=entry_width,
            font=(text_box_font, subtext_size),
            justify='center',
            disabledbackground="#636363"
        )

        # to use in get_vals()
        self.lb_result = tk.Label(
            bg="black",
            fg="red",
            width=100,
            height=1,
            font=(subtext_font, subtext_size),
            anchor="center"
        )

    # wait for events
    def start(self):
        self.root.mainloop()


    # TODO: homepage
    # state True: train
    # state False: new user
    def homepage(self, state):
        debug("In need_data_page()")

        # menu at top
        menubar = tk.Menu(
            self.root,
            bg="black",
            fg="white",
            activeforeground="white",
            activebackground="black"
        )
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(
            label="Append Lexis",
            activeforeground="white",
            activebackground="black",
            command=add_word
        )
        filemenu.add_command(
            label="Set Pests",
            activeforeground="white",
            activebackground="black",
            command=pest_settings
        )

        menubar.add_cascade(label="Menu", menu=filemenu)
        self.root.config(menu=menubar)

        lb_need_data = tk.Label(
            text="Please add a vocab.json\n to the data directory. ",
            bg="black", fg="#ffcccc",
            width=100, height=1,
            font=(subtext_font, subtext_size),
            anchor="center",
            pady=40
        )

        bt_refresh = tk.Button(
            text="Refresh",
            width=10, height=2,
            bg="black", fg="white",
            font=(subtext_font, subtext_size),
            anchor="center",
            highlightthickness=0,
            command=utils.refresh
        )

        # display widgets
        self.lb_title.pack(pady=(50, subtext_size))
        lb_need_data.pack()
        bt_refresh.pack()

    # TODO: these both
    def add_word():
        pass

    def pest_settings():
        pass

    # sets up progress
    def new_user_page(self):
        debug("In new_user_page()")

        lb_vocab = tk.Label(
            text="Vocabulary key:",
            bg="black", fg="white",
            width=100, height=1,
            font=(subtext_font, subtext_size),
            anchor="center"
        )

        et_vocab = tk.Entry(
            bg="black", fg="white",
            width=entry_width,
            font=(text_box_font, subtext_size),
            justify='center'
        )
        et_vocab.insert(0, "vocab")

        lb_def = tk.Label(
            text="Definition key:",
            bg="black", fg="white",
            width=100, height=1,
            font=(subtext_font, subtext_size),
            anchor="center"
        )
        et_def = tk.Entry(
            bg="black", fg="white",
            width=entry_width,
            font=(text_box_font, subtext_size),
            justify='center'
        )
        et_def.insert(0, "meaning")


        lb_roman = tk.Label(
            text="Romanization key:",
            bg="black",
            fg="white",
            width=100,
            height=1,
            font=(subtext_font, subtext_size),
            anchor="center"
        )
        # y/n selection
        rd_roman_no = tk.Radiobutton(
            bg="black", fg="white",
            selectcolor="black",
            activebackground="black",
            activeforeground="white",
            font=(subtext_font, subtext_size - 5),
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
            font=(subtext_font, subtext_size - 5),
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
            font=(subtext_font, subtext_size),
            fg="white",
            anchor="center",
            highlightthickness=0,
            command=partial(self.get_vals, et_vocab, et_def, self.et_roman)
        )

        # title
        self.lb_title.pack(pady=(50,5))

        # vocab
        lb_vocab.pack(pady=(10,0))
        et_vocab.pack(pady=(5,0))

        # definition
        lb_def.pack(pady=(subtext_size,0))
        et_def.pack(pady=(5,0))

        # romanization
        lb_roman.pack(pady=(subtext_size,0))
        rd_roman_no.pack()
        rd_roman_yes.pack()
        self.et_roman.pack()

        # start
        bt_start.pack(pady=(subtext_size,0))

    # get all active entry values
    def get_vals(self, *args):
        keys = []
        result = tk.StringVar()

        for entry in args:
            if entry['state'] != 'disabled':
                keys.append(entry.get())
        result.set(utils.create_progress(keys))

        self.lb_result.config(textvariable=result)
        self.lb_result.pack()


    # No: 0; Yes: 1
    def roman_sel(self, selection):
        if not selection:
            self.et_roman.config(state='disabled')
        else:
            self.et_roman.config(state='normal')

    def default_page(self):
        debug("In default_page()")
        # TODO: do program
