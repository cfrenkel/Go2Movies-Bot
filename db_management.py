import settings
import pymongo.mongo_client


class DBManagement:
    def __init__(self):
        self.client = pymongo.mongo_client.MongoClient()
        self.db = self.client.get_database(settings.db)
        self.collection = self.db.get_collection(settings.collection)


    def insert_user(self, chat_id, status):
        pass

    def update_status(self, chat_id):
        pass

    def insert_movie(self, chat_id):
        pass

    def delete_movie(self, chat_id):
        pass

    def delete_all_movies(self, chat_id):
        pass

    def insert_chosen_movie(self, chat_id):
        pass

    def get_all_movies(self, chat_id):
        pass

    def get_chosen_movie(self, chat_id):
        pass

    def get_date(self, chat_id):
        pass

    def insert_date(self, chat_id, is_notification=True):
        pass

    def find_user(self, chat_id):
        pass






