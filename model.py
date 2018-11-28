# YOUR BOT LOGIC/STORAGE/BACKEND FUNCTIONS HERE
import datetime
import requests
import db_management as DB
import secret_settings


class Model:
    def __init__(self):
        pass

    def add_user(self, chat_id):
        if not DB.find_user(chat_id):
            DB.insert_user(chat_id)
            return True
        return False

    def add_movie(self, chat_id, movie_name):
        querystring = {"query": movie_name.replace(" ", "+"),"n": 1}
        response = requests.request("GET", secret_settings.url_movieglu_api + "filmLiveSearch/",
                                    headers=secret_settings.headers_movieglu_api, params=querystring)
        movie_id = response.json()['films'][0]['film_id']
        movie = self.get_film_details(movie_id)
        movie_det = {"film_id":movie_id, "movie_name":movie_name,
        "ganer": movie['genres'][0]['genre_id'], "cast": [c['cast_id'] for c in movie["cast"]], "directors": [
            c['director_id'] for c in movie["directors"]]}
        DB.DBManagement.insert_movie(chat_id, movie_det)

    def get_recommended_movies(self, chat_id,lat,lon,date):
        cinemas = self.get_cinemas_nearby(3, lat,lon)
        films = []
        movies = []
        for cinema in cinemas:
            films.append({"cinema":cinema, "films":self.get_cinema_show_times(cinema['cinema_id'], date)})

        for film in films:
            for f in film["films"]:
                movie_det = self.get_film_details(f['film_id'])
                trailer = movie_det['trailers']['med'][0]['film_trailer']
                image = movie_det['images']['poster']['1']['medium']['film_image']
                movies.append({"cinema":film['cinema'], "ganer":movie_det['genres'][0]['genre_id'], "cast":[c['cast_id']for c in movie_det["cast"]],"directors": [c['director_id']for c in movie_det["directors"]],"trailers":trailer ,"images":image})

        recommend = []
        my_movies = self.get_all_movies(chat_id)
        for my_movie in my_movies:
            for movie in movies:
                if my_movie['ganer'] ==  movie['ganer'] or set(my_movie['cast'])^set(movie['cast']) or set(my_movie['directors'])^set(movie['directors']):
                    recommend.append(movies)

        return movies







    def get_recommended_name_movie(self, chosen_movie):
        return chosen_movie

    def get_recommended_place_movie(self, chosen_movie):
        pass

    def get_recommended_time_movie(self, chosen_movie):
        pass

    def get_recommended_trailer_movie(self, chosen_movie_id):
        querystring = {"film_id": chosen_movie_id}
        response = requests.request("GET", secret_settings.url_movieglu_api + "trailers/",
                                    headers=secret_settings.headers_movieglu_api, params=querystring)
        return response.json()['trailers']['high'][0]['film_trailer']

    def get_recommended_image_movie(self, chosen_movie_id):
        querystring = {"film_id": chosen_movie_id}
        response = requests.request("GET", secret_settings.url_movieglu_api + "images/",
                                    headers=secret_settings.headers_movieglu_api, params=querystring)
        return response.json()['poster']['1']['medium']['film_image']

    def choose_movie(self, chat_id, movie):
        DB.insert_chosen_movie(chat_id, movie)
    # movie type is list/tuple of all movie info

    def get_chosen_movie(self, chat_id):
        return DB.get_chosen_movie(chat_id)

    def delete_movie(self, chat_id, movie):
        pass
        # optional

    def delete_all_movies(self, chat_id):
        DB.delete_all_movies(chat_id)

    def choose_date(self, chat_id, date=datetime.datetime.now(), is_notification = True):
        DB.insert_date(chat_id, date, is_notification)

    def get_all_movies(self, chat_id):
        return DB.get_all_movies(chat_id)

    def get_date(self, chat_id):
        return DB.get_date(chat_id)

    def get_cinemas_nearby(self, n_cinemas, lat, lon):
        querystring = {"n": n_cinemas}
        headers = secret_settings.headers_movieglu_api
        headers['geolocation'] = f"{lat};{lon}"
        response = requests.request("GET", secret_settings.url_movieglu_api + "cinemasNearby/",
                                    headers=headers, params=querystring)
        cinemas = response.json()['cinemas']
        return cinemas

    def get_cinema_show_times(self, cinema_id, date):
        querystring = {"cinema_id": cinema_id, "date": date}
        headers = secret_settings.headers_movieglu_api
        response = requests.request("GET", secret_settings.url_movieglu_api + "cinemaShowTimest/",
                                    headers=headers, params=querystring)
        result = response.json()
        films = result['films']
        return films


    def get_film_details(self, movie_id):
        querystring = {"film_id": movie_id}
        response = requests.request("GET", secret_settings.url_movieglu_api+"filmDetails/", headers=secret_settings.headers_movieglu_api, params=querystring)
        return response

    def notify(self, chat_id, time_before=60):
        pass


m = Model()
m.add_movie("star wars")
#print(m.get_cinemas_nearby(5, 40.692532, -73.990997))
#print(m.get_cinema_show_times(7334, str(datetime.datetime.now())[:10]))
