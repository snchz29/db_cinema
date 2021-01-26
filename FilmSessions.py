from Sessions import Sessions


class FilmSessions(Sessions):

    def __init__(self, fid, **kw):
        super().__init__(**kw)
        self.film_id = fid
        self.sessions = self.db.get_sessions_by_film(self.film_id)
        film_name = self.db.get_films_by_id(self.film_id)[0][1]
        self.title(film_name)
        self.make_table_header(
            {
                "Кинотеатр": 10,
                "Зал": 3,
                "Дата и время": 19,
                "Места": 5,
                "Цена": 5,
            }
        )
        self.make_table(len(self.sessions),
                        {
                            'cinema': 10,
                            'room_number': 3,
                            'date_time': 19,
                            'seats': 5,
                            'cost': 5,
                        }
                        )
        self.push_data([
            {
                "cinema": session[1],
                "room_number": session[2],
                "date_time": session[3],
                "seats": session[4],
                "cost": session[5],
            }
            for session in self.sessions])
