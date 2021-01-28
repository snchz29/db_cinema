from Sessions import Sessions


class ActorSessions(Sessions):

    def __init__(self, actor, **kw):
        super().__init__(**kw)
        self.actor = actor
        self.sessions = self.db.get_sessions_by_actor(self.actor)
        self.title(f"Сеансы п.у. {self.actor[0]} {self.actor[1]}")
        self.make_table_header(
            {
                "Название фильма": 15,
                "Кинотеатр": 10,
                "Зал": 3,
                "Дата и время": 19,
                "Места": 5,
                "Цена": 5,
            }
        )
        self.make_table(len(self.sessions),
                        {
                            'film': 15,
                            'cinema': 10,
                            'room_number': 3,
                            'date_time': 19,
                            'seats': 5,
                            'cost': 5,
                        }
                        )

        self.push_data([
            {
                "film": session[1],
                "cinema": session[2],
                "room_number": session[3],
                "date_time": session[4],
                "seats": session[5],
                "cost": session[6]
            }
            for session in self.sessions])
