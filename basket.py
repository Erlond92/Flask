import json


class UserBasket:
    def __init__(self, user_id):
        self.id = user_id

    def create_table(self):
        with open(f"user_basket/{self.id}.json", "w", encoding="utf-8") as f:
            f.write(json.dumps({}))

    def add_product(self, product_id):
        with open(f"user_basket/{self.id}.json", "r", encoding="utf-8") as f:
            basket = json.load(f)
            product_id = str(product_id)
            try:
                if basket[product_id] != 0:
                    basket[product_id] += 1
            except KeyError:
                basket[product_id] = 1
        with open(f"user_basket/{self.id}.json", "w") as f:
            f.write(json.dumps(basket))

    def delet_product(self, product_id):
        with open(f"user_basket/{self.id}.json", "r", encoding="utf-8") as f:
            product_id = str(product_id)
            basket = json.load(f)
            basket[product_id] -= 1
        with open(f"user_basket/{self.id}.json", "w") as f:
            f.write(json.dumps(basket))

    def clear_basket(self):
        with open(f"user_basket/{self.id}.json", "w", encoding="utf-8") as f:
            f.write(json.dumps({}))

    def view_basket(self):
        with open(f"user_basket/{self.id}.json", "r", encoding="utf-8") as f:
            return json.load(f)

    def all_delet_product(self, product_id):
        with open(f"user_basket/{self.id}.json", "r", encoding="utf-8") as f:
            product_id = str(product_id)
            basket = json.load(f)
            basket[product_id] = 0
        with open(f"user_basket/{self.id}.json", "w") as f:
            f.write(json.dumps(basket))

    def l_product(self):
        with open(f"user_basket/{self.id}.json", "r", encoding="utf-8") as f:
            basket = json.load(f)
        return sum([basket[key] for key in basket.keys()])
