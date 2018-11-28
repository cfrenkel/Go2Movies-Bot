import settings
import pymongo.mongo_client


class DBManagement:
    def __init__(self):
        self.client = pymongo.mongo_client.MongoClient()
        self.db = self.client.get_database(settings.db)
        self.collection = self.db.get_collection(settings.collection)

    def insert_user(self, chat_id, status):
        self.collection.insert_one({"chat_id":chat_id},{"status":status,"movies_list":[], "date":None, "chosen_movie":None, "is_notification":None})

    def update_status(self, chat_id,status):
        self.collection.update_one({"chat_id":chat_id},{"$set":{"status":status}})

    def insert_movie(self, chat_id, movie):
        movie_list = self.collection.find_one({},{"chat_id":chat_id})["movies_list"]
        movie_list.append(movie)
        self.collection.update_one({"chat_id": chat_id}, {"$set": {"movies_list": movie_list}})

    def delete_movie(self, chat_id):
        pass

    def delete_all_movies(self, chat_id):
        self.collection.update_one({"chat_id": chat_id}, {"$set": {"movies_list": []}})

    def insert_chosen_movie(self, chat_id):
        pass

    def get_all_movies(self, chat_id):
        return self.collection.find_one({}, {"chat_id": chat_id})["movies_list"]

    def get_chosen_movie(self, chat_id):
        return self.collection.find_one({}, {"chat_id": chat_id})["chosen_movie"]

    def get_date(self, chat_id):
        return self.collection.find_one({},{"chat_id":chat_id})["date"]

    def insert_date(self, chat_id, date, is_notification=True):
        pass

    def find_user(self, chat_id):
        if self.collection.find({},{"chat_id":chat_id}):
            return True
        return False





