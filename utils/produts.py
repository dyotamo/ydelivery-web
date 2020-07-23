def get_total(order):
    total = 0.0
    for item in order.brews:
        total += (item.brew.unit_price * item.quantity)
    return total
