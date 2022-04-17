from data import db_session
from data.users import User


class UserLogin():
    def fromDB(self, user_id, db):
        self.__user = db.getUser(user_id)

    def create(self, user):
        self.__user = user

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_annonymous(self):
        return False

    def get_id(self):
        return str(self.__user['id'])
