function addBasket(method, product_id) {
    var basket = $("a").filter(function () {
        return $(this).text() == "Корзина"
    });
    if (basket.length == 1) {
        var k_product = $.getElementsByClassName("price")
        $.get(`http://127.0.0.1:5000/api/${method}/${product_id}`);
    }
    else {
        alert("Вы незарегистрированы.");
    }
}