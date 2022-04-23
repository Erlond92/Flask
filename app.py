from flask import Flask, url_for, render_template, request, redirect
from forms import RegistrationForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, current_user
from data import db_session, api
from data.users import User

app = Flask(__name__)
app.config["SECRET_KEY"] = "yandexlyceum_secret_key"
db_session.global_init("db/users.sqlite")
app.register_blueprint(api.blueprint)
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def user_load(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/index", methods=['POST', 'GET'])
@app.route("/", methods=['POST', 'GET'])
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
            return render_template("login.html", title="Войти", form=form, message="Неправильный email")
        password = db_sess.query(User.password).filter(User.email == form_dict["email"]).one()[0]
        if check_password_hash(password, form_dict["password"]):
            user = db_sess.query(User).filter(User.email ==  form_dict["email"]).first()
            login_user(user, remember=True)
            return redirect("/")
        else:
            return render_template("login.html", title="Войти", form=form, message="Неправильный пароль")
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
            return render_template("registration.html",
                                   title="Регистрация", form=form, message="Такая почта уже зарегистрирован")
        user = User()
        user.name = form_dict["username"]
        user.email = form_dict["email"]
        user.password = generate_password_hash(form_dict["password"])
        db_sess.add(user)
        db_sess.commit()
    return render_template("registration.html", title="Регистрация", form=form, message="")


if __name__ == '__main__':
    app.run()
