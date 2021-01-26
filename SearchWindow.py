import re
from tkinter import Toplevel, Frame, Label, Entry, Button, LEFT
from SearchResults import SearchResults
from DbHolder import DbHolder


class SearchWindow(Toplevel):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.grab_set()
        self.resizable(False, False)
        self.title("Поиск")

        self.frame_date = Frame(self)
        self.label_date = Label(self.frame_date, text="Дата", width=5)
        self.entry_date = Entry(self.frame_date)
        self.entry_date.insert(0, "XXXX-XX-XX")

        self.frame_time_start = Frame(self)
        self.label_time_start = Label(self.frame_time_start, text="С", width=5)
        self.entry_time_start = Entry(self.frame_time_start)
        self.entry_time_start.insert(0, "XX:XX:XX")

        self.frame_time_end = Frame(self)
        self.label_time_end = Label(self.frame_time_end, text="До", width=5)
        self.entry_time_end = Entry(self.frame_time_end)
        self.entry_time_end.insert(0, "XX:XX:XX")

        self.frame_genre = Frame(self)
        self.label_genre = Label(self.frame_genre, text="Жанр", width=5)
        self.entry_genre = Entry(self.frame_genre)

        self.confirm = Button(self, text="Поиск", command=self.show_result)
        self.pack()

    def pack(self):
        self.frame_date.pack()
        self.label_date.pack(side=LEFT)
        self.entry_date.pack(side=LEFT)
        self.frame_time_start.pack()
        self.label_time_start.pack(side=LEFT)
        self.entry_time_start.pack(side=LEFT)
        self.frame_time_end.pack()
        self.label_time_end.pack(side=LEFT)
        self.entry_time_end.pack(side=LEFT)
        self.label_genre.pack(side=LEFT)
        self.entry_genre.pack(side=LEFT)
        self.frame_genre.pack()
        self.confirm.pack()

    def show_result(self):
        db = DbHolder()
        reg_date = r"2\w\w\w-[01]\w-[0-3]\w"
        reg_time = r"[0-2]\w:[0-6]\w:[0-6]\w"
        if not re.match(reg_date, self.entry_date.get()):
            return
        elif not re.match(reg_time, self.entry_time_start.get()):
            return
        elif not re.match(reg_time, self.entry_time_end.get()):
            return
        else:
            res = db.get_sessions_by_date(self.entry_date.get(), self.entry_time_start.get(), self.entry_time_end.get(), self.entry_genre.get().capitalize())
            SearchResults(res)
            self.destroy()



