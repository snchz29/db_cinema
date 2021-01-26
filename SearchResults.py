from Sessions import Sessions


class SearchResults(Sessions):
    def __init__(self, results, **kw):
        super().__init__(**kw)
        self.sessions = results
        self.title("Результаты поиска")
        self.make_table_header(
            {
                "Кинотеатр": 10,
                "Название фильма": 15,
                "Зал": 3,
                "Дата и время": 19,
                "Места": 5,
                "Цена": 5,
                "Жанры": 15,
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
                            'genres': 15,
                        }
                        )
        self.push_data([
            {
                "film": session[1],
                "cinema": session[2],
                "room_number": session[3],
                "date_time": session[4],
                "seats": session[5],
                "cost": session[6],
                "genres": session[7],
            }
            for session in self.sessions])
