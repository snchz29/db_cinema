from tkinter import Label, Entry, Button

from DbHolder import DbHolder
from ActorSessions import ActorSessions


class ActorItemBlock:
    db = DbHolder()

    def __init__(self, master, actor):
        self.actor = actor
        self.label_name = Label(master, text="Имя")
        self.label_surname = Label(master, text="Фамилия")
        self.label_birth = Label(master, text="Дата рождения")
        self.entry_name = Entry(master, width=30)
        self.entry_surname = Entry(master, width=30)
        self.entry_birth = Entry(master, width=30)
        self.button_films = Button(master, width=30, text="Сеансы", command=self.show_films)
        self.pack()
        self.update(actor)

    def show_films(self):
        ActorSessions(self.actor)

    def pack(self):
        self.label_name.pack()
        self.entry_name.pack()
        self.label_surname.pack()
        self.entry_surname.pack()
        self.label_birth.pack()
        self.entry_birth.pack()
        self.button_films.pack(pady=5)

    def update(self, actor=None):
        self.erase_fields()
        if actor:
            self.entry_name.insert(0, actor[0])
            self.entry_surname.insert(0, actor[1])
            self.entry_birth.insert(0, actor[2])

    def erase_fields(self):
        self.entry_name.delete(0, 100)
        self.entry_surname.delete(0, 100)
        self.entry_birth.delete(0, 100)
