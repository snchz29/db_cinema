from tkinter import Toplevel, PhotoImage, Canvas, Label, Scrollbar
import io
from PIL import Image, ImageTk
import requests

from DbHolder import DbHolder


class FilmPoster(Toplevel):
    db = DbHolder()

    def __init__(self, fid, pic, **kw):
        super().__init__(**kw)
        self.grab_set()
        response = requests.get(pic)
        img_data = response.content
        bytes = Image.open(io.BytesIO(img_data))
        bytes.thumbnail((400, 400))
        img = ImageTk.PhotoImage(bytes)
        self.panel = Label(self, image=img)
        self.panel.image = img
        self.panel.place(x=0, y=0)
        self.geometry(f"{img.width()}x{img.height()}")
        self.resizable(False, False)
        film_name = self.db.get_films_by_id(fid)[0][1]
        self.title(film_name)


