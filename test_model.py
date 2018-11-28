# YOUR BACKEND TESTS HERE
from model import Model
import unittest


class ModelTestCase(unittest.TestCase):

    def setUp(self):
        pass

    # def test_add_user(self, chat_id):
    #     self.assertEqual(chat_id, "")
    #
    # def test_add_movie(self, chat_id, movie):
    #     DB.insert_movie(chat_id, movie)
    #
    #
    # def get_recommended_movies(self, chat_id):
    #     pass
    #
    #
    # def get_recommended_name_movie(self, chosen_movie):
    #     return chosen_movie
    #
    #
    # def get_recommended_place_movie(self, chosen_movie):
    #     return
    #
    #
    # def get_recommended_time_movie(self, chosen_movie):
    #     pass
    #
    #
    # def get_recommended_trailer_movie(self, chosen_movie_id):
    #     querystring = {"film_id": chosen_movie_id}
    #     response = requests.request("GET", secret_settings.url_movieglu_api + "trailers/",
    #                                 headers=secret_settings.headers_movieglu_api, params=querystring)
    #     return response.json()['trailers']['high'][0]['film_trailer']
    #
    #
    # def get_recommended_image_movie(self, chosen_movie_id):
    #     querystring = {"film_id": chosen_movie_id}
    #     response = requests.request("GET", secret_settings.url_movieglu_api + "images/",
    #                                 headers=secret_settings.headers_movieglu_api, params=querystring)
    #     return response.json()['poster']['1']['medium']['film_image']
    #
    #
    # def choose_movie(self, chat_id, movie):
    #     DB.insert_chosen_movie(chat_id, movie)
    #
    #
    # # movie type is list/tuple of all movie info
    #
    # def get_chosen_movie(self, chat_id):
    #     return DB.get_chosen_movie(chat_id)
    #
    #
    # def delete_movie(self, chat_id, movie):
    #     pass
    #     # optional
    #
    #
    # def delete_all_movies(self, chat_id):
    #     DB.delete_all_movies(chat_id)
    #
    #
    # def choose_date(self, chat_id, date=datetime.datetime.now(), is_notification=True):
    #     DB.insert_date(chat_id, date, is_notification)
    #
    #
    # def get_all_movies(self, chat_id):
    #     return DB.get_all_movies(chat_id)
    #
    #
    # def get_date(self, chat_id):
    #     return DB.get_date(chat_id)
    #
    #
    # def notify(self, chat_id, time_before=60):
    #     pass