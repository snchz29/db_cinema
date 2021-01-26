import re
from tkinter import Toplevel, Button, LEFT, Entry, BOTTOM

from DbHolder import DbHolder


class FilmsInsertRole(Toplevel):
    db = DbHolder()

    def __init__(self, fid, **kw):
        super().__init__(**kw)
        self.grab_set()
        self.geometry("450x100")
        self.resizable(False, False)
        self.title("Вставить роль")
        self.film_id = fid
        self.entry_name = Entry(self, width=10)
        self.entry_name.insert(0, "Имя")
        self.entry_surname = Entry(self, width=10)
        self.entry_surname.insert(0, "Фамилия")
        self.entry_birth = Entry(self, width=10)
        self.entry_birth.insert(0, "XXXX-XX-XX")
        self.entry_role = Entry(self, width=10)
        self.entry_role.insert(0, "Роль")
        self.button_accept = Button(self, text="Добавить", command=self.click_button)
        self.entry_name.pack(side=LEFT)
        self.entry_surname.pack(side=LEFT)
        self.entry_birth.pack(side=LEFT)
        self.entry_role.pack(side=LEFT)
        self.button_accept.pack(side=BOTTOM)

    def click_button(self):
        reg = r'[12]\w\w\w-[01]\w-[0123]\w'
        if len(self.entry_birth.get()) != 10 or not re.match(reg, self.entry_birth.get()):
            print("Bad Date&time")
            return

        self.db.insert_role(self.film_id, self.entry_name.get(), self.entry_surname.get(), self.entry_birth.get(),
                            self.entry_role.get())
        self.destroy()
