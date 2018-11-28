# YOUR BOT LOGIC/STORAGE/BACKEND FUNCTIONS HERE
import datetime
import db_management


class Model:
    def __init__(self):
        pass

    def add_user(self, chat_id):
        pass

    def find_user(self, chat_id):
        pass

    def add_movie(self, chat_id, movie):
        pass

    def get_recommended_movies(self, chat_id):
        pass

    def get_recommended_name_movie(self, chosen_movie):
        pass

    def get_recommended_place_movie(self, chosen_movie):
        pass

    def get_recommended_time_movie(self, chosen_movie):
        pass

    def get_recommended_trailer_movie(self, chosen_movie):
        pass

    def get_recommended_image_movie(self, chosen_movie):
        pass

    def choose_movie(self, chat_id, movie):
        pass
    # movie type is list/tuple of all movie info

    def get_chosen_movie(self, chat_id):
        pass

    def delete_movie(self, chat_id, movie):
        pass
        # optional

    def delete_all_movies(self, chat_id):
        pass

    def choose_date(self, chat_id, date=datetime.datetime.now()):
        pass

    def get_movie(self, chosen_movie):
        pass

    def get_all_movies(self, chat_id):
        pass

    def get_date(self, chat_id):
        pass

    def notify(self, chat_id, time_before=60):
        pass
