from tkinter import Toplevel, Button, Text, END, Scrollbar, LEFT, Y
from DbHolder import DbHolder


class ReportWindow(Toplevel):
    db = DbHolder()

    def __init__(self, **kw):
        super().__init__(**kw)
        self.grab_set()
        self.geometry("750x500")
        self.title("Отчет")
        self.text_field = Text(self, width=92, height=50)
        self.text_field.bind("<Key>", lambda e: "break")
        self.text_field.pack(side=LEFT)
        self.scroll = Scrollbar(command=self.text_field.yview)
        self.scroll.pack(side=LEFT, fill=Y)
        self.text_field.config(yscrollcommand=self.scroll.set)
        self.push()

    def push(self):
        films = self.db.get_report_by_cinema_films()
        cinemas = self.db.get_report_cinemas_income()
        districts = self.db.get_report_district_income()
        print(films)
        tmp_districts = []
        tmp_cinemas = []
        cinema_ind = 0
        distr_ind = 0
        self.text_field.insert(END, "Отчет по районам\n")
        self.text_field.insert(END, "Суммарный доход: " + str(self.db.get_report_full_income()[0][0]) + "\n")

        for film in films:
            if film[0] not in tmp_districts:
                tmp_districts.append(film[0])
                self.text_field.insert(END, film[0] + "\n" + "Доход: " + str(round(districts[distr_ind][1], 2)) + "\n")
                distr_ind += 1
            if film[1] not in tmp_cinemas:
                tmp_cinemas.append(film[1])
                self.text_field.insert(END, "\t" + film[1] + "\n\t" + "Доход: " + str(
                    round(cinemas[cinema_ind][0], 2)) + "\n")
                cinema_ind += 1
            self.text_field.insert(END,
                                   "\t\t" + film[2] + "   Кол-во сеансов:" + str(film[4]) + "   Средняя цена:" + str(
                                       round(film[3], 2)) + "\n")
        genres = self.db.get_report_genres()
        self.text_field.insert(END, "\nОтчет по жанрам\n")
        for g in genres:
            self.text_field.insert(END, g[0] + "\t\t" + str(g[1]) + "\n")
