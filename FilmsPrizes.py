from tkinter import Toplevel, Button, Label, Frame, LEFT, Entry

from DbHolder import DbHolder
from FilmsInsertPrize import FilmsInsertPrize


class FilmsPrizes(Toplevel):
    db = DbHolder()

    def __init__(self, fid, **kw):
        super().__init__(**kw)
        self.grab_set()
        self.film_id = fid
        self.prizes = self.db.get_prizes_by_film_id(self.film_id)
        print(self.prizes)

        self.geometry("400x200")
        self.resizable(False, False)
        film_name = self.db.get_films_by_id(self.film_id)[0][1]
        self.title(film_name)
        self.frame_header = Frame(self)
        self.label_name = Label(self.frame_header, text="Название", width=11)
        self.label_nomination = Label(self.frame_header, text="Номинация", width=11)
        self.label_year = Label(self.frame_header, text="Год", width=11)
        self.label_buttons = Label(self.frame_header, width=10)
        self.label_name.pack(side=LEFT)
        self.label_nomination.pack(side=LEFT)
        self.label_year.pack(side=LEFT)
        self.label_buttons.pack(side=LEFT)
        self.frame_header.pack()

        self.lines = []
        for i in range(len(self.prizes)):
            self.lines.append({})
            self.lines[i]['frame'] = Frame(self)
            self.lines[i]['prize_id'] = self.prizes[i][0]
            self.lines[i]['entry_name'] = Entry(self.lines[i]['frame'], width=10)
            self.lines[i]['entry_nomination'] = Entry(self.lines[i]['frame'], width=10)
            self.lines[i]['entry_year'] = Entry(self.lines[i]['frame'], width=10)
            self.lines[i]['button'] = Button(self.lines[i]['frame'], width=5, text="Удалить")

            self.lines[i]['frame'].pack()
            self.lines[i]['entry_name'].pack(side=LEFT)
            self.lines[i]['entry_nomination'].pack(side=LEFT)
            self.lines[i]['entry_year'].pack(side=LEFT)
            self.lines[i]['button'].pack(side=LEFT)

        self.push_data()
        self.button_insert = Button(self, width=20, text="Добавить Приз", command=self.show_insert_prize)
        self.button_insert.pack()

    def push_data(self):
        for i in range(len(self.prizes)):
            self.lines[i]["entry_name"].insert(0, self.prizes[i][1])
            self.lines[i]["entry_nomination"].insert(0, self.prizes[i][3])
            self.lines[i]["entry_year"].insert(0, self.prizes[i][2])
            self.lines[i]["button"].bind('<Button-1>',
                                         lambda e, ind=self.lines[i]["prize_id"]: self.db.delete_prize(ind))

    def show_insert_prize(self):
        FilmsInsertPrize(self.film_id)
