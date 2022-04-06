from flask import Flask, url_for, render_template, request

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def main():
    card_list = [
        {
            "img": url_for("static", filename="/img/lamp.png"),
            "name": "Ягненок",
            "mass": "Вес: 225 г",
            "description": """Фаршированный гречневой кашей,
                        курагой, апельсином и зеленым яблоком""",
            "price": "620 ₽"
        },
        {
            "img": url_for("static", filename="/img/lamp.png"),
            "name": "Ягненок",
            "mass": "Вес: 225 г",
            "description": """Фаршированный гречневой кашей,
                            курагой, апельсином и зеленым яблоком""",
            "price": "620 ₽"
        }
    ]
    if request.method == "GET":
        return render_template("main.html", cards=card_list)
    elif request.method == "POST":
        print("OK")


if __name__ == '__main__':
    app.run()
