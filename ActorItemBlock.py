from tkinter import Label, Entry, Button

from DbHolder import DbHolder
from ActorSessions import ActorSessions


class ActorItemBlock:
    db = DbHolder()

    def __init__(self, master, aid):
        self.actor_id = aid
        self.label_name = Label(master, text="Имя")
        self.label_surname = Label(master, text="Фамилия")
        self.label_birth = Label(master, text="Дата рождения")
        self.entry_name = Entry(master, width=30)
        self.entry_surname = Entry(master, width=30)
        self.entry_birth = Entry(master, width=30)
        self.button_films = Button(master, width=30, text="Сеансы", command=self.show_films)
        self.index = 0
        self.pack()
        self.update(self.index)

    def show_films(self):
        ActorSessions(self.actor_id)

    def pack(self):
        self.label_name.pack()
        self.entry_name.pack()
        self.label_surname.pack()
        self.entry_surname.pack()
        self.label_birth.pack()
        self.entry_birth.pack()
        self.button_films.pack(pady=5)

    def update(self, index, actor_id=None):
        self.index = index
        if actor_id:
            self.actor_id = actor_id
        list_actors = self.db.get("actors")
        print("Actor:", *list_actors, sep="\n")
        if index < 0 or index > len(list_actors):
            return
        self.erase_fields()
        if index != len(list_actors):
            self.entry_name.insert(0, list_actors[index][1])
            self.entry_surname.insert(0, list_actors[index][2])
            self.entry_birth.insert(0, list_actors[index][3])

    def erase_fields(self):
        self.entry_name.delete(0, 100)
        self.entry_surname.delete(0, 100)
        self.entry_birth.delete(0, 100)
