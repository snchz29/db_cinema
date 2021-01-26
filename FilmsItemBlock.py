from tkinter import Label, Entry, Button, Frame, LEFT, END

from DbHolder import DbHolder
from FilmsActors import FilmsActors
from FilmsPrizes import FilmsPrizes
from FilmPoster import FilmPoster
from FilmSessions import FilmSessions


class FilmsItemBlock:
    db = DbHolder()
    ENTRY_WIDTH = 40

    def __init__(self, master, fid):
        self.film_id = fid
        self.label_name = Label(master, text="Название")
        self.label_producer = Label(master, text="Режиссер")
        self.label_operator = Label(master, text="Оператор")
        self.label_cost = Label(master, text="Стоимость")
        self.label_country = Label(master, text="Страна")
        self.label_duration = Label(master, text="Продолжительность")
        self.label_picture = Label(master, text="Ссылка на кадр")
        self.label_genres = Label(master, text="Жанры")
        self.entry_name = Entry(master, width=self.ENTRY_WIDTH)
        self.entry_producer = Entry(master, width=self.ENTRY_WIDTH)
        self.entry_operator = Entry(master, width=self.ENTRY_WIDTH)
        self.entry_cost = Entry(master, width=self.ENTRY_WIDTH)
        self.entry_country = Entry(master, width=self.ENTRY_WIDTH)
        self.entry_duration = Entry(master, width=self.ENTRY_WIDTH)
        self.entry_picture = Entry(master, width=self.ENTRY_WIDTH)
        self.entry_genres = Entry(master, width=self.ENTRY_WIDTH)

        self.frame_buttons = Frame(master)
        self.button_actors = Button(self.frame_buttons, text="Актеры", command=self.show_actors)
        self.button_prizes = Button(self.frame_buttons, text="Призы", command=self.show_prizes)
        self.button_picture = Button(self.frame_buttons, text="Показать кадр", command=self.show_picture)
        self.button_sessions = Button(self.frame_buttons, text="Сеансы", command=self.show_sessions)

        self.pack([
            self.label_name, self.entry_name,
            self.label_producer, self.entry_producer,
            self.label_operator, self.entry_operator,
            self.label_cost, self.entry_cost,
            self.label_country, self.entry_country,
            self.label_duration, self.entry_duration,
            self.label_picture, self.entry_picture,
            self.label_genres, self.entry_genres,
            self.frame_buttons,
        ], [
            self.button_actors,
            self.button_prizes,
            self.button_picture,
            self.button_sessions,
        ])

        self.index = 0
        self.update(self.index)

    def show_actors(self):
        FilmsActors(self.film_id)

    def show_prizes(self):
        FilmsPrizes(self.film_id)

    def pack(self, fields, buttons):
        for field in fields:
            field.pack()
        for button in buttons:
            button.pack(side=LEFT)

    def update(self, index, film_id=None):
        self.index = index
        if film_id:
            self.film_id = film_id
        list_films = self.db.get("films")
        genres = [i[0] for i in self.db.get_genres_by_film_id(self.film_id)]

        print("Films:", *list_films, sep="\n")
        if index < 0 or index > len(list_films):
            return
        self.erase_fields()
        if index != len(list_films):
            self.entry_name.insert(0, list_films[index][1])
            self.entry_producer.insert(0, list_films[index][2])
            self.entry_operator.insert(0, list_films[index][3])
            self.entry_cost.insert(0, list_films[index][4])
            self.entry_country.insert(0, list_films[index][5])
            self.entry_duration.insert(0, list_films[index][6])
            self.entry_picture.insert(0, list_films[index][7])
            self.entry_genres.insert(0, ", ".join(genres))

    def erase_fields(self):
        self.entry_name.delete(0, END)
        self.entry_producer.delete(0, END)
        self.entry_operator.delete(0, END)
        self.entry_cost.delete(0, END)
        self.entry_country.delete(0, END)
        self.entry_duration.delete(0, END)
        self.entry_picture.delete(0, END)
        self.entry_genres.delete(0, END)

    def show_picture(self):
        FilmPoster(self.film_id, self.entry_picture.get())

    def show_sessions(self):
        FilmSessions(self.film_id)
