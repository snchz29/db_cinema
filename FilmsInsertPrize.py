import re
from tkinter import Toplevel, Button, LEFT, Entry, BOTTOM

from DbHolder import DbHolder


class FilmsInsertPrize(Toplevel):
    db = DbHolder()

    def __init__(self, fid, **kw):
        super().__init__(**kw)
        self.grab_set()
        self.geometry("450x100")
        self.resizable(False, False)
        self.title("Вставить приз")
        self.film_id = fid
        self.entry_name = Entry(self, width=10)
        self.entry_name.insert(0, "Название")
        self.entry_nomination = Entry(self, width=10)
        self.entry_nomination.insert(0, "Номинация")
        self.entry_year = Entry(self, width=10)
        self.entry_year.insert(0, "Год")
        self.button_accept = Button(self, text="Добавить", command=self.click_button)
        self.entry_name.pack(side=LEFT)
        self.entry_nomination.pack(side=LEFT)
        self.entry_year.pack(side=LEFT)
        self.button_accept.pack(side=BOTTOM)

    def click_button(self):
        reg = r'[12]\w\w\w'
        if len(self.entry_year.get()) != 4 or not re.match(reg, self.entry_year.get()):
            print("Bad Year")
            return

        self.db.insert_prize(self.film_id, self.entry_name.get(), self.entry_year.get(), self.entry_nomination.get())
