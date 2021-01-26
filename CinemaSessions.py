from tkinter import Button
import re

from CinemaInsertSession import CinemaInsertSession
from Sessions import Sessions


class CinemaSessions(Sessions):
    def __init__(self, cid, **kw):
        super().__init__(**kw)
        self.button_insert = Button(self, width=30, text="Добавить", command=self.insert_session)
        self.button_upgrade = Button(self, width=30, text="Обновить", command=self.update_db)
        self.cinema_id = cid
        self.sessions = self.db.get_sessions_by_cinema(self.cinema_id)
        self.title("Сеансы " + self.db.get_cinema_by_id(self.cinema_id)[0][1])

        self.make_table_header(
            {
                "№": 2,
                "Фильм": 20,
                "Дата и время сеанса": 20,
                "Цена": 6,
                "Места": 5,
                "": 5,
            }
        )

        self.make_table(len(self.sessions),
                        {
                            "number": 2,
                            "film": 20,
                            "date_time": 20,
                            "cost": 6,
                            "seats": 5,
                        },
                        {
                            "drop": "DEL",
                        }
                        )

        self.prepare_data()
        self.button_upgrade.pack()
        self.button_insert.pack()

    def update_db(self):
        for i in range(len(self.sessions)):
            number = self.lines[i]["number"].get()
            film = self.lines[i]["film"].get()
            date_time = self.lines[i]["date_time"].get()
            seats = self.lines[i]["seats"].get()
            rooms = self.db.get_rooms_by_cinema(self.cinema_id)
            if number not in [room[0] for room in rooms]:
                print("Bad Number")
                break
            reg = r'[12]\w\w\w-[01]\w-[0123]\w [012]\w:[0-6]\w:00'
            if len(date_time) != 19 or not re.match(reg, date_time):
                print("Bad Date&time")
                break
            print(rooms)
            print(self.sessions)
            print([room[2] for room in rooms if int(room[1]) == int(self.sessions[i][1])])
            if int(seats) > int([room[2] for room in rooms if int(room[1]) == int(self.sessions[i][1])][0]):
                print("Bad Seats")
                break
            self.db.update_session(self.sessions[i][0], number, date_time, seats)
            self.db.update_film(self.sessions[i][2], film)

    def insert_session(self):
        CinemaInsertSession(self.cinema_id)

    def prepare_data(self):
        self.push_data([
            {
                "number": session[1],
                "film": session[2],
                "date_time": session[3],
                "cost": session[4],
                "seats": session[5],
            }
            for session in self.sessions])
        for i in range(len(self.sessions)):
            self.lines[i]["id"] = self.sessions[i][0]
            self.lines[i]["drop"].bind('<Button-1>', lambda e, ind=self.lines[i]["id"]: self.db.delete_session(ind))
