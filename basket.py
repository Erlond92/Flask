import json


class UserBasket:
    def __init__(self, user_id):
        self.id = user_id
        self.create_table()

    def create_table(self):
        with open(f"user_basket/{self.id}.json", "w", encoding="utf-8") as f:
            d = {self.id: {}}
            f.write(json.dumps(d))

    def add_product(self, product_id, n):
        with open(f"user_basket/{self.id}.json", "r", encoding="utf-8") as f:
            basket = json.load(f)[str(self.id)]
            try:
                if basket[product_id]:
                    basket[product_id] += n
            except KeyError:
                basket[product_id] = n
        with open(f"user_basket/{self.id}.json", "w") as f:
            f.write(json.dumps({self.id: basket}))

    def delet_product(self, product_id, n):
        with open(f"user_basket/{self.id}.json", "r", encoding="utf-8") as f:
            basket = json.load(f)[str(self.id)]
            if basket[product_id] > n:
                basket[product_id] -= n
            else:
                basket[product_id] = 0
        with open(f"user_basket/{self.id}.json", "w") as f:
            f.write(json.dumps({self.id: basket}))

    def clear_basket(self):
        with open(f"user_basket/{self.id}.json", "w", encoding="utf-8") as f:
            f.write(json.dumps({self.id: {}}))


if __name__ == "__main__":
    test = UserBasket(1)
    test.add_product(12, 2)
    test.add_product(15, 12)
    test.create_table()
