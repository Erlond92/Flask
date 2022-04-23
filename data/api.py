from flask import Blueprint

blueprint = Blueprint(
    "basket_api",
    __name__,
    template_folder="templates"
)


@blueprint.route("/api/test")
def test():
    print("TEST")
    return "TEST"
