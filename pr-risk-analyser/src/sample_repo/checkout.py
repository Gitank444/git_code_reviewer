from pricing import calculate_total
from notification import send_receipt

def process_checkout(cart):
    total = calculate_total(cart)
    send_receipt(total)
    return total

def risky_checkout(cart):
    total = calculate_total(cart)
    return total