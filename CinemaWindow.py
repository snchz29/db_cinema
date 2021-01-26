from tkinter import Toplevel, Button, LEFT, RIGHT, BOTTOM, NORMAL, DISABLED, Frame

from DbHolder import DbHolder
from CinemaItemBlock import CinemaItemBlock
from PostersWindow import PostersWindow


class CinemaWindow(Toplevel):
    db = DbHolder()

    def __init__(self, is_faq=False, **kw):
        super().__init__(**kw)
        self.grab_set()
        self.geometry('500x300')
        self.title("Кинотеатры")
        self.resizable(False, False)
        self.is_faq = is_faq
        self.cur_index = 0
        self.cur_id = self.db.get("cinemas")[self.cur_index][0]
        self.block_content = CinemaItemBlock(self, self.cur_id)
        self.frame_buttons = Frame(self)
        self.frame_buttons.pack(side=BOTTOM)
        self.button_prev = Button(self.frame_buttons, text="<", command=self.click_prev)
        self.button_prev.pack(anchor="s", side=LEFT)
        self.button_next = Button(self.frame_buttons, text=">", command=self.click_next)
        self.button_next.pack(anchor="s", side=RIGHT)
        self.button_edit = Button(self.frame_buttons, text="Изменить", command=self.edit_cinema, state=NORMAL)
        self.button_edit.pack(side=LEFT)
        self.button_drop = Button(self.frame_buttons, text="Удалить", command=self.delete_cinema,
                                  state=NORMAL if self.is_faq else DISABLED)
        self.button_drop.pack(side=LEFT)
        self.button_poster = Button(self.frame_buttons, text="Афиши", command=self.show_poster,
                                    state=NORMAL)
        self.button_poster.pack(side=LEFT)

    def show_poster(self):
        PostersWindow(self.cur_id)

    def delete_cinema(self):
        self.db.delete_cinema(self.cur_id)
        self.click_prev()

    def edit_cinema(self):
        fields = self.block_content
        if fields.entry_is_open.get() not in ('0', '1'):
            return
        self.db.update_cinemas(self.cur_id, fields.entry_name.get(), fields.entry_address.get(),
                               fields.entry_district.get(), fields.entry_is_open.get())

    def insert_cinema(self):
        fields = self.block_content
        if fields.entry_is_open.get() not in ('0', '1'):
            return
        self.db.insert_cinema(fields.entry_name.get(), fields.entry_address.get(), fields.entry_district.get(),
                              fields.entry_is_open.get())
        self.button_edit.config(text="Изменить", command=self.edit_cinema)
        self.button_drop.config(state=NORMAL)
        self.button_poster.config(state=NORMAL)
        fields.button_sessions.config(state=NORMAL)

    def click_prev(self):
        self.cur_index -= 1
        if self.cur_index < 0:
            self.cur_index = 0
        self.cur_id = self.db.get("cinemas")[self.cur_index][0]
        self.button_edit.config(text="Изменить", command=self.edit_cinema)
        self.button_drop.config(state=NORMAL if self.is_faq else DISABLED)
        self.button_poster.config(state=NORMAL)
        self.block_content.button_sessions.config(state=NORMAL)
        self.block_content.update(self.cur_index, self.cur_id)

    def click_next(self):
        self.cur_index += 1
        if self.cur_index >= len(self.db.get("cinemas")) and not self.is_faq:
            self.cur_index -= 1

        if self.cur_index >= len(self.db.get("cinemas")) and self.is_faq:
            self.cur_index = len(self.db.get("cinemas"))
            self.button_edit.config(text="Добавить", command=self.insert_cinema)
            self.button_drop.config(state=DISABLED)
            self.button_poster.config(state=DISABLED)
            self.block_content.button_sessions.config(state=DISABLED)
        else:
            self.cur_id = self.db.get("cinemas")[self.cur_index][0]
        self.block_content.update(self.cur_index, self.cur_id)
