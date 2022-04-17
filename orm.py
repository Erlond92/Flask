from data import db_session
from data.users import User


def main():
    db_session.global_init("db/test.sqlite")
    user = User()
    user.name = "1254"
    user.about = "1234"
    user.email = "1264@gmail.com"
    db_sess = db_session.create_session()
    db_sess.add(user)
    db_sess.commit()


if __name__ == "__main__":
    main()
