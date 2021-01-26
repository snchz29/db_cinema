from tkinter import Toplevel, Frame, Label, LEFT, Entry, Button
from abc import ABCMeta

from DbHolder import DbHolder


class Sessions(Toplevel, metaclass=ABCMeta):
    db = DbHolder()

    def __init__(self, **kw):
        super().__init__(**kw)
        self.resizable(False, False)
        self.grab_set()
        self.lines = []

    def make_table_header(self, th: dict):
        header = Frame(self)
        for verbose, width in th.items():
            Label(header, width=width, text=verbose).pack(side=LEFT)
        header.pack()

    def make_table(self, n_rows: int, entries: dict, buttons=None):
        if buttons is None:
            buttons = dict()
        for i in range(n_rows):
            self.lines.append({})
            self.lines[i]["frame"] = Frame(self)
            self.lines[i]["frame"].pack()
            for verbose, width in entries.items():
                self.lines[i][verbose] = Entry(self.lines[i]["frame"], width=width)
                self.lines[i][verbose].pack(side=LEFT)
            for verbose, text in buttons.items():
                self.lines[i][verbose] = Button(self.lines[i]["frame"], text=text)
                self.lines[i][verbose].pack(side=LEFT)

    def push_data(self, data: list):
        for i in range(len(self.lines)):
            for verbose, value in data[i].items():
                self.lines[i][verbose].insert(0, value)
