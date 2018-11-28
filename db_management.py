import settings

class db_management:
    def __init__(self):
        self.db = settings.db
        self.collection = settings.collection

    def init_user(self, chat_id, status):
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

    def insert_date(self, chat_id, is_notification=True):
        pass

