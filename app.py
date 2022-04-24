from flask import Flask, url_for, render_template, request, redirect, session
from data.forms import RegistrationForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user
from data import db_session, api
from data.users import User
from data.product import Product
from data.UserLogin import UserLogin
from basket import UserBasket
import datetime

app = Flask(__name__)
app.permanent_session_lifetime = datetime.timedelta(days=365)
app.config["SECRET_KEY"] = "yandexlyceum_secret_key"
db_session.global_init("db/users.sqlite")
app.register_blueprint(api.blueprint)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return UserLogin().from_database(id=user_id)


@app.route("/index", methods=['POST', 'GET'])
@app.route("/", methods=['POST', 'GET'])
def index():
    db_sess = db_session.create_session()
    l = []
    for id in range(1, 5):
        card_dict = {
            "id": id,
            "img": url_for("static", filename=f"/img/food{id}.png"),
            "name": db_sess.query(Product.name).filter(Product.id == id).first()[0],
            "mass": f"Вес: {db_sess.query(Product.mass).filter(Product.id == id).first()[0]} г",
            "description": db_sess.query(Product.description).filter(Product.id == id).first()[0],
            "price": f"{db_sess.query(Product.price).filter(Product.id == id).first()[0]} ₽"}
        l.append(card_dict)
    card_list = [
        {
            "name": "ХОЛОДНЫЕ ЗАКУСКИ",
            "list": l
        },
        {
            "name": "ГОРЯЧИЕ ЗАКУСКИ",
            "list": l
        },
        {
            "name": "МЯСНЫЕ БЛЮДА",
            "list": l
        }
    ]
    if request.method == "GET":
        a = session.get("_user_id") is not None
        return render_template("main.html", cards=card_list, title="LOGOS", auth=a,
                               basket_k=UserBasket(session.get("_user_id")).l_product())


@app.route("/login", methods=['GET', 'POST'])
def login():
    session.pop("_user_id", None)
    form = LoginForm()
    if request.method == "POST":
        form_dict = dict(request.form)
        db_sess = db_session.create_session()
        if not db_sess.query(User).filter(User.email == form_dict["email"]).first():
            return render_template("login.html", title="Войти", form=form, message="Неправильный email")
        password = db_sess.query(User.password).filter(User.email == form_dict["email"]).one()[0]
        if check_password_hash(password, form_dict["password"]):
            user = db_sess.query(User).filter(User.email == form_dict["email"]).first()
            user_login = UserLogin()
            user_login.create(user)
            login_user(user_login, remember=True)
            return redirect("/index")
        else:
            return render_template("login.html", title="Войти", form=form, message="Неправильный пароль",
                                   basket_k=UserBasket(session.get("_user_id")).l_product())
    return render_template("login.html", title="Войти", form=form, message="", auth=False,
                           basket_k=UserBasket(session.get("_user_id")).l_product())


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
                                   title="Регистрация", form=form, message="Такая почта уже зарегистрирован",
                                   basket_k=UserBasket(session.get("_user_id")).l_product())
        user = User()
        user.name = form_dict["username"]
        user.email = form_dict["email"]
        user.password = generate_password_hash(form_dict["password"])
        db_sess.add(user)
        db_sess.commit()
    return render_template("registration.html", title="Регистрация", form=form, message="", auth=False,
                           basket_k=UserBasket(session.get("_user_id")).l_product())


@app.route("/basket", methods=["GET", "POST"])
# @login_required
def basket():
    bask = UserBasket(session.get("_user_id")).view_basket()
    db_sess = db_session.create_session()
    basket_view = []
    for key in bask.keys():
        item = dict()
        item["id"] = key
        item["name"] = db_sess.query(Product.name).filter(Product.id == key).first()
        item["description"] = db_sess.query(Product.description).filter(Product.id == key).first()
        item["k"] = bask[key]
        item["price"] = db_sess.query(Product.price).filter(Product.id == key).first()
        basket_view.append(item)
    a = session.get("_user_id") is not None
    return render_template("basket.html", basket=basket_view, auth=a, title="Корзина",
                           basket_k=UserBasket(session.get("_user_id")).l_product())


if __name__ == '__main__':
    app.run(debug=True)
