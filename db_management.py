import settings
import pymongo.mongo_client

class DBManagement:

    def __init__(self):
        self.client = pymongo.mongo_client.MongoClient()
        self.db = self.client.get_database(settings.db)
        self.collection = self.db.get_collection(settings.collection)

    def insert_user(self, chat_id):
        self.collection.insert_one({"chat_id": chat_id, "status": 'start', "movies_list": [], "date":None, "chosen_movie":None, "is_notification":None, "lat":None, "lon":None})

    def update_status(self, chat_id, status):
        self.collection.update_one({"chat_id": chat_id}, {"$set": {"status": status}})

    def update_movie(self, chat_id):
        self.collection.update_one({"chat_id": chat_id}, {"$set": {"movie": None}})

    def update_lat(self, chat_id, lat):
        self.collection.update_one({"chat_id": chat_id}, {"$set": {"lat": lat}})

    def update_lon(self, chat_id, lon):
        self.collection.update_one({"chat_id": chat_id}, {"$set": {"lon": lon}})

    def insert_movie(self, chat_id, movie):
        movies_list = self.collection.find_one({"chat_id": chat_id})["movies_list"]
        if movie not in movies_list:
            movies_list.append(movie)
            self.collection.update_one({"chat_id": chat_id}, {"$set": {"movies_list": movies_list}})

    def delete_all_movies(self, chat_id):
        self.collection.update_one({"chat_id": chat_id}, {"$set": {"movies_list": []}})

    def insert_chosen_movie(self, chat_id, movie):
        self.collection.update_one({'chat_id': chat_id, },
                                   {"$set": {"movie": movie}})

    def get_status(self, chat_id):
        return self.collection.find_one({"chat_id": chat_id})['status']

    def get_all_movies(self, chat_id):
        return self.collection.find_one({"chat_id": chat_id})["movies_list"]

    # def get_movies_example(self):
    #     return self.collection.find_one()

    def get_chosen_movie(self, chat_id):
        return self.collection.find_one({"chat_id": chat_id})["movie"]

    def get_date(self, chat_id):
        return self.collection.find_one({"chat_id": chat_id})["date"]

    def get_lat(self, chat_id):
        return self.collection.find_one({"chat_id": chat_id})["lat"]

    def get_lon(self, chat_id):
        return self.collection.find_one({"chat_id": chat_id})["lon"]

    def insert_date(self, chat_id, date, is_notification=True):
        self.collection.update_one({'chat_id': chat_id, },
                                   {'date': date,
                                    'is_notification': is_notification})

    def find_user(self, chat_id):
        c = self.collection.count({"chat_id": chat_id})
        if c != 0:
            return True
        return False


class DBManagementHelper:

    def __init__(self):
        self.client = pymongo.mongo_client.MongoClient()
        self.db = self.client.get_database(settings.db)
        self.collection = self.db.get_collection("recommended movies")

    def insert_movie_list(self, chat_id, movie_list):
        self.collection.replace_one({"chat_id": chat_id},{"movies_list": movie_list, "index": 0}, upsert=True)

    def update_index(self, chat_id, index):
        self.collection.update_one({"chat_id": chat_id}, {"$set": {"index": index}})

    def get_index(self, chat_id):
        return self.collection.find_one({"chat_id": chat_id})["index"]

    def get_movies_list(self, chat_id):
        return self.collection.find_one({"chat_id": chat_id})["movies_list"]


