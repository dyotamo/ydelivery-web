import unittest

from utils.produts import get_total
from models import Brew, Order, Brew_Order


class TestBrews(unittest.TestCase):
    def test_order(self):
        order = Order()

        brew_1 = Brew(id=1, unit_price=100.0)
        brew_2 = Brew(id=2, unit_price=300.0)
        brew_3 = Brew(id=3, unit_price=250.0)

        item_1 = Brew_Order(brew=brew_1, quantity=5)
        item_2 = Brew_Order(brew=brew_2, quantity=1)
        item_3 = Brew_Order(brew=brew_3, quantity=4)

        order.brews.append(item_1)
        order.brews.append(item_2)
        order.brews.append(item_3)

        self.assertEqual(get_total(order), 1800.0)

    def test_empty_order(self):
        self.assertEqual(get_total(Order()), 0.0)


if __name__ == '__main__':
    unittest.main()
