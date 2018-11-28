import settings
import pymongo.mongo_client


class DBManagement:

    def __init__(self):
        self.client = pymongo.mongo_client.MongoClient()
        self.db = self.client.get_database(settings.db)
        self.collection = self.db.get_collection(settings.collection)

    def insert_user(self, chat_id, status):
        pass

    def update_status(self, chat_id, status):
        self.collection.update_one({'chat_id': chat_id, }, {'status': status, })

    def insert_movie(self, chat_id):
        pass

    def delete_movie(self, chat_id):
        pass

    def delete_all_movies(self, chat_id):
        pass

    def insert_chosen_movie(self, chat_id, movie):
        self.collection.update_one({'chat_id': chat_id, },
                                   {"$set": {"movie": {'name': movie['name'],
                                                       'place': movie['place'],
                                                       'time': movie['time'],
                                                       'trailer': movie['trailer'],
                                                       'image': movie['image']}}})

    def get_all_movies(self, chat_id):
        pass

    def get_chosen_movie(self, chat_id):
        pass

    def get_date(self, chat_id):
        pass

    def insert_date(self, chat_id, date, is_notification=True):
        self.collection.update_one({'chat_id': chat_id, },
                                   {'date': date,
                                    'is_notification': is_notification})

    def find_user(self, chat_id):
        pass





