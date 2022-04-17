from flask import Flask, url_for, render_template, request, redirect
from forms import RegistrationForm, LoginForm
from data import db_session
from data.users import User

app = Flask(__name__)
app.config["SECRET_KEY"] = "yandexlyceum_secret_key"
db_session.global_init("db/users.sqlite")


@app.route('/', methods=['POST', 'GET'])
def index():
    card_dict = {
        "img": url_for("static", filename="/img/lamp.png"),
        "name": "Ягненок",
        "mass": "Вес: 225 г",
        "description": "Фаршированный гречневой кашей, курагой, апельсином и зеленым яблоком",
        "price": "620 ₽"}
    card_list = [
        {
            "name": "ХОЛОДНЫЕ ЗАКУСКИ",
            "list": [card_dict for _ in range(4)]
        },
        {
            "name": "ГОРЯЧИЕ ЗАКУСКИ",
            "list": [card_dict for _ in range(4)]
        },
        {
            "name": "МЯСНЫЕ БЛЮДА",
            "list": [card_dict for _ in range(4)]
        }
    ]
    if request.method == "GET":
        return render_template("main.html", cards=card_list, title="LOGOS")


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == "POST":
        form_dict = dict(request.form)
        db_sess = db_session.create_session()
        if not db_sess.query(User).filter(User.email == form_dict["email"]).first():
            user = db_sess.query(User).filter(User.id == 1).first()
            print(user)
            return redirect("/registration")
        return redirect("/")
    return render_template("login.html", title="Войти", form=form, message="")
@app.route("/registration", methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    if request.method == "POST":
        form_dict = dict(request.form)
        if form_dict["password"] != form_dict["password_again"]:
            return render_template("registration.html", title="Регистрация", form=form, message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form_dict["email"]).first():
            return render_template("registration.html", title="Регистрация", form=form, message="Такая почта уже зарегистрирован")
        user = User()
        user.name = form_dict["username"]
        user.email = form_dict["email"]
        user.password = form_dict["password"]
        print(user)
        db_sess.add(user)
        db_sess.commit()
    return render_template("registration.html", title="Регистрация", form=form, message="")

if __name__ == '__main__':
    app.run()
