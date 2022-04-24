from data import db_session
from data.users import User
from flask_login import UserMixin


class UserLogin(UserMixin):
    def create(self, user):
        self.__user = user
        return self.__user

    def from_database(self, id):
        self.__user = db_session.create_session().query(User).filter(User.id == id).first()

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_annonymous(self):
        return False

    def get_id(self):
        return str(self.__user.id)
