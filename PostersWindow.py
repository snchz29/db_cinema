from tkinter import Toplevel, Frame, Button, BOTTOM, LEFT, RIGHT, Canvas, CENTER
import io
from PIL import Image, ImageTk
import requests

from DbHolder import DbHolder


class PostersWindow(Toplevel):
    db = DbHolder()

    def __init__(self, cid, **kw):
        super().__init__(**kw)
        self.grab_set()
        self.geometry("500x700")
        self.resizable(False, False)
        self.title("Афиши")
        self.cinema_id = cid
        self.cur_index = 0
        self.films = self.db.get_films_by_cinema(self.cinema_id)
        if len(self.films) == 0:
            self.destroy()
            return
        self.img = None
        print(self.films)
        self.canvas = Canvas(self, width=500, height=670, bg='white')
        self.canvas.pack()
        self.frame_buttons = Frame(self)
        self.button_prev = Button(self.frame_buttons, text="<", command=self.click_prev)
        self.button_next = Button(self.frame_buttons, text=">", command=self.click_next)
        self.frame_buttons.pack(side=BOTTOM)
        self.button_prev.pack(side=LEFT)
        self.button_next.pack(side=RIGHT)
        self.render()

    def click_prev(self):
        self.cur_index = (self.cur_index - 1) % len(self.films)
        self.render()

    def click_next(self):
        self.cur_index = (self.cur_index + 1) % len(self.films)
        self.render()

    def render(self):
        self._clear()
        film = self.films[self.cur_index]
        self._render_main(film)
        height_sessions = max(self._render_prizes(film), self._render_actors(film))
        self._render_sessions(film, height_sessions)

    def _clear(self):
        self.canvas.create_rectangle(0, 0, 500, 670, fill='white', outline='white')

    def _render_main(self, film):
        cv = self.canvas
        response = requests.get(film[7])
        img_data = response.content
        img_bytes = Image.open(io.BytesIO(img_data))
        img_bytes.thumbnail((300, 300))
        self.img = ImageTk.PhotoImage(img_bytes)
        cv.create_image(490, img_bytes.size[1], anchor="se", image=self.img)
        cv.create_text(10, 20, text=f"{film[1]} ({film[4]})", justify=LEFT, anchor="w", font="KacstPoster 10")
        cv.create_text(10, 50, text=f"Режиссер: {film[2]}", justify=LEFT, anchor="w", font="KacstPoster 10")
        cv.create_text(10, 80, text=f"Оператор: {film[3]}", justify=LEFT, anchor="w", font="KacstPoster 10")
        cv.create_text(10, 110, text=f"Продолжительность: {film[5]} мин.", justify=LEFT, anchor="w",
                       font="KacstPoster 10")
        nl = '\n'
        cv.create_text(10, 140, text=f"Жанры: {film[6].replace(',', nl+' '*20)}", justify=LEFT, anchor="w",
                       font="KacstPoster 10")

    def _render_prizes(self, film):
        prizes = self.db.get_prizes_by_film_id(film[0])
        height_prizes = 320
        if len(prizes) == 0:
            return height_prizes
        cv = self.canvas
        cv.create_text(125, height_prizes, text="Призы", justify=CENTER, font="KacstPoster 10")
        height_prizes += 20
        for prize in prizes:
            cv.create_text(10, height_prizes, text=f"* {prize[1]} {prize[2]}\n  {prize[3]}", justify=LEFT, anchor="w", font="KacstPoster 7")
            height_prizes += 25
        return height_prizes

    def _render_actors(self, film):
        actors = self.db.get_actors_by_film_id(film[0])
        height_actors = 320
        if len(actors) == 0:
            return height_actors
        cv = self.canvas
        cv.create_text(375, height_actors, text="В ролях", justify=CENTER, font="KacstPoster 10")
        height_actors += 20
        for actor in actors:
            cv.create_text(260, height_actors, text=f"{actor[0]} {actor[1]} -- {actor[2]}", justify=LEFT, anchor="w", font="KacstPoster 7")
            height_actors += 20
        return height_actors

    def _render_sessions(self, film, height_sessions):
        sessions = self.db.get_sessions_by_film_and_cinema(film[0], self.cinema_id)
        if len(sessions) == 0:
            return
        cv = self.canvas
        height_sessions += 25
        cv.create_text(250, height_sessions, text="Сеансы", justify=CENTER, font="KacstPoster 15")
        height_sessions += 25
        cv.create_text(100, height_sessions, text="Начало сеанса", justify=CENTER, font="KacstPoster 10")
        cv.create_text(250, height_sessions, text="Свободные места", justify=CENTER, font="KacstPoster 10")
        cv.create_text(400, height_sessions, text="Цена билета", justify=CENTER, font="KacstPoster 10")
        height_sessions += 20
        for session in sessions:
            cv.create_text(100, height_sessions, text=f"{session[3]}", justify=CENTER, font="KacstPoster 10")
            cv.create_text(250, height_sessions, text=f"{session[4]}", justify=CENTER, font="KacstPoster 10")
            cv.create_text(400, height_sessions, text=f"{session[5]}", justify=CENTER, font="KacstPoster 10")
            height_sessions += 20
