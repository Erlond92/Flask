from flask import Blueprint
from basket import UserBasket
from flask import session

blueprint = Blueprint(
    "basket_api",
    __name__,
    template_folder="templates"
)


@blueprint.route("/api/<int:method>/<int:product_id>")
def basket(method, product_id):
    user = UserBasket(session.get("_user_id"))
    if method == 1:
        user.add_product(product_id)
    elif method == 0:
        user.delet_product(product_id)
    elif method == 2:
        user.clear_basket()
    elif method == 3:
        user.all_delet_product(product_id)
    return "OK"
