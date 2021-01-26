import sqlite3
import functools


def find_best_id(ids):
    id_ = max(ids) + 1
    for i in range(1, max(ids) + 2):
        if i not in ids:
            id_ = i
            break
    return id_


def getter(decorated):
    @functools.wraps(decorated)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('data.sqlite')
        cursor = conn.cursor()
        cursor.execute(decorated(*args, **kwargs))
        res = cursor.fetchall()
        conn.close()
        return res
    return wrapper


def updater_deleter(decorated):
    @functools.wraps(decorated)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('data.sqlite')
        cursor = conn.cursor()
        cursor.execute(decorated(*args, **kwargs))
        conn.commit()
        conn.close()
    return wrapper


def inserter(decorated):
    @functools.wraps(decorated)
    def wrapper(self, *args, **kwargs):
        conn = sqlite3.connect('data.sqlite')
        cursor = conn.cursor()
        cursor.execute(decorated(self, *args, **kwargs))
        conn.commit()
        conn.close()
    return wrapper


class DbHolder:
    @staticmethod
    @getter
    def get(table: str):
        return f'SELECT * FROM {table}'

    @staticmethod
    @getter
    def get_cinema_by_id(cinema_id):
        return f'SELECT * FROM cinemas WHERE id="{cinema_id}"'

    @staticmethod
    @getter
    def get_sessions_by_cinema(cinema_id):
        return f'''SELECT sessions.id, rooms.number, name, date_time, films.cost / 10000 * (4-rooms.category) AS cost, seats
                   FROM sessions INNER JOIN films ON film_id = films.id
                   INNER JOIN rooms ON room_id = rooms.id
                   WHERE room_id IN (SELECT id 
                                     FROM rooms 
                                     WHERE cinema_id="{cinema_id}" OR cinema_id={cinema_id});'''

    @staticmethod
    @getter
    def get_sessions_by_film(film_id):
        return f'''SELECT sessions.id, cinemas.name, rooms.number, date_time, seats, 
                            films.cost / 10000 * (4-rooms.category) AS cost
                   FROM sessions INNER JOIN films ON film_id = films.id
                   INNER JOIN rooms ON room_id = rooms.id
                   INNER JOIN cinemas ON rooms.cinema_id = cinemas.id
                   WHERE film_id = "{film_id}" OR film_id = {film_id};'''

    @staticmethod
    @getter
    def get_sessions_by_film_and_cinema(film_id, cinema_id):
        return f'''SELECT sessions.id, cinemas.name, rooms.number, date_time, seats, 
                          films.cost / 10000 * (4-rooms.category) AS cost
                   FROM sessions INNER JOIN films ON film_id = films.id
                   INNER JOIN rooms ON room_id = rooms.id
                   INNER JOIN cinemas ON rooms.cinema_id = cinemas.id
                   WHERE (film_id = "{film_id}" OR film_id = {film_id}) AND 
                         (cinemas.id = "{cinema_id}" OR cinemas.id = {cinema_id});'''

    @staticmethod
    @getter
    def get_sessions_by_actor(actor_id):
        return f'''SELECT sessions.id, films.name, cinemas.name, rooms.number, date_time, seats, 
                            films.cost / 10000 * (4-rooms.category) AS cost
                   FROM sessions INNER JOIN films ON sessions.film_id = films.id
                   INNER JOIN roles ON roles.film_id = films.id
                   INNER JOIN actors ON actors.id = roles.actor_id
                   INNER JOIN rooms ON room_id = rooms.id
                   INNER JOIN cinemas ON rooms.cinema_id = cinemas.id
                   WHERE actors.id = "{actor_id}";'''

    @staticmethod
    @getter
    def get_sessions_by_date(date, time_b, time_e, genre):
        return f'''SELECT sessions.id, f.name, c.name, r.number, date_time, seats,
                          f.cost / 10000 * (4-r.category) AS cost, GROUP_CONCAT(g.genre)
                   FROM sessions INNER JOIN rooms r ON r.id = sessions.room_id
                   INNER JOIN cinemas c ON  c.id = r.cinema_id
                   INNER JOIN films f ON f.id = sessions.film_id AND "{genre}" IN (SELECT genre 
                                                                                   FROM genres 
                                                                                   WHERE f.id = genres.film_id)
                   INNER JOIN genres g ON f.id = g.film_id
                   GROUP BY sessions.id
                   HAVING date_time > "{date} {time_b}" AND date_time < "{date} {time_e}"'''

    @staticmethod
    @getter
    def get_room_by_id(room_ids):
        return f'''SELECT * FROM rooms  WHERE id IN ({",".join(["'" + str(i) + "'" for i in room_ids])})'''

    @staticmethod
    @getter
    def get_rooms_by_cinema(cinema_id):
        return f'''SELECT id, number, capacity FROM rooms  WHERE cinema_id="{str(cinema_id)}"'''

    @staticmethod
    @getter
    def get_films_by_id(film_ids):
        if film_ids:
            return f'''SELECT * FROM films 
                       WHERE id IN ({",".join(["'" + str(i) + "'" for i in film_ids])}) OR 
                             id IN ({",".join([str(i) for i in film_ids])}) '''
        else:
            return f'''SELECT * FROM films 
                       WHERE id="{film_ids}" OR id={film_ids}'''

    @staticmethod
    @getter
    def get_film_id_by_name(name, prod):
        return f'''SELECT id FROM films WHERE name="{name}" and producer="{prod}"'''

    @staticmethod
    @getter
    def get_films_by_cinema(cinema_id):
        return f'''SELECT films.id, films.name, films.producer, films.operator, films.country, films.duration, 
                          GROUP_CONCAT(DISTINCT genres.genre), films.picture
                   FROM films INNER JOIN sessions ON sessions.film_id = films.id
                              INNER JOIN rooms ON rooms.id = sessions.room_id AND rooms.cinema_id="{cinema_id}"
                              INNER JOIN genres ON films.id = genres.film_id
                   GROUP BY films.id;'''

    @staticmethod
    @getter
    def get_genres_by_film_id(film_id):
        return f'''SELECT genre FROM genres WHERE film_id="{str(film_id)}"'''

    @staticmethod
    @getter
    def get_roles_by_film_id(film_id):
        return f'''SELECT * FROM roles WHERE film_id="{str(film_id)}"'''

    @staticmethod
    @getter
    def get_actors_by_film_id(film_id):
        return f'''SELECT name, surname, role_name 
                   FROM actors INNER JOIN roles r on actors.id = r.actor_id 
                   WHERE r.film_id = "{str(film_id)}";'''

    @staticmethod
    @getter
    def get_actors_by_id(actors_ids):
        if type(actors_ids) is list:
            return f'''SELECT * FROM actors WHERE id IN ({",".join(['"' + str(i) + '"' for i in actors_ids])})'''
        else:
            return f'''SELECT * FROM actors WHERE id="{str(actors_ids)}"'''

    @staticmethod
    @getter
    def get_actor_by_name(name, surname, birth):
        return f'''SELECT * FROM actors WHERE name="{name}" AND surname="{surname}" AND birth="{birth}"'''

    @staticmethod
    @getter
    def get_prizes_by_film_id(film_id):
        return f'''SELECT * FROM prizes WHERE prizes.film_id="{str(film_id)}"'''

    @staticmethod
    @getter
    def get_report_by_cinema_films():
        return '''SELECT c.district, c.name, f.name, avg((4 - r.category) * f.cost/10000) AS avg_cost, count(s.id)
                  FROM films INNER JOIN sessions s ON films.id = s.film_id
                  INNER JOIN rooms r ON s.room_id = r.id
                  INNER JOIN cinemas c ON c.id = r.cinema_id
                  INNER JOIN films f ON f.id = s.film_id
                  GROUP BY cinema_id, film_id
                  ORDER BY district, c.name, f.name;'''

    @staticmethod
    @getter
    def get_report_cinemas_income():
        return '''SELECT sum(income), cinema, district
                  FROM (SELECT c.name as cinema, c.district as district, 
                               sum(r.capacity - sessions.seats) * avg((4 - r.category)*f.cost/10000) - f.cost as income
                        FROM sessions INNER JOIN rooms r ON r.id = sessions.room_id
                        INNER JOIN films f ON f.id = sessions.film_id
                        INNER JOIN cinemas c ON c.id = r.cinema_id
                        GROUP BY film_id, r.cinema_id
                        ORDER BY r.cinema_id)
                  GROUP BY cinema
                  ORDER BY district, cinema;'''

    @staticmethod
    @getter
    def get_report_district_income():
        return '''SELECT district, sum(income)
                  FROM (SELECT sum(income) AS income, district 
                        FROM (SELECT c.name AS cinema, c.district AS district, 
                                sum(r.capacity-sessions.seats) * avg(f.cost/10000 * (4 - r.category)) - f.cost AS income
                              FROM sessions INNER JOIN rooms r ON r.id = sessions.room_id
                              INNER JOIN films f ON f.id = sessions.film_id
                              INNER JOIN cinemas c ON c.id = r.cinema_id
                              GROUP BY film_id, r.cinema_id
                              ORDER BY r.cinema_id)
                        GROUP BY cinema)
                  GROUP BY district;'''

    @staticmethod
    @getter
    def get_report_full_income():
        return '''SELECT SUM(income)
                  FROM (SELECT district, sum(income) AS income
                        FROM (SELECT sum(income) AS income, district
                              FROM (SELECT c.name AS cinema, c.district AS district,
                                sum(r.capacity-sessions.seats) * avg(f.cost/10000 * (4 - r.category)) - f.cost AS income                                  
                                    FROM sessions INNER JOIN rooms r ON r.id = sessions.room_id
                                    INNER JOIN films f ON f.id = sessions.film_id                                  
                                    INNER JOIN cinemas c ON c.id = r.cinema_id                                  
                                    GROUP BY film_id, r.cinema_id                                  
                                    ORDER BY r.cinema_id)                            
                              GROUP BY cinema)                      
                        GROUP BY district);'''

    @staticmethod
    @getter
    def get_report_genres():
        return '''SELECT genre, count(film_id) FROM genres GROUP BY genre;'''

    @staticmethod
    @updater_deleter
    def update_cinemas(cinema_id, name, address, district, is_open):
        return f'''UPDATE cinemas 
                   SET name="{name}", address="{address}", district="{district}", is_open="{is_open}"    
                   WHERE id="{cinema_id}"'''

    @staticmethod
    @updater_deleter
    def update_session(session_id, room_id, date_time, seats):
        return f'''UPDATE sessions 
                   SET room_id="{room_id}", date_time="{date_time}", seats="{seats}" 
                   WHERE id="{session_id}"'''

    @staticmethod
    @updater_deleter
    def update_film(film_id, name, prod=None, operator=None, cost=None, country=None, duration=None, pic=None):
        if prod is None:
            return f'''UPDATE films SET name="{name}" WHERE id="{str(film_id)}"'''
        else:
            return f'''UPDATE films 
                       SET name="{name}", producer="{prod}", operator="{operator}", cost="{str(cost)}", 
                           country="{country}", duration="{str(duration)}", picture="{pic}"
                       WHERE id="{str(film_id)}"'''

    @staticmethod
    @updater_deleter
    def update_actor(actor_id, name, surname, birth):
        return f'''UPDATE actors 
                   SET name="{name}", surname="{surname}", birth="{birth}" 
                   WHERE id="{actor_id}"'''

    @inserter
    def insert_cinema(self, name, address, district, is_open):
        ids = list(map(int, [i[0] for i in self.get('cinemas')]))
        cinema_id = find_best_id(ids)
        return f'''INSERT INTO cinemas (id, name, address, district, is_open)
                   VALUES ("{str(cinema_id)}", "{name}", "{address}", "{district}", "{is_open}")'''

    @inserter
    def insert_room(self, cinema_id, number, capacity, category):
        ids = list(map(int, [i[0] for i in self.get('rooms')]))
        room_id = find_best_id(ids)
        return f'''INSERT INTO rooms (id, cinema_id, number, capacity, category)
                   VALUES ("{str(room_id)}", "{str(cinema_id)}", "{str(number)}", "{str(capacity)}", 
                           "{str(category)}")'''

    @inserter
    def insert_film(self, name, prod, operator, cost, country, duration, pic):
        ids = list(map(int, [i[0] for i in self.get('films')]))
        film_id = find_best_id(ids)
        return f'''INSERT INTO films (id, name, producer, operator, cost, country, duration, picture) 
                   VALUES ("{str(film_id)}", "{name}", "{prod}", "{operator}", "{str(cost)}", "{country}",
                           "{str(duration)}", "{pic}")'''

    @inserter
    def insert_session(self, room_id, film_id, date_time, seats):
        ids = list(map(int, [i[0] for i in self.get('sessions')]))
        session_id = find_best_id(ids)
        return f'''INSERT INTO sessions (id, room_id, film_id, date_time, seats) 
                   VALUES ("{str(session_id)}", "{str(room_id)}", "{str(film_id)}", "{date_time}", "{str(seats)}")'''

    @inserter
    def insert_genre(self, film_id, genre):
        ids = list(map(int, [i[0] for i in self.get('genres')]))
        genre_id = find_best_id(ids)
        return f'''INSERT INTO genres (id, film_id, genre) 
                   VALUES ("{str(genre_id)}", "{str(film_id)}", "{genre}")'''

    @inserter
    def insert_role(self, film_id, name, surname, birth, role):
        res = self.get_actor_by_name(name, surname, birth)
        if len(res) == 0:
            ids = list(map(int, [i[0] for i in self.get('actors')]))
            actor_id = find_best_id(ids)
            self.insert_actor(name, surname, birth)
        else:
            actor_id = res[0][0]
        ids = list(map(int, [i[0] for i in self.get('roles')]))
        role_id = find_best_id(ids)
        return f'''INSERT INTO roles (id, actor_id, film_id, role_name) 
                   VALUES ("{str(role_id)}","{str(actor_id)}","{str(film_id)}","{role}")'''

    @inserter
    def insert_actor(self, name, surname, birth):
        ids = list(map(int, [i[0] for i in self.get('actors')]))
        actor_id = find_best_id(ids)
        return f'''INSERT INTO actors (id, name, surname, birth) 
                   VALUES ("{str(actor_id)}","{name}","{surname}","{birth}")'''

    @inserter
    def insert_prize(self, film_id, name, year, nomination):
        ids = list(map(int, [i[0] for i in self.get('prizes')]))
        prize_id = find_best_id(ids)
        return f'''INSERT INTO prizes (id, name, year, nomination, film_id) 
                   VALUES ("{str(prize_id)}", "{name}", "{str(year)}", "{nomination}","{str(film_id)}")'''

    @inserter
    def delete_cinema(self, cinema_id):
        sessions_id = [s[0] for s in self.get_sessions_by_cinema(cinema_id)]
        self._delete_cinema_from_cinemas(cinema_id)
        self._delete_cinema_from_rooms(cinema_id)
        self._delete_cinema_from_sessions(sessions_id)

    @staticmethod
    @updater_deleter
    def _delete_cinema_from_cinemas(cinema_id):
        return f'''DELETE FROM cinemas WHERE id="{str(cinema_id)}"'''

    @staticmethod
    @updater_deleter
    def _delete_cinema_from_rooms(cinema_id):
        return f'''DELETE FROM rooms WHERE cinema_id="{str(cinema_id)}"'''

    @staticmethod
    @updater_deleter
    def _delete_cinema_from_sessions(sessions_id):
        return f'''DELETE FROM sessions WHERE id IN ({",".join(map(str, sessions_id))})'''

    def delete_film(self, film_id):
        self._delete_film_from_films(film_id)
        self._delete_film_from_roles(film_id)
        self.delete_genre(film_id)
        self._delete_film_from_prizes(film_id)

    @staticmethod
    @updater_deleter
    def _delete_film_from_films(film_id):
        return f'''DELETE FROM films WHERE id="{str(film_id)}";'''

    @staticmethod
    @updater_deleter
    def _delete_film_from_roles(film_id):
        return f'''DELETE FROM roles WHERE film_id="{str(film_id)}";'''

    @staticmethod
    @updater_deleter
    def _delete_film_from_prizes(film_id):
        return f'''DELETE FROM prizes WHERE film_id="{str(film_id)}"'''

    @staticmethod
    @updater_deleter
    def delete_session(session_id):
        return f'''DELETE FROM sessions WHERE id="{str(session_id)}"'''

    @staticmethod
    @updater_deleter
    def delete_genre(film_id):
        return f'''DELETE FROM genres WHERE film_id="{str(film_id)}"'''

    @staticmethod
    @updater_deleter
    def delete_role(role_id):
        return f'''DELETE FROM roles WHERE id="{str(role_id)}"'''

    def delete_actor(self, actor_id):
        self._delete_actor_from_actors(actor_id)
        self._delete_actor_from_roles(actor_id)

    @staticmethod
    @updater_deleter
    def _delete_actor_from_actors(actor_id):
        return f'''DELETE FROM actors WHERE id="{str(actor_id)}"'''

    @staticmethod
    @updater_deleter
    def _delete_actor_from_roles(actor_id):
        return f'''DELETE FROM roles WHERE actor_id="{str(actor_id)}"'''

    @staticmethod
    @updater_deleter
    def delete_prize(prize_id):
        return f'''DELETE FROM prizes WHERE id="{str(prize_id)}"'''
