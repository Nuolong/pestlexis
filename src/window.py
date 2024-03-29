#!/usr/bin/env python3

# imports
import tkinter as tk
import train
import utils
from utils import debug
from functools import partial
import os
import time
import json
import pygame
import random

# constants
background_clr = "#000000"
entry_width = 14
text_width = 28
subtext_size = 15
subtext_font = "Consolas"
text_box_font = "Consolas"
title_font = "Times New Roman"
title_size = 45
lvl_colors = { '1': "#9bf598",
               '2': "#27c722",
               '3': "#00e0d5",
               '4': "#798CFF",
               '5': "#c73cfa"  }
refresh_rate = 10000
sound_dir = "../data/sounds/"


class Window:
    def __init__(self):
        # window settings
        self.root = tk.Tk()
        self.root.title('Pestlexis')
        self.root.config(background = background_clr)
        self.root.geometry("500x500")
        self.elements = []
        self.focus, self.sound = utils.get_pests()
        self.active_word = False
        self.lb_title = tk.Label(
            text="Pestlexis",
            bg="black", fg="white",
            width=100,
            font=(title_font, title_size),
            anchor="center"
        )
        self.sounds = []

    # wait for events
    def start(self):
        pygame.init()
        for filename in os.listdir(sound_dir):
            self.sounds.append(sound_dir + filename)

        self.root.after(1000, self.play_sound)
        self.root.after(1000, self.grab_focus)
        self.root.mainloop()


    def grab_focus(self):
        try:
            if not self.root.focus_displayof() and self.active_word and self.focus:
                self.root.withdraw()
                self.root.deiconify()
                self.root.focus_force()
                self.root.lift()
                self.root.attributes('-topmost', True)
                self.root.attributes('-topmost', False)
        # for being on the menu
        except KeyError:
            pass
        self.root.after(1000, self.grab_focus)

    def play_sound(self):
        try:
            if not self.root.focus_displayof() and self.active_word and self.sound:
                pygame.mixer.music.load(random.choice(self.sounds))
                pygame.mixer.music.play()
        except KeyError:
            pass
        self.root.after(1000, self.play_sound)

    # TODO: homepage
    # state True: train
    # state False: new user
    def homepage(self):
        debug("In homepage")

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
            command=self.add_word
        )
        filemenu.add_command(
            label="Set Pests",
            activeforeground="white",
            activebackground="black",
            command=self.pest_settings
        )
        filemenu.add_command(
            label="Train Settings",
            activeforeground="white",
            activebackground="black",
            command=self.train_settings
        )

        menubar.add_cascade(label="Menu", menu=filemenu)
        self.root.config(menu=menubar)

        if not os.path.exists("../data/user/dict.json"):
            self.active_word = False
            for element in self.elements:
                element.destroy()
            self.elements = []

            lb_title = tk.Label(
                text="Pestlexis",
                bg="black", fg="white",
                width=100,
                font=(title_font, title_size),
                anchor="center"
            )

            lb_need_data = tk.Label(
                text="Welcome new user! \nImport your dictionary \nor add new words.",
                bg="black", fg="#798CFF",
                width=100, height=1,
                font=(subtext_font, subtext_size),
                anchor="center",
                pady=40
            )

            bt_import = tk.Button(
                text="Import JSON",
                width=10, height=2,
                bg="black", fg="white",
                font=(subtext_font, subtext_size),
                anchor="center",
                highlightthickness=0,
                command=self.import_page
            )

            bt_add_word = tk.Button(
                text="Add Words",
                width=10, height=2,
                bg="black", fg="white",
                font=(subtext_font, subtext_size),
                anchor="center",
                highlightthickness=0,
                command=self.add_word
            )

            # display widgets
            lb_title.pack(pady=(50, subtext_size))
            lb_need_data.pack()
            bt_import.pack(pady=(30, subtext_size))
            bt_add_word.pack(pady=(30, subtext_size))
            self.elements.extend([lb_title, lb_need_data, bt_import, bt_add_word])

        else:
            for element in self.elements:
                element.destroy()
            self.elements = []

            word, meaning, roman, lvl = train.get_word()

            # no words to study right now
            if word is None:
                self.active_word = False
                lb_finished = tk.Label(
                    text="Check back later! \nNo words are ready to be trained.",
                    bg="black", fg="#798CFF",
                    width=100, height=1,
                    font=(subtext_font, subtext_size),
                    anchor="center",
                    pady=40
                )
                lb_finished.pack(pady=(50, subtext_size))
                self.elements.append(lb_finished)
                self.root.after(refresh_rate, self.homepage)

            elif roman is None:
                self.active_word = True
                lb_word = tk.Label(
                    text=word,
                    bg="black", fg=lvl_colors[lvl],
                    width=100, height=1,
                    font=(subtext_font, title_size),
                    anchor="center",
                    pady=40
                )
                lb_def = tk.Label(
                    text="Definition:",
                    bg="black", fg="white",
                    width=100, height=1,
                    font=(subtext_font, subtext_size),
                    anchor="center"
                )
                tx_def = tk.Text(
                    bg="black", fg="white",
                    width=text_width,
                    height=entry_width/4,
                    font=(text_box_font, subtext_size)
                )

                lb_result = tk.Label(
                    bg="black",
                    fg="red",
                    width=100,
                    height=1,
                    font=(subtext_font, subtext_size),
                    anchor="center"
                )

                bt_check = tk.Button(
                    text="Check",
                    width=10,
                    height=2,
                    bg="black",
                    font=(subtext_font, subtext_size),
                    fg="white",
                    anchor="center",
                    highlightthickness=0,
                    command=partial(self.check_ans, word, lvl, lb_result, tx_def)
                )

                lb_word.pack()
                lb_def.pack()
                tx_def.pack()
                bt_check.pack(pady=(subtext_size,0))
                self.elements.extend([lb_word, lb_def, tx_def, bt_check])

            else:
                self.active_word = True
                for element in self.elements:
                    element.destroy()
                self.elements = []

                lb_word = tk.Label(
                    text=word,
                    bg="black", fg=lvl_colors[lvl],
                    width=100, height=1,
                    font=(subtext_font, title_size),
                    anchor="center",
                    pady=40
                )
                lb_def = tk.Label(
                    text="Definition:",
                    bg="black", fg="white",
                    width=100, height=1,
                    font=(subtext_font, subtext_size),
                    anchor="center"
                )
                tx_def = tk.Text(
                    bg="black", fg="white",
                    width=text_width,
                    height=entry_width/4,
                    font=(text_box_font, subtext_size)
                )

                lb_roman = tk.Label(
                    text="Romanization:",
                    bg="black",
                    fg="white",
                    width=100,
                    height=1,
                    font=(subtext_font, subtext_size),
                    anchor="center"
                )

                et_roman = tk.Entry(
                    bg="black", fg="white",
                    width=entry_width,
                    font=(text_box_font, subtext_size),
                    justify='center',
                    disabledbackground="#636363"
                )

                lb_result = tk.Label(
                    bg="black",
                    fg="red",
                    width=100,
                    height=1,
                    font=(subtext_font, subtext_size),
                    anchor="center"
                )

                bt_check = tk.Button(
                    text="Check",
                    width=10,
                    height=2,
                    bg="black",
                    font=(subtext_font, subtext_size),
                    fg="white",
                    anchor="center",
                    highlightthickness=0,
                    command=partial(self.check_ans, word, lvl, lb_result, tx_def, et_roman)
                )

                lb_word.pack()
                lb_def.pack()
                tx_def.pack()
                lb_roman.pack(pady=(subtext_size,0))
                et_roman.pack()
                bt_check.pack(pady=(subtext_size,0))
                self.elements.extend([lb_word, lb_def, tx_def, lb_roman, et_roman, bt_check])

    # TODO: these both
    def add_word(self):
        debug("In add_word")
        add_word_window = tk.Toplevel(self.root)
        add_word_window.title("Append Lexis")
        add_word_window.geometry("400x450")
        add_word_window.config(background = background_clr)

        lb_vocab = tk.Label(
            add_word_window,
            text="Word:",
            bg="black", fg="white",
            width=100, height=1,
            font=(subtext_font, subtext_size),
            anchor="center"
        )

        et_vocab = tk.Entry(
            add_word_window,
            bg="black", fg="white",
            width=entry_width,
            font=(text_box_font, subtext_size),
            justify='center'
        )

        lb_def = tk.Label(
            add_word_window,
            text="Definition:",
            bg="black", fg="white",
            width=100, height=1,
            font=(subtext_font, subtext_size),
            anchor="center"
        )
        tx_def = tk.Text(
            add_word_window,
            bg="black", fg="white",
            width=text_width,
            height=entry_width/4,
            font=(text_box_font, subtext_size)
        )

        lb_roman = tk.Label(
            add_word_window,
            text="Romanization:",
            bg="black",
            fg="white",
            width=100,
            height=1,
            font=(subtext_font, subtext_size),
            anchor="center"
        )

        et_roman = tk.Entry(
            add_word_window,
            bg="black", fg="white",
            width=entry_width,
            font=(text_box_font, subtext_size),
            justify='center',
            disabledbackground="#636363"
        )

        # y/n selection
        rd_roman_no = tk.Radiobutton(
            add_word_window,
            bg="black", fg="white",
            selectcolor="black",
            activebackground="black",
            activeforeground="white",
            font=(subtext_font, subtext_size - 5),
            highlightthickness=0,
            value=0,
            command=partial(self.roman_sel, 0, et_roman),
            text="No",
        )
        rd_roman_yes = tk.Radiobutton(
            add_word_window,
            bg="black", fg="white",
            selectcolor="black",
            activebackground="black",
            activeforeground="white",
            font=(subtext_font, subtext_size - 5),
            highlightthickness=0,
            value=1,
            command=partial(self.roman_sel, 1, et_roman),
            text="Yes",
        )

        # to use in get_vals()
        lb_result = tk.Label(
            add_word_window,
            bg="black",
            fg="red",
            width=100,
            height=1,
            font=(subtext_font, subtext_size),
            anchor="center"
        )

        bt_add = tk.Button(
            add_word_window,
            text="Add",
            width=10,
            height=2,
            bg="black",
            font=(subtext_font, subtext_size),
            fg="white",
            anchor="center",
            highlightthickness=0,
            command=partial(self.get_vals_word, lb_result, et_vocab, tx_def, et_roman)
        )

        # vocab
        lb_vocab.pack(pady=(10,0))
        et_vocab.pack(pady=(5,0))

        # definition
        lb_def.pack(pady=(subtext_size,0))
        tx_def.pack(pady=(5,0))

        # romanization
        lb_roman.pack(pady=(subtext_size,0))
        rd_roman_no.pack()
        rd_roman_yes.pack()
        et_roman.pack()

        # start
        bt_add.pack(pady=(subtext_size,0))

    def pest_settings(self):
        debug("In pest_settings")
        pest_window = tk.Toplevel(self.root)
        pest_window.title("Pest Settings")
        pest_window.geometry("400x260")
        pest_window.config(background = background_clr)

        focus = tk.IntVar()
        sound = tk.IntVar()

        with open("../data/user/settings.json", "r") as settings:
            settings_dict = json.load(settings)

        # set current setting
        focus.set(settings_dict['focus'])
        sound.set(settings_dict['sound'])

        lb_focus = tk.Label(
            pest_window,
            text="Force focus:",
            bg="black",
            fg="white",
            width=100,
            height=1,
            font=(subtext_font, subtext_size),
            anchor="center"
        )

        focus_off = tk.Radiobutton(
            pest_window,
            bg="black", fg="white",
            selectcolor="black",
            activebackground="black",
            activeforeground="white",
            font=(subtext_font, subtext_size - 5),
            highlightthickness=0,
            value=0,
            text="Off",
            variable=focus
        )
        focus_on = tk.Radiobutton(
            pest_window,
            bg="black", fg="white",
            selectcolor="black",
            activebackground="black",
            activeforeground="white",
            font=(subtext_font, subtext_size - 5),
            highlightthickness=0,
            value=1,
            text="On",
            variable=focus
        )

        lb_sound = tk.Label(
            pest_window,
            text="Play sound:",
            bg="black",
            fg="white",
            width=100,
            height=1,
            font=(subtext_font, subtext_size),
            anchor="center"
        )

        sound_off = tk.Radiobutton(
            pest_window,
            bg="black", fg="white",
            selectcolor="black",
            activebackground="black",
            activeforeground="white",
            font=(subtext_font, subtext_size - 5),
            highlightthickness=0,
            value=0,
            text="Off",
            variable=sound
        )
        sound_on = tk.Radiobutton(
            pest_window,
            bg="black", fg="white",
            selectcolor="black",
            activebackground="black",
            activeforeground="white",
            font=(subtext_font, subtext_size - 5),
            highlightthickness=0,
            value=1,
            text="On",
            variable=sound
        )

        lb_result = tk.Label(
            pest_window,
            bg="black",
            fg="red",
            width=100,
            height=1,
            font=(subtext_font, subtext_size),
            anchor="center"
        )

        bt_save = tk.Button(
            pest_window,
            text="Save",
            width=10,
            height=1,
            bg="black",
            font=(subtext_font, subtext_size),
            fg="white",
            anchor="center",
            highlightthickness=0,
            command=partial(self.read_pests, lb_result, focus, sound)
        )

        lb_focus.pack(pady=(10,0))
        focus_off.pack(pady=(5,0))
        focus_on.pack()

        lb_sound.pack(pady=(10,0))
        sound_off.pack(pady=(5,0))
        sound_on.pack()

        bt_save.pack(pady=(20,0))

    def train_settings(self):
        debug("In train_settings")
        train_window = tk.Toplevel(self.root)
        train_window.title("Training Settings")
        train_window.geometry("400x375")
        train_window.config(background = background_clr)
        current = train.load_setting()
        current_conv = []

        # to display what the current settings are in entries
        for time in current:
            day = time // (24 * 3600)
            time = time % (24 * 3600)
            hour = time // 3600
            time %= 3600
            minutes = time // 60
            time %= 60
            seconds = time
            current_conv.append("%d:%d:%d:%d" % (day, hour, minutes, seconds))


        lb_lvl2 = tk.Label(
            train_window,
            text="Level 2:",
            bg="black", fg=lvl_colors['2'],
            width=100, height=1,
            font=(subtext_font, subtext_size),
            anchor="center"
        )

        et_lvl2 = tk.Entry(
            train_window,
            bg="black", fg="white",
            width=entry_width,
            font=(text_box_font, subtext_size),
            justify='center'
        )
        et_lvl2.insert(0, current_conv[0])

        lb_lvl3 = tk.Label(
            train_window,
            text="Level 3:",
            bg="black", fg=lvl_colors['3'],
            width=100, height=1,
            font=(subtext_font, subtext_size),
            anchor="center"
        )

        et_lvl3 = tk.Entry(
            train_window,
            bg="black", fg="white",
            width=entry_width,
            font=(text_box_font, subtext_size),
            justify='center'
        )
        et_lvl3.insert(0, current_conv[1])

        lb_lvl4 = tk.Label(
            train_window,
            text="Level 4:",
            bg="black", fg=lvl_colors['4'],
            width=100, height=1,
            font=(subtext_font, subtext_size),
            anchor="center"
        )

        et_lvl4 = tk.Entry(
            train_window,
            bg="black", fg="white",
            width=entry_width,
            font=(text_box_font, subtext_size),
            justify='center'
        )
        et_lvl4.insert(0, current_conv[2])

        lb_lvl5 = tk.Label(
            train_window,
            text="Level 5:",
            bg="black", fg=lvl_colors['5'],
            width=100, height=1,
            font=(subtext_font, subtext_size),
            anchor="center"
        )

        et_lvl5 = tk.Entry(
            train_window,
            bg="black", fg="white",
            width=entry_width,
            font=(text_box_font, subtext_size),
            justify='center'
        )
        et_lvl5.insert(0, current_conv[3])

        lb_result = tk.Label(
            train_window,
            bg="black",
            fg="red",
            width=100,
            height=1,
            font=(subtext_font, subtext_size),
            anchor="center"
        )

        bt_save = tk.Button(
            train_window,
            text="Save",
            width=10,
            height=1,
            bg="black",
            font=(subtext_font, subtext_size),
            fg="white",
            anchor="center",
            highlightthickness=0,
            command=partial(self.read_settings, lb_result, et_lvl2, et_lvl3, et_lvl4, et_lvl5)
        )

        # vocab
        lb_lvl2.pack(pady=(10,0))
        et_lvl2.pack(pady=(5,0))
        lb_lvl3.pack(pady=(10,0))
        et_lvl3.pack(pady=(5,0))
        lb_lvl4.pack(pady=(10,0))
        et_lvl4.pack(pady=(5,0))
        lb_lvl5.pack(pady=(10,0))
        et_lvl5.pack(pady=(5,0))
        bt_save.pack(pady=(20,0))

    # import json page
    def import_page(self):
        debug("In import_page")
        import_window = tk.Toplevel(self.root)
        import_window.title("Import Lexis")
        import_window.geometry("400x375")
        import_window.config(background = background_clr)

        lb_vocab = tk.Label(
            import_window,
            text="Vocabulary key:",
            bg="black", fg="white",
            width=100, height=1,
            font=(subtext_font, subtext_size),
            anchor="center"
        )

        et_vocab = tk.Entry(
            import_window,
            bg="black", fg="white",
            width=entry_width,
            font=(text_box_font, subtext_size),
            justify='center'
        )
        et_vocab.insert(0, "vocab")

        lb_def = tk.Label(
            import_window,
            text="Definition key:",
            bg="black", fg="white",
            width=100, height=1,
            font=(subtext_font, subtext_size),
            anchor="center"
        )
        et_def = tk.Entry(
            import_window,
            bg="black", fg="white",
            width=entry_width,
            font=(text_box_font, subtext_size),
            justify='center'
        )
        et_def.insert(0, "meaning")


        lb_roman = tk.Label(
            import_window,
            text="Romanization key:",
            bg="black",
            fg="white",
            width=100,
            height=1,
            font=(subtext_font, subtext_size),
            anchor="center"
        )

        et_roman = tk.Entry(
            import_window,
            bg="black", fg="white",
            width=entry_width,
            font=(text_box_font, subtext_size),
            justify='center',
            disabledbackground="#636363"
        )

        # y/n selection
        rd_roman_no = tk.Radiobutton(
            import_window,
            bg="black", fg="white",
            selectcolor="black",
            activebackground="black",
            activeforeground="white",
            font=(subtext_font, subtext_size - 5),
            highlightthickness=0,
            value=0,
            command=partial(self.roman_sel, 0, et_roman),
            text="No",
        )
        rd_roman_yes = tk.Radiobutton(
            import_window,
            bg="black", fg="white",
            selectcolor="black",
            activebackground="black",
            activeforeground="white",
            font=(subtext_font, subtext_size - 5),
            highlightthickness=0,
            value=1,
            command=partial(self.roman_sel, 1, et_roman),
            text="Yes",
        )
        et_roman.insert(0, "roman")

        lb_result = tk.Label(
            import_window,
            bg="black",
            fg="red",
            width=100,
            height=1,
            font=(subtext_font, subtext_size),
            anchor="center"
        )

        bt_start = tk.Button(
            import_window,
            text="Import",
            width=10,
            height=2,
            bg="black",
            font=(subtext_font, subtext_size),
            fg="white",
            anchor="center",
            highlightthickness=0,
            command=partial(self.get_vals_import, lb_result, et_vocab, et_def, et_roman)
        )

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
        et_roman.pack()

        # start
        bt_start.pack(pady=(subtext_size,0))

    # get all active entry values
    def get_vals_import(self, label, *args):
        keys = []
        result = tk.StringVar()

        for entry in args:
            if entry['state'] != 'disabled':
                keys.append(entry.get())

        status, strg = utils.import_dict(keys)
        result.set(strg)

        label.config(textvariable=result)
        label.pack()
        self.root.update_idletasks()

        # restart app 1 second after success
        if status:
            time.sleep(1)
            debug("Import success")
            utils.refresh()


    # gets fields for adding a new word and adds word
    def get_vals_word(self, label, *args):
        keys = []
        result = tk.StringVar()

        for entry in args:
            if entry.winfo_class() == 'Text':
                keys.append(entry.get("1.0", "end"))
            elif entry['state'] != 'disabled':
                keys.append(entry.get())

        status, strg = utils.add_vocab(keys)
        result.set(strg)

        label.config(textvariable=result)
        label.pack()

        # clear the boxes after adding successfully.
        if status:
            for entry in args:
                if entry.winfo_class() == 'Text':
                    entry.delete("1.0", "end")
                else:
                    entry.delete(0, "end")

        self.homepage()

    # No: 0; Yes: 1
    def roman_sel(self, selection, et):
        if not selection:
            et.config(state='disabled')
        else:
            et.config(state='normal')

    def read_pests(self, label, focus, train):
        result = tk.StringVar()

        strg = utils.save_pests(focus.get(), train.get())
        self.focus, self.sound = utils.get_pests()
        result.set(strg)

        label.config(textvariable=result)
        label.pack()


    def read_settings(self, label, lvl2, lvl3, lvl4, lvl5):
        result = tk.StringVar()

        strg = utils.save_settings(lvl2.get(), lvl3.get(), lvl4.get(), lvl5.get())
        result.set(strg)

        label.config(textvariable=result)
        label.pack()

    def check_ans(self, word, lvl, label, *args):
        correct = False
        result = tk.StringVar()

        if train.validate(word, *args):
            correct = True
            result.set(train.correct(word, lvl))
            label.config(fg='green')
        else:
            result.set(train.incorrect(word, lvl))
            label.config(fg='red')


        label.config(textvariable=result)
        self.elements.append(label)

        if not correct:
            for el in self.elements:
                if el.winfo_class() == 'Button':
                    el.destroy()
                    self.elements.remove(el)


            bt_review = tk.Button(
                text="Done",
                width=10,
                height=2,
                bg="black",
                font=(subtext_font, subtext_size),
                fg="white",
                anchor="center",
                highlightthickness=0,
                command=partial(self.homepage)
            )
            self.elements.append(bt_review)
            bt_review.pack(pady=(subtext_size,0))
            label.pack()
            return

        label.pack()
        self.root.update_idletasks()
        time.sleep(2)
        self.homepage()
