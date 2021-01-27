from tkinter import Label, Entry, Button

from DbHolder import DbHolder
from CinemaSessions import CinemaSessions


class CinemaItemBlock:
    db = DbHolder()

    def __init__(self, master, idc):
        self.cinema_id = idc
        self.label_name = Label(master, text="Название")
        self.label_address = Label(master, text="Адрес")
        self.label_district = Label(master, text="Район")
        self.label_is_open = Label(master, text="Открыт?")
        self.entry_name = Entry(master, width=30)
        self.entry_address = Entry(master, width=30)
        self.entry_district = Entry(master, width=30)
        self.entry_is_open = Entry(master, width=30)
        self.button_sessions = Button(master, width=30, text="Сеансы", command=self.show_sessions)
        self.pack()
        self.index = 0
        self.update(self.index)

    def show_sessions(self):
        CinemaSessions(self.cinema_id)

    def pack(self):
        self.label_name.pack()
        self.entry_name.pack()
        self.label_address.pack()
        self.entry_address.pack()
        self.label_district.pack()
        self.entry_district.pack()
        self.label_is_open.pack()
        self.entry_is_open.pack()
        self.button_sessions.pack(pady=5)

    def update(self, index, cinema_id=None):
        self.index = index
        if cinema_id:
            self.cinema_id = cinema_id
        list_cinemas = self.db.get("cinemas")
        if index < 0 or index > len(list_cinemas):
            return
        self.erase_fields()
        if index != len(list_cinemas):
            self.entry_name.insert(0, list_cinemas[index][1].capitalize())
            self.entry_address.insert(0, list_cinemas[index][2].capitalize())
            self.entry_district.insert(0, list_cinemas[index][3].capitalize())
            self.entry_is_open.insert(0, list_cinemas[index][4])

    def erase_fields(self):
        self.entry_name.delete(0, 100)
        self.entry_address.delete(0, 100)
        self.entry_district.delete(0, 100)
        self.entry_is_open.delete(0, 100)
