# YOUR BOT LOGIC/STORAGE/BACKEND FUNCTIONS HERE
import datetime
import requests
import db_management as DB
import secret_settings

def add_user(chat_id):
    if not DB.DBManagement().find_user(chat_id):
        DB.DBManagement().insert_user(chat_id)
        return True
    return False

def update_status(chat_id, status):
    DB.DBManagement().update_status(chat_id, status)

def get_status( chat_id):
    return DB.DBManagement().get_status(chat_id)

def add_movie(chat_id, movie_name):
    querystring = {"query": movie_name.replace(" ", "+"), "n": 1}
    response = requests.request("GET", secret_settings.url_movieglu_api + "filmLiveSearch/",
                                headers=secret_settings.headers_movieglu_api, params=querystring)
    movie_id = response.json()['films'][0]['film_id']
    movie = get_movie_details(movie_id)
    movie_det = {"film_id": movie_id, "movie_name": movie_name,
                 "ganer": movie['genres'][0]['genre_id'], "cast": [c['cast_id'] for c in movie["cast"]],
                 "directors": [
                     c['director_id'] for c in movie["directors"]]}
    DB.DBManagement().insert_movie(chat_id, movie_det)

def get_recommended_movies(lat, lon, date):  # chat_id,
    cinemas = get_cinemas_nearby(3, lat, lon)
    films = []
    movies = []
    for cinema in cinemas:
        films.append({"cinema": cinema, "films": get_cinema_show_times(cinema['cinema_id'], date)})

    for film in films:
        for f in film["films"]:
            movie_det = get_movie_details(f['film_id'])
            trailer = movie_det['trailers']['med'][0]['film_trailer']
            image = movie_det['images']['poster']['1']['medium']['film_image']
            movies.append({"cinema": film['cinema'], "ganer": movie_det['genres'][0]['genre_id'],
                           "cast": [c['cast_id'] for c in movie_det["cast"]],
                           "directors": [c['director_id'] for c in movie_det["directors"]], "trailers": trailer,
                           "images": image})

    recommend = []
    # my_movies = get_all_movies(chat_id)
    my_movies = [{"film_id": 277058,
                  "movie_name": "The Predator",
                  "ganer": 5,
                  "cast": [13906, 13907, 13050],
                  "directors": [3549]}]
    for my_movie in my_movies:
        for movie in movies:
            if my_movie['ganer'] == movie['ganer'] or set(my_movie['cast']) ^ set(movie['cast']) or set(
                    my_movie['directors']) ^ set(movie['directors']):
                recommend.append(movie)

    return recommend

def get_recommended_name_movie( chosen_movie):
    return chosen_movie

def get_recommended_place_movie( chosen_movie):
    pass

def get_recommended_time_movie( chosen_movie):
    pass

def get_recommended_trailer_movie( chosen_movie_id):
    querystring = {"film_id": chosen_movie_id}
    response = requests.request("GET", secret_settings.url_movieglu_api + "trailers/",
                                headers=secret_settings.headers_movieglu_api, params=querystring)
    return response.json()['trailers']['high'][0]['film_trailer']

def get_recommended_image_movie( chosen_movie_id):
    querystring = {"film_id": chosen_movie_id}
    response = requests.request("GET", secret_settings.url_movieglu_api + "images/",
                                headers=secret_settings.headers_movieglu_api, params=querystring)
    return response.json()['poster']['1']['medium']['film_image']

def choose_movie( chat_id, movie):
    DB.DBManagement().insert_chosen_movie(chat_id, movie)

# movie type is list/tuple of all movie info

def get_chosen_movie( chat_id):
    return DB.DBManagement().get_chosen_movie(chat_id)

def delete_movie( chat_id, movie):
    pass
    # optional

def delete_all_movies( chat_id):
    DB.DBManagement().delete_all_movies(chat_id)

def choose_date( chat_id, date=datetime.datetime.now(), is_notification=True):
    DB.DBManagement().insert_date(chat_id, date, is_notification)

def get_all_movies( chat_id):
    return DB.DBManagement().get_all_movies(chat_id)

def get_date( chat_id):
    return DB.DBManagement().get_date(chat_id)

def get_cinemas_nearby( n_cinemas, lat, lon):
    querystring = {"n": n_cinemas}
    headers = secret_settings.headers_movieglu_api
    headers['geolocation'] = f"{lat};{lon}"
    response = requests.request("GET", secret_settings.url_movieglu_api + "cinemasNearby/",
                                headers=headers, params=querystring)
    cinemas = response.json()['cinemas']
    return cinemas

def get_cinema_show_times( cinema_id, date):
    querystring = {"cinema_id": cinema_id, "date": date}
    headers = secret_settings.headers_movieglu_api
    response = requests.request("GET", secret_settings.url_movieglu_api + "cinemaShowTimest/",
                                headers=headers, params=querystring)
    result = response.json()
    films = result['films']
    return films

def get_movie_details( movie_id):
    querystring = {"film_id": movie_id}
    response = requests.request("GET", secret_settings.url_movieglu_api + "filmDetails/",
                                headers=secret_settings.headers_movieglu_api, params=querystring)
    return response

def notify( chat_id, time_before=60):
    pass

