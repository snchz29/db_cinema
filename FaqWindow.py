from tkinter import Toplevel, Button

from CinemaWindow import CinemaWindow
from FilmsWindow import FilmsWindow
from ReportWindow import ReportWindow
from ActorsWindow import ActorsWindow
from SearchWindow import SearchWindow


class FaqWindow(Toplevel):
    def __init__(self):
        super().__init__()
        self.grab_set()
        self.title("Справочная")
        self.geometry("200x350")
        self.resizable(False, False)
        self.button_cinema = Button(self, text="Кинотеатры", width=100, height=2, bg="lightblue",
                                    command=show_cinema_window)
        self.button_films = Button(self, text="Фильмы", width=100, height=2, bg="lightblue", command=show_films_window)
        self.button_actors = Button(self, text="Актеры", width=100, height=2, bg="lightblue",
                                    command=show_actors_window)
        self.button_search = Button(self, text="Поиск по дате", width=100, height=2, bg="lightblue",
                                     command=show_search_window)
        self.button_reports = Button(self, text="Отчет", width=100, height=2, bg="lightblue",
                                     command=show_report_window)
        self.button_cinema.pack(pady=10)
        self.button_films.pack(pady=10)
        self.button_actors.pack(pady=10)
        self.button_search.pack(pady=10)
        self.button_reports.pack(pady=10)


def show_cinema_window():
    CinemaWindow(is_faq=True)


def show_films_window():
    FilmsWindow()


def show_actors_window():
    ActorsWindow()


def show_report_window():
    ReportWindow()


def show_search_window():
    SearchWindow()
