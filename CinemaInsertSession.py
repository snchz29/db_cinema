import re
from tkinter import Toplevel, Frame, LabelFrame, Label, Entry, Button, LEFT, BOTTOM

from DbHolder import DbHolder


class CinemaInsertSession(Toplevel):
    db = DbHolder()

    def __init__(self, cid, **kw):
        super().__init__(**kw)
        self.grab_set()
        self.cinema_id = cid
        self.title(self.db.get_cinema_by_id(self.cinema_id)[0][1])
        self.resizable(False, False)
        self.entry_room_number = None
        self.entry_capacity = None
        self.entry_category = None
        self.entry_number = None
        self.entry_film_name = None
        self.entry_film_prod = None
        self.entry_date_time = None
        self.entry_seats = None
        self.setup()

    def setup(self):
        self.setup_room()
        self.setup_session()

    @staticmethod
    def _setup_entry(parent_frame, verbose, label_width):
        frame = Frame(parent_frame)
        label = Label(frame, text=verbose, width=label_width)
        entry = Entry(frame)
        frame.pack(anchor="w")
        label.pack(side=LEFT)
        entry.pack(side=LEFT)
        return entry

    def setup_room(self):
        width = 12
        frame_room = LabelFrame(self, text="Зал")
        self.entry_room_number = self._setup_entry(frame_room, 'Номер', width)
        self.entry_capacity = self._setup_entry(frame_room, 'Вместимость', width)
        self.entry_category = self._setup_entry(frame_room, 'Категория', width)
        self.label_status_room = Label(frame_room)
        self.label_status_room.pack(anchor="w")
        button_insert = Button(frame_room, text="Добавить зал", command=self.insert_room)
        button_insert.pack(anchor="e")
        frame_room.pack()

    def setup_session(self):
        width = 19
        frame_session = LabelFrame(self, text="Сеанс")
        self.entry_number = self._setup_entry(frame_session, 'Номер зала', width)
        self.entry_film_name = self._setup_entry(frame_session, 'Название фильма', width)
        self.entry_film_prod = self._setup_entry(frame_session, 'Режиссер', width)
        self.entry_date_time = self._setup_entry(frame_session, 'Дата и время сеанса', width)
        self.entry_seats = self._setup_entry(frame_session, 'Места', width)
        self.label_status_session = Label(frame_session)
        self.label_status_session.pack(anchor="w")
        frame_session.pack()
        button_insert = Button(frame_session, text="Добавить сеанс", command=self.insert_session)
        button_insert.pack(anchor="e", side=BOTTOM)

    def insert_room(self):
        cinema_id, number, capacity, category = str(self.cinema_id), str(self.entry_room_number.get()), \
                                                self.entry_capacity.get(), self.entry_category.get()
        print(cinema_id, number, capacity, category, sep='\n')
        print([i[0] for i in self.db.get_rooms_by_cinema(cinema_id)])
        if number in [i[0] for i in self.db.get_rooms_by_cinema(cinema_id)]:
            self.print_status(self.label_status_room, "Bad number")
            print("Bad number")
            return
        if not 0 < int(category) < 4:
            self.print_status(self.label_status_room, "Bad category")
            print("Bad category")
            return
        if int(capacity) > 120:
            self.print_status(self.label_status_room, "Bad capacity")
            print("Bad capacity")
            return
        self.db.insert_room(cinema_id, number, capacity, category)
        self.print_status(self.label_status_room, "Success")

    def insert_session(self):
        number, name, prod, date_time, seats = self.entry_number.get(), self.entry_film_name.get(), \
                                               self.entry_film_prod.get(), self.entry_date_time.get(), \
                                               self.entry_seats.get()
        cinema_rooms = self.db.get_rooms_by_cinema(self.cinema_id)
        if number not in [i[0] for i in cinema_rooms]:
            self.print_status(self.label_status_session, "Bad number")
            print("Bad number")
            return
        room_id = cinema_rooms[[i[0] for i in cinema_rooms].index(number)][1]
        film_id = None
        try:
            film_id = self.db.get_film_id_by_name(name, prod)[0][0]
        except IndexError:
            self.print_status(self.label_status_session, "Bad film")
            print("Bad film")
            return
        reg = r'[12]\w\w\w-[01]\w-[0123]\w [012]\w:[0-6]\w:00'
        if len(date_time) != 19 or not re.match(reg, date_time):
            self.print_status(self.label_status_session, "Bad Date&time")
            print("Bad Date&time")
            return
        print(self.db.get_room_by_id(room_id))
        if int(seats) > int(self.db.get_room_by_id(room_id)[0][3]):
            self.print_status(self.label_status_session, "Bad seats")
            print("Bad seats")
            return
        self.db.insert_session(room_id, film_id, date_time, seats)

    def print_status(self, label: Label, status: str) -> None:
        label.config(text=status)
        self.after(3000, lambda: label.config(text=""))
