from tkinter import Tk, Button

from CinemaWindow import CinemaWindow
from FilmsWindow import FilmsWindow
from FaqWindow import FaqWindow


class Root(Tk):
    def __init__(self):
        super().__init__()
        self.grab_set()
        self.title("Кинотеатры")
        self.geometry("200x200")
        self.resizable(False, False)
        self.button1 = Button(self, text="Кинотеатры", width=100, height=2, bg="lightblue", command=show_cinema_window)
        self.button2 = Button(self, text="Справочная", width=100, height=2, bg="lightblue", command=show_faq_window)
        self.button3 = Button(self, text="Выход", width=100, height=2, bg="lightblue", command=self.quit)
        self.button1.pack(pady=10)
        self.button2.pack(pady=10)
        self.button3.pack(pady=10)


def show_cinema_window():
    CinemaWindow()


def show_films_window():
    FilmsWindow()

def show_faq_window():
    FaqWindow()