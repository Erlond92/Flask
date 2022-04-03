from flask import Flask, url_for, render_template, current_app

app = Flask(__name__)

@app.route('/')
def main():
    return render_template("base.html",
                           base_style=url_for("static", filename="/css/index.css"),
                           calling_svg=url_for("static", filename="/img/Calling.svg"),
                           up_svg=url_for("static", filename="/img/up.svg"),
                           search_svg=url_for("static", filename="/img/search.svg")
                           )


if __name__ == '__main__':
    app.run()
