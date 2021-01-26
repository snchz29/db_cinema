from tkinter import Toplevel, Button, LEFT, RIGHT, BOTTOM, NORMAL, DISABLED, END, Frame

from DbHolder import DbHolder
from FilmsItemBlock import FilmsItemBlock


class FilmsWindow(Toplevel):
    db = DbHolder()
    cur_index = 0
    cur_id = db.get("films")[cur_index][0]

    def __init__(self, **kw):
        super().__init__(**kw)
        self.grab_set()
        self.geometry('500x500')
        self.resizable(False, False)
        self.title("Фильмы")
        self.frame_buttons = Frame(self)
        self.frame_buttons.pack(side=BOTTOM)
        self.button_prev = Button(self.frame_buttons, text="<", command=self.click_prev)
        self.button_prev.pack(side=LEFT)
        self.block_content = FilmsItemBlock(self, self.cur_id)
        self.button_next = Button(self.frame_buttons, text=">", command=self.click_next)
        self.button_next.pack(side=RIGHT)
        self.button_edit = Button(self.frame_buttons, text="Изменить", command=self.edit_film)
        self.button_edit.pack(side=LEFT)
        self.button_drop = Button(self.frame_buttons, text="Удалить", command=self.delete_film)
        self.button_drop.pack(side=LEFT)

    def delete_film(self):
        self.db.delete_film(self.cur_id)
        self.click_prev()
        pass

    def edit_film(self):
        fields = self.block_content
        if int(fields.entry_cost.get()) < 10000:
            return
        if int(fields.entry_duration.get()) < 5:
            return
        self.db.update_film(self.cur_id, fields.entry_name.get(), fields.entry_producer.get(),
                            fields.entry_operator.get(), fields.entry_cost.get(), fields.entry_country.get(),
                            fields.entry_duration.get(), fields.entry_picture.get())
        self.db.delete_genre(self.cur_id)
        text = fields.entry_genres.get()
        for g in text.split(", "):
            if len(g) > 0:
                self.db.insert_genre(self.cur_id, g)

    def insert_film(self):
        fields = self.block_content
        if int(fields.entry_cost.get()) < 10000:
            return
        if int(fields.entry_duration.get()) < 5:
            return
        self.db.insert_film(fields.entry_name.get(), fields.entry_producer.get(), fields.entry_operator.get(),
                            fields.entry_cost.get(), fields.entry_country.get(), fields.entry_duration.get(),
                            fields.entry_picture.get())
        self.button_edit.config(text="Изменить", command=self.edit_film)
        self.button_drop.config(state=NORMAL)
        self.cur_id = self.db.get("films")[self.cur_index][0]
        print("CUR:",self.cur_id)

    def click_prev(self):
        self.cur_index -= 1
        if self.cur_index < 0:
            self.cur_index = 0
        self.cur_id = self.db.get("films")[self.cur_index][0]
        self.button_edit.config(text="Изменить", command=self.edit_film)
        self.button_drop.config(state=NORMAL)
        self.block_content.button_sessions.config(state=NORMAL)
        self.block_content.button_actors.config(state=NORMAL)
        self.block_content.button_prizes.config(state=NORMAL)
        self.block_content.update(self.cur_index, self.cur_id)

    def click_next(self):
        self.cur_index += 1
        if self.cur_index >= len(self.db.get("films")):
            self.cur_index = len(self.db.get("films"))
            self.button_edit.config(text="Добавить", command=self.insert_film)
            self.button_drop.config(state=DISABLED)
            self.block_content.button_sessions.config(state=DISABLED)
            self.block_content.button_actors.config(state=DISABLED)
            self.block_content.button_prizes.config(state=DISABLED)
        else:
            self.cur_id = self.db.get("films")[self.cur_index][0]
        self.block_content.update(self.cur_index, self.cur_id)
