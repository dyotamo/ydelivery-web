def get_total(order):
    total = 0.0
    for item in order.products:
        total += (item.product.unit_price * item.quantity)
    return total
