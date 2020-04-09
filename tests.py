import unittest

from utils.collections import map_items
from utils.produts import get_total

from models import Product, Order, Product_Order


class TestCollections(unittest.TestCase):
    def test_map_items(self):
        self.assertEqual(map_items([12, 12, 3, 4, 12, 89, 90]), {
            12: 3,
            3: 1,
            4: 1,
            89: 1,
            90: 1
        })

    def test_map_items_empty(self):
        self.assertEqual(map_items([]), {})


class TestProducts(unittest.TestCase):
    def test_order(self):
        order = Order()

        product_1 = Product(id=1, unit_price=100.0)
        product_2 = Product(id=2, unit_price=300.0)
        product_3 = Product(id=3, unit_price=250.0)

        item_1 = Product_Order(product=product_1, quantity=5)
        item_2 = Product_Order(product=product_2, quantity=1)
        item_3 = Product_Order(product=product_3, quantity=4)

        order.products.append(item_1)
        order.products.append(item_2)
        order.products.append(item_3)

        self.assertEqual(get_total(order), 1800.0)

    def test_empty_order(self):
        self.assertEqual(get_total(Order()), 0.0)


if __name__ == '__main__':
    unittest.main()
