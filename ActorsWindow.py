import re
from tkinter import Toplevel, Button, LEFT, RIGHT, BOTTOM, NORMAL, DISABLED, Frame

from DbHolder import DbHolder
from ActorItemBlock import ActorItemBlock


class ActorsWindow(Toplevel):
    db = DbHolder()

    def __init__(self, **kw):
        super().__init__(**kw)
        self.grab_set()
        self.resizable(False, False)
        self.geometry("300x300")
        self.title("Актеры")
        self.cur_index = 0
        self.cur_actor = self.db.get_actors()[self.cur_index]
        self.frame_buttons = Frame(self)
        self.frame_buttons.pack(side=BOTTOM)
        self.button_prev = Button(self.frame_buttons, text="<", command=self.click_prev)
        self.button_prev.pack(anchor="s", side=LEFT)
        self.block_content = ActorItemBlock(self, self.cur_actor)
        self.button_next = Button(self.frame_buttons, text=">", command=self.click_next)
        self.button_next.pack(anchor="s", side=RIGHT)
        self.button_edit = Button(self.frame_buttons, text="Изменить", command=self.edit_actor)
        self.button_edit.pack(side=LEFT)
        self.button_drop = Button(self.frame_buttons, text="Удалить", command=self.delete_actor)
        self.button_drop.pack(side=LEFT)

    def click_prev(self):
        self.cur_index -= 1
        if self.cur_index < 0:
            self.cur_index = 0
            return
        self.cur_actor = self.db.get_actors()[self.cur_index]
        self.button_edit.config(text="Изменить", command=self.edit_actor)
        self.button_drop.config(state=NORMAL)
        self.block_content.update(self.cur_actor)

    def click_next(self):
        self.cur_index += 1
        if self.cur_index >= len(self.db.get_actors()):
            self.cur_index = len(self.db.get_actors()) - 1
        self.cur_actor = self.db.get_actors()[self.cur_index]
        self.block_content.update(self.cur_actor)

    def delete_actor(self):
        self.db.delete_actor(self.cur_actor)
        self.click_prev()

    def edit_actor(self):
        fields = self.block_content
        self.db.update_actor(self.cur_actor, fields.entry_name.get(), fields.entry_surname.get(), fields.entry_birth.get())

