from tkinter import Toplevel, Button, Label, Frame, LEFT, Entry

from FilmsInsertRole import FilmsInsertRole
from DbHolder import DbHolder


class FilmsActors(Toplevel):
    db = DbHolder()

    def __init__(self, fid, **kw):
        super().__init__(**kw)
        self.grab_set()
        self.film_id = fid
        self.roles = self.db.get_roles_by_film_id(self.film_id)
        self.roles.sort(key=lambda item: item[1])
        self.actors = self.db.get_actors_by_id([i[1] for i in self.roles])
        self.actors.sort(key=lambda item: item[0])
        self.geometry("440x200")
        self.resizable(False, False)
        film_name = self.db.get_films_by_id(self.film_id)[0][1]
        self.title(film_name)
        self.frame_header = Frame(self)
        self.label_name = Label(self.frame_header, text="Имя", width=11)
        self.label_surname = Label(self.frame_header, text="Фамилия", width=11)
        self.label_role = Label(self.frame_header, text="Роль", width=11)
        self.label_buttons_role = Label(self.frame_header, width=10)
        self.label_buttons_actor = Label(self.frame_header, width=10)
        self.label_name.pack(side=LEFT)
        self.label_surname.pack(side=LEFT)
        self.label_role.pack(side=LEFT)
        self.label_buttons_role.pack(side=LEFT)
        self.label_buttons_actor.pack(side=LEFT)
        self.frame_header.pack()

        self.lines = []
        for i in range(len(self.roles)):
            self.lines.append({})
            self.lines[i]['frame'] = Frame(self)
            self.lines[i]['role_id'] = self.roles[i][0]
            self.lines[i]['actor_id'] = self.actors[i][0]
            self.lines[i]['entry_name'] = Entry(self.lines[i]['frame'], width=10)
            self.lines[i]['entry_surname'] = Entry(self.lines[i]['frame'], width=10)
            self.lines[i]['entry_role'] = Entry(self.lines[i]['frame'], width=10)
            self.lines[i]['button_role'] = Button(self.lines[i]['frame'], width=5, text="Роль")
            self.lines[i]['button_actor'] = Button(self.lines[i]['frame'], width=5, text="Актер")

            self.lines[i]['frame'].pack()
            self.lines[i]['entry_name'].pack(side=LEFT)
            self.lines[i]['entry_surname'].pack(side=LEFT)
            self.lines[i]['entry_role'].pack(side=LEFT)
            self.lines[i]['button_role'].pack(side=LEFT)
            self.lines[i]['button_actor'].pack(side=LEFT)

        self.push_data()
        self.button_insert_role = Button(self, width=20, text="Добавить Роль", command=self.show_insert_role)
        self.button_insert_role.pack()

    def push_data(self):
        for i in range(len(self.roles)):
            self.lines[i]["entry_name"].insert(0, self.actors[i][1])
            self.lines[i]["entry_surname"].insert(0, self.actors[i][2])
            self.lines[i]["entry_role"].insert(0, self.roles[i][3])
            self.lines[i]["button_role"].bind('<Button-1>',
                                              lambda e, ind=self.lines[i]["role_id"]: self.db.delete_role(ind))
            self.lines[i]["button_actor"].bind('<Button-1>',
                                               lambda e, ind=self.lines[i]["actor_id"]: self.db.delete_actor(ind))

    def show_insert_role(self):
        FilmsInsertRole(self.film_id)
