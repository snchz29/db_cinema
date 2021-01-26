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
        self.cur_id = self.db.get("actors")[self.cur_index][0]
        self.frame_buttons = Frame(self)
        self.frame_buttons.pack(side=BOTTOM)
        self.button_prev = Button(self.frame_buttons, text="<", command=self.click_prev)
        self.button_prev.pack(anchor="s", side=LEFT)
        self.block_content = ActorItemBlock(self, self.cur_id)
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
        self.cur_id = self.db.get("actors")[self.cur_index][0]
        self.button_edit.config(text="Изменить", command=self.edit_actor)
        self.button_drop.config(state=NORMAL)
        self.block_content.update(self.cur_index, self.cur_id)

    def click_next(self):
        self.cur_index += 1
        if self.cur_index >= len(self.db.get("actors")):
            self.cur_index = len(self.db.get("actors"))
            self.button_edit.config(text="Добавить", command=self.insert_actor)
            self.button_drop.config(state=DISABLED)
        else:
            self.cur_id = self.db.get("actors")[self.cur_index][0]
        self.block_content.update(self.cur_index, self.cur_id)

    def delete_actor(self):
        print(self.cur_id)
        self.db.delete_actor(self.cur_id)
        self.click_prev()

    def edit_actor(self):
        fields = self.block_content
        self.db.update_actor(self.cur_id, fields.entry_name.get(), fields.entry_surname.get(), fields.entry_birth.get())

    def insert_actor(self):
        fields = self.block_content
        reg = r'[12]\w\w\w-[01]\w-[0123]\w'
        if len(fields.entry_birth.get()) != 10 or not re.match(reg, fields.entry_birth.get()):
            print("Bad Date")
            return
        self.db.insert_actor(fields.entry_name.get(), fields.entry_surname.get(), fields.entry_birth.get())
        self.button_edit.config(text="Изменить", command=self.edit_actor)
        self.button_drop.config(state=NORMAL)
